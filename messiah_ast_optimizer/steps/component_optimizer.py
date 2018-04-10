# -*- coding:utf-8 -*-
"""
规则：
1）作为Component的Module不能定义除Componennt Class和Import外的东西，否则调过合并，并抛出警告信息需要修改

1) 若有Class Attr和FunctionDef重名， 抛错
2）若有除Class Attr、FunctionDef、Property以外的其他AstNode， 抛错
3）import有重名且不一样 ， 抛错， 有些有try import这种如何处理？
4）若有Class及其自类带有无法识别的Meta，跳过合并（后续增加handler，自定义处理）
"""

import ast
import itertools
import common.classutils

from core.utils import enum
from core.eval import PyFrame
from collections import OrderedDict, defaultdict
from core.exception import MEvalException
from core.base import MessiahStepVisitor, MessiahStepTransformer, MessiahStepTokenizer, MessiahOptimizerStep



class ComponentTokenizer(MessiahStepTokenizer):
	pass

  
class ComponentVisitor(MessiahStepVisitor):
	def visit_ClassDef(self, node, context):
		if node.decorator_list:
			pass
		return node

	def visit_Name(self, node, context):
		pass
		# if isinstance(node.ctx, ast.Load):
		# 	print node.load()

	def visit_Call(self, node, context):
		pass


class GlobalEntryMerger(object):

	def __init__(self):
		self.entries = defaultdict(list)
		self.names = {}
		self.merged_files = []

	def check(self, node):
		checker = getattr(self, 'check_%s' % node.__class__.__name__)
		return checker(node)

	def check_Import(self, node):
		return self._checkImport(node)

	def check_ImportFrom(self, node):
		return self._checkImport(node, fromlist=True)

	def _checkImport(self, node, fromlist=False):
		for alias in node.names:
			name = alias.inferName()
			if name == '*':
				return False

			if name not in self.names:
				continue

			desc = self.names[name]
			if desc[0] != node.__class__.__name__:
				return False
			else:
				type, relname, index = self.names[name]
				cur = self.entries[type][index]
				if relname != name or not self.sameModule(node, cur):
					return False

		return True

	def sameModule(self, src, dst):
		return src.findModule() is dst.findModule()

	def check_Assign(self, node):
		names = utils.get_names(node)
		if not names:
			return False

		return any((name in self.names for name in names))

	def check_FunctionDef(self, node):
		return node.name in self.names

	def check_ClassDef(self, node):
		return node.name in self.names

	def merge(self, node):
		merger = getattr(self, 'merge_%s' % node.__class__.__name__)
		return merger(node)

	def merge_Import(self, node):
		return self._mergeImport(node)

	def merge_ImportFrom(self, node):
		return self._mergeImport(node)

	def _mergeImport(self, node):
		remove = True
		type = node.__class__.__name__
		for alias in node.names:
			name = alias.inferName()
			if name in self.names:
				continue

			remove = False
			self.names[name] = (type, name, len(self.entries[type]))

		if not remove:
			self.entries[type].append(node)


	def merge_Assign(self, node):
		self.entries['Assign'].append(node)

		names = utils.get_names(node)
		for name in names:
			self.names[name] = ('Assign', )

	def merge_FunctionDef(self, node):
		self.entries['FunctionDef'].append(node)
		self.names[node.id] = ('FunctionDef', )

	def merge_ClassDef(self, node):
		self.entries['ClassDef'].append(node)
		self.names[node.id] = ('ClassDef', )


class ComponentTransformer(MessiahStepTransformer):

	def __init__(self, optimizer):
		super(ComponentTransformer, self).__init__(optimizer)
		self.merge_cls = {}

	def onVisitFile(self, fullpath, relpath):
		self.entry_merger = None

	def visit_ClassDef(self, node, context):
		for deco in node.decorator_list:
			if isinstance(deco, ast.Call) and deco.func.id == 'Components':
				if not self.entry_merger:
					self.entry_merger = GlobalEntryMerger()

				return self.mergeComponents(node, deco)

		# print 'MRO of %s: %s' % (node.name, [n.name for n in node.nMro()])
		# print 'FullBases of %s: %s' % (node.name, [n.name for n in node.nFullBases()])
		return node

	def mergeComponents(self, node, deco):
		locals = dict(node.parent.nScope().scope.locals)
		globals = dict(node.nModule().scope.locals)
		frame = PyFrame(locals, globals)

		components = self.getAllComponents(node.name, deco, frame)
		skips = self._mergeComponents(node, components)
		return node

	def getAllComponents(self, name, node, frame):
		components = []
		try:
			posargs, keyargs = node._evalArgs(frame)
			membername = keyargs.get("postfix", "%sMember") % name

			for args in posargs:
				if isinstance(args, ast.Module):
					args = args.load(membername)
					if not args:
						raise RuntimeError('Merge Component get unknown component')

				if isinstance(args, ast.ClassDef):
					components.append(args)
				else:
					raise RuntimeError('Merge Component with unknown type')
		except MEvalException:
			components = []

		return components

	def _mergeComponents(self, host, components):
		methods, attrs, properties = {}, [], []
		skips, host_module = [], host.nModule()

		for comp in components:
			mro = comp.nMro()
			comp_module = comp.nModule()
			skip = False

			if comp_module is not host_module and not self.mergeGlobalEntries(comp_module):
				skip = True

			if not self.canMerge(mro):
				skip = True

			if skip:
				skips.append(comp)
				continue

			_methods, _attrs, _properties = self._fetchComponent(comp, mro)
			methods.update(_methods)
			attrs.extend(_attrs)
			properties.extend(_properties)

		host.body = [b for b in itertools.chain(properties, attrs, methods.values())]
		return skips

	def _fetchComponent(self, component, mro):
		methods, attrs = component.fullGetmembers(mro)
		properties = component.fullGetbodies(mro=mro, predicate=self.isPropertyDef)

		return methods, attrs, properties

	def isPropertyDef(self, node):
		if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
			return True

	def mergeGlobalEntries(self, module):
		"""
		1) 模块里的命名不能和其他component模块一样且指向不同内容
		2）除了Assign，AugAssign，Import, Import_from, ClassDef, FunctionDef, If, Try, 还有其他stmt
		3）除了Import和ImportFrom可能是相同Import，其他的name def不能重名
		"""

		if module.__file__ in self.entry_merger.merged_files:
			return True

		for body in module.body:
			if not isinstance(body, (ast.Import, ast.ImportFrom, ast.Assign, ast.FunctionDef, ast.ClassDef)):
				raise RuntimeError('Invalid Stmt defined in Component of %s' % module.__file__)

			if isinstance(body, ast.ClassDef) and body.name.endswith('Member'):
				continue

			if not self.entry_merger.check(body):
				return False

		for body in module.body:
			if isinstance(body, ast.ClassDef) and body.name.endswith('Member'):
				continue

			self.entry_merger.merge(body)

		print self.entry_merger.entries

		return True

	def canMerge(self, mro):
		for cls in mro:
			if not cls or cls.decorator_list:
				return False
		return True


ComponentOptimizeStep = MessiahOptimizerStep(tokenizer=ComponentTokenizer, visitor=ComponentVisitor, transformer=ComponentTransformer)
