# -*- coding:utf-8 -*-

import os
import scandir
import unparser

from walker import TokenizeWalker, VisitWalker, TransformWalker
from mixins import ConfigHandlerMixin, LogHandlerMixin


def OptimizeStep(*stepcls):
	def _OptimizeStep(kclass):
		tokenizer_visitors = []
		visit_visitors = []
		transform_visitors = []

		for step in stepcls:
			step.tokenizer and tokenizer_visitors.append(step.tokenizer)
			step.visitor and visit_visitors.append(step.visitor)
			step.transformer and transform_visitors.append(step.transformer)

		kclass._tokenizer_visitors = tokenizer_visitors
		kclass._visit_visitors = visit_visitors
		kclass._transform_visitors = transform_visitors

		return kclass

	return _OptimizeStep


class MessiahOptimizer(ConfigHandlerMixin, LogHandlerMixin):
	def __init__(self, path, setting, cmd_settings):
		ConfigHandlerMixin.__init__(self, setting, cmd_settings)
		LogHandlerMixin.__init__(self)

		self.path = path
		self.logger = self.getLogger('MessiahOptimizer')
		self.ignore_dirs = [os.path.normpath(d) for d in self.config.IGNORE_DIRS]
		self.ignore_files = [os.path.normpath(f) for f in self.config.IGNORE_FILES]
		self.file = None
		self.filter_files = {}

		self.tokenize_walker = TokenizeWalker(path, self)
		self.visit_walker = VisitWalker(path, self)
		self.transform_walker = TransformWalker(path, self)

		self.tokenizers = []
		self.visitors = []
		self.transformers = []

		self.optimize_data = {}

	def optimize(self):
		self.activate()
		self.filterOptimizeFiles()

		self.processTokenize()
		self.processVisit()
		self.processTransform()

	def activate(self):
		self.tokenizers = [cls(self) for cls in self._tokenizer_visitors]
		self.tokenize_walker.activate(self.tokenizers)

		self.visitors = [cls(self) for cls in self._visit_visitors]
		self.visit_walker.activate(self.visitors)

		self.transformers = [cls(self) for cls in self._transform_visitors]
		self.transform_walker.activate(self.transformers)

	def filterOptimizeFiles(self):
		self.filter_files = {}

		if os.path.isfile(self.path):
			head, tail = os.path.split(self.path)
			self.filter_files[self.path] = tail
			self.path = head
			return

		for root, dirs, files in scandir.walk(self.path, topdown=True):
			dirs[:] = [d for d in dirs if os.path.normpath(os.path.join(root, d)) not in self.ignore_dirs]

			for file in files:
				if file.endswith('.py'):
					fullpath = os.path.join(root, file)
					relpath = os.path.relpath(fullpath, self.path)
					self.filter_files[fullpath] = relpath

	def processTokenize(self):
		self.tokenize_walker.notifyEnter()
		for fullpath, relpath in self.filter_files.iteritems():
			self.tokenize_walker.walk(fullpath, relpath)

		self.tokenize_walker.notifyExit()

	def processVisit(self):
		self.visit_walker.notifyEnter()
		for fullpath, relpath in self.filter_files.iteritems():
			self.visit_walker.walk(fullpath, relpath)

		self.visit_walker.notifyExit()

	def processTransform(self):
		self.transform_walker.notifyEnter()
		for fullpath, relpath in self.filter_files.iteritems():
			node = self.transform_walker.walk(fullpath, relpath)
			fullpath = os.path.join('dump', relpath)
			self.unparse(fullpath, node)

		self.transform_walker.notifyExit()

	def storeData(self, visitor, data):
		self.optimize_data[visitor.__name__] = data

	def loadData(self, visitor, default=None):
		return self.optimize_data.get(visitor.__name__, default)

	def unparse(self, path, tree):
		src = '\n'.join(['# -*- coding:utf-8 -*-', unparser.unparse(tree)])
		open(path, 'w').write(src)
