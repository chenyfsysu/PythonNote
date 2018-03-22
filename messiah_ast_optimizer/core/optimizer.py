# -*- coding:utf-8 -*-

from walker import TokenizeWalker, VisitWalker, TransformWalker


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
		kclass._transform_visitors = transformer

		return kclass

	return _OptimizeStep


class MessiahOptimizer(object):
	def __init__(self):
		self.tokenize_walker = TokenizeWalker()
		self.visit_walker = VisitWalker()
		self.transform_walker = TransformWalker()

		self.tokenizers = []
		self.visitors = []
		self.transformers = []

		self.optimize_data = {}

	def optimize(self):
		self.activate()

	def activate(self):
		self.tokenizers = [cls(self) for cls in self._tokenizer_visitors]
		self.tokenize_walker.activate(self.tokenizers)

		self.visitors = [cls(self) for cls in self._visit_visitors]
		self.visit_walker.activate(self.visitors)

		self.transformers = [cls(self) for cls in self._transform_visitors]
		self.transform_walker.activate(self.transformers)


	def filterOptimizeFiles(self):
		pass

	def processTokenize(self):
		pass

	def processVisit(self):
		pass

	def processTransform(self):
		pass

	def storeData(self, visitor, data):
		self.optimize_data[visitor.__name__] = data

	def loadData(self, visitor, data):
		return self.optimize_data.get(visitor.__name__, None)


	def filterExecuteFiles(self):
		self.filter_files = {}
		for root, dirs, files in scandir.walk(self.path, topdown=True):
			dirs[:] = [d for d in dirs if os.path.normpath(os.path.join(root, d)) not in self.ignore_dirs]

			for file in files:
				if file.endswith('.py'):
					fullpath = os.path.join(root, file)
					relpath = os.path.relpath(fullpath, self.path)
					self.filter_files[fullpath] = relpath

	def executeTokenize(self):
		for fullpath, relpath in self.filter_files.iteritems():
			self._executeTokenize(fullpath, relpath)

		self.optimizer.endTokenize()

	def _executeTokenize(self, path, relpath):
		self.file = open(path)
		self.optimizer.executeTokenize(relpath, self.file.readline)
		self.file.close()

		print 'tokenizer completed, %s' % path

	def executeVisit(self):
		for fullpath, relpath in self.filter_files.iteritems():
			self.file = open(fullpath)
			tree = ast.parse(self.file.read())
			self.optimizer.executeVisit(relpath, tree)
			print 'vistor completed, %s' % fullpath

		self.optimizer.endVisit()

	def executeTransform(self):
		modifys = {}

		for fullpath, relpath in self.filter_files.iteritems():
			self.file = open(fullpath)
			tree = ast.parse(self.file.read())
			modify = self.optimizer.executeTransform(relpath, tree)
			if True or tree.dirty:
				self.unparse(fullpath, tree)
			print 'transformer completed, %s' % fullpath

	def unparse(self, path, tree):
		src = '\n'.join(['# -*- coding:utf-8 -*-', unparser.unparse(tree)])
		# print src
		open(path, 'w').write(src)
