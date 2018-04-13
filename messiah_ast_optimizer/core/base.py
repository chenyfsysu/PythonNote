# -*- coding:utf-8 -*-

import ast
import utils
import const

from collections import defaultdict


class VisitorMeta(type):
	def __new__(mcls, name, bases, attrs):
		previsitors = defaultdict(list)
		visitors = defaultdict(list)
		postvisitors = defaultdict(list)
		for base in bases:
			base_previsitors = getattr(base, '_previsitors', None)
			base_previsitors and previsitors.update(base_previsitors)
			base_visitors = getattr(base, '_visitors', None)
			base_visitors and visitors.update(base._visitors)
			base_postvisitors = getattr(base, '_postvisitors', None)
			base_postvisitors and postvisitors.update(base._postvisitors)

		for key, func in attrs.iteritems():
			if key.startswith('previsit_'):
				previsitors[key].append(key)
			elif key.startswith('visit_'):
				visitors[key].append(key)
			elif key.startswith('postvisit_'):
				postvisitors[key].append(key)

		attrs['_previsitors'] = previsitors
		attrs['_visitors'] = visitors
		attrs['_postvisitors'] = postvisitors

		return super(VisitorMeta, mcls).__new__(mcls, name, bases, attrs)


class IVisitor(object):
	__metaclass__ = VisitorMeta


class Visitor(IVisitor):

	def __init__(self, optimizer=None):
		self.optimizer = optimizer
		self.logger = optimizer.getLogger(self.__class__.__name__)

	def onEnter(self):
		pass

	def onExit(self):
		pass

	def onVisitFile(self, fullpath, relpath):
		pass

	def onLeaveFile(self, fullpath, relpath):
		pass


class HostVisitor(object):
	__metaclass__ = VisitorMeta

	def __init__(self, rootpath, optimizer):
		super(HostVisitor, self).__init__()
		self.rootpath = rootpath
		self.optimizer = optimizer
		self.logger = optimizer.getLogger(self.__class__.__name__)

		self.previsitors = defaultdict(list)
		self.visitors = defaultdict(list)
		self.postvisitors = defaultdict(list)
		self.raw_visitors = []

	def walk(self):
		raise NotImplementedError

	def activate(self, visitors):
		self.raw_visitors = visitors
		map(self.register, visitors)

	def register(self, visitor):
		for func in visitor._previsitors:
			key = func[9:]
			method = getattr(visitor, func)
			self.previsitors[key].append(method)

		for func in visitor._visitors:
			key = func[6:]
			method = getattr(visitor, func)
			self.visitors[key].append(method)

		for func in visitor._postvisitors:
			key = func[10:]
			method = getattr(visitor, func)
			self.postvisitors[key].append(method)

	def previsit(self, key, *args):
		for visitor in self.previsitors.get(key, ()):
			visitor(*args)

	def visit(self, key, node, *args):
		for visitor in self.visitors.get(key, ()):
			node = visitor(node, *args)

		return node

	def postvisit(self, key, *args):
		for visitor in self.postvisitors.get(key, ()):
			visitor(*args)

	def notifyEnter(self):
		for visitor in self.raw_visitors:
			visitor.onEnter()

	def notifyExit(self):
		for visitor in self.raw_visitors:
			visitor.onExit()

	def notifyVisitFile(self, fullpath, relpath):
		for visitor in self.raw_visitors:
			visitor.onVisitFile(fullpath, relpath)

	def notifyLeaveFile(self, fullpath, relpath):
		for visitor in self.raw_visitors:
			visitor.onLeaveFile(fullpath, relpath)


class AstVisitor(Visitor, ast.NodeVisitor):
	pass


class AstHostVisitor(HostVisitor):

	def fullvisit(self, node):
		visitor = getattr(self, 'fullvisit_%s' % node.__class__.__name__)
		return visitor(node)


class MessiahStepTokenizer(Visitor):
	pass


class MessiahStepVisitor(AstVisitor):
	pass


class MessiahStepTransformer(AstVisitor):
	pass


class MessiahOptimizerStep(object):

	def __init__(self, tokenizer=None, visitor=None, transformer=None):
		self.tokenizer = tokenizer
		self.visitor = visitor
		self.transformer = transformer
