# -*- coding:utf-8 -*-
"""
规则：
1）作为Component的Module定义的Global内容会被合并到Host
2）如果Component的Module的Globals和已合并的Component有重名的定义，除非是相同的Import或者是ImportFrom，否则合并将会调过并报警告信息
eg: Component A: from Model import Model
	Component B: import Model
	两个Component的Model含义不一样，则调过合并Component B

3) 如果Component存在Class Attr和FunctionDef重名, 调过合并并抛建议修改信息
4）若有除Class Attr、FunctionDef、Property以外的其他AstNode， 调过合并并抛建议修改信息
5）如果Component存在Meta，装饰器等，调过合并， 抛提示信息
6）Component里面定义的内容，除了函数外不允许存在同名， 否则抛错
7）有些有依赖关系的Component， 如iCombatUnit中的calcRideProps是要被impRide覆盖的，因此如果impCombat不能合并，impRide也不能合并
"""

import ast
import itertools
import operator
import common.classutils

from core.utils import enum, get_names, new_importfrom, unparse_src
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

	def visit_ClassDef(self, node, context):
		for deco in node.decorator_list:
			if isinstance(deco, ast.Call) and deco.func.id == 'Components':
				return self.handleComponentDependency(context.__fullpath__, node, deco)

	def handleComponentDependency(self, path, node, deco):
		locals = dict(node.parent.nScope().scope.locals)
		globals = dict(node.nModule().scope.locals)
		frame = PyFrame(locals, globals)

		files = self.getComponentDependency(node.name, deco, frame)
		files and self.optimizer.addFileDependencies(path, files)

	def getComponentDependency(self, name, node, frame):
		host_module = node.nModule()

		files = []
		try:
			posargs, keyargs = node._evalArgs(frame)
			membername = keyargs.get("postfix", "%sMember") % name

			for args in posargs:
				if isinstance(args, ast.Module):
					files.append(args.__file__)
				elif isinstance(args, ast.ClassDef):
					module = args.nModule()
					module is not host_module and files.append(module.__file__)
				else:
					raise RuntimeError('Merge Component with unknown type')
		except MEvalException:
			self.logger.debug('Merge is skip because of get component Error')
			files = []

		return files


class EntryMerger(object):

	def __init__(self, logger):
		self.logger = logger
		self.entries = defaultdict(list)

	def dump(self):
		raise NotImplementedError

	def check(self, node):
		checker = getattr(self, 'check_%s' % node.__class__.__name__)
		return checker(node)

	def merge(self, node):
		merger = getattr(self, 'merge_%s' % node.__class__.__name__)
		return merger(node)


class GlobalEntryMerger(EntryMerger):

	def __init__(self, logger):
		super(GlobalEntryMerger, self).__init__(logger)
		self.names = {}
		self.merged_files = {}

	def dump(self):
		getter = operator.itemgetter('Import', 'ImportFrom', 'Stmt')
		return [body for c in getter(self.entries) for body in c]

	def sameModule(self, src, dst):
		return src.findModule() is dst.findModule()

	def check_Import(self, node):
		accept = True
		for alias in node.names:
			name = alias.inferName()

			if name not in self.names:
				continue

			desc = self.names[name]
			if desc[0] != 'Import':
				accept = False
			else:
				type, fullname, index, _ = self.names[name]
				cur = self.entries[type][index]
				accept = cur.findModule(fullname) is node.findModule(alias.name)

			if not accept:
				self.markDuplicate(name, node.nModule().__file__, desc[-1])
				break

		return accept

	def check_ImportFrom(self, node):
		accept = True
		for alias in node.names:
			name = alias.inferName()

			if name == '*':
				self.logger.warning('componennt %s import star from %s, merge is skip', node.nModule().__file__, node.module)
				return False

			if name not in self.names:
				continue

			desc = self.names[name]
			if desc[0] != 'ImportFrom':
				accept = False
			else:
				type, fromlist, index, _ = self.names[name]
				cur = self.entries[type][index]
				accept = fromlist == alias.name and cur.findModule() is node.findModule()

			if not accept:
				self.markDuplicate(name, node.nModule().__file__, desc[-1])
				break

		return accept

	def check_Assign(self, node):
		for target in node.targets:
			names = get_names(target)

			if not names:
				self.logger.warning('Strange assignment is defined in %s', node.nModule().__file__)
				return False

			for name in names :
				if name in self.names:
					self.markDuplicate(name, node.nModule().__file__, self.names[name][-1])
					return False

		return True

	def check_FunctionDef(self, node):
		return self._checkFunctionOrClass(node)

	def check_ClassDef(self, node):
		return self._checkFunctionOrClass(node)

	def _checkFunctionOrClass(self, node):
		accept = node.name not in self.names
		if not accept:
			name = node.name
			self.markDuplicate(name, node.nModule().__file__, self.names[name][-1])

		return accept

	def merge_Import(self, node):
		self._mergeImport(node)
		for alias in node.names:
			module = node.findModule(alias.name)
			if alias.name != module.__name__:
				alias.name = module.__name__

	def merge_ImportFrom(self, node):
		self._mergeImport(node)
		
		module = node.findModule()
		if module.__name__ != node.module:
			node.module = module.__name__

	def _mergeImport(self, node):
		"""有些相对Import"""
		remove = True
		type = node.__class__.__name__
		path = node.nModule().__file__
		for alias in node.names:
			name = alias.inferName()
			if name in self.names:
				continue

			remove = False
			self.names[name] = (type, alias.name, len(self.entries[type]), path)

		if not remove:
			self.entries[type].append(node)

	def merge_Assign(self, node):
		self.entries['Stmt'].append(node)
		path = node.nModule().__file__

		for target in node.targets:
			names = get_names(target)
			for name in names:
				self.names[name] = ('Stmt', path)

	def merge_FunctionDef(self, node):
		self.entries['Stmt'].append(node)
		self.names[node.name] = ('Stmt', node.nModule().__file__)

	def merge_ClassDef(self, node):
		self.entries['Stmt'].append(node)
		self.names[node.name] = ('Stmt', node.nModule().__file__)

	def markDuplicate(self, name, dst, src):
		self.logger.warning('Global definition of name %s in %s is duplicate with file in %s', name, dst, src)


class ComponentEntryMerger(EntryMerger):
	ComponentFuncArgs = {
		'init': 'bdict',
		'post': 'bdict',
		'fini': 'bdict',
		'tick': 'dt'
	}

	def __init__(self, logger):
		super(ComponentEntryMerger, self).__init__(logger)
		self.stmt_names = {}
		self.func_names = {}
		self.components_func = defaultdict(list)

	def dump(self):
		getter = operator.itemgetter('Stmt', 'FunctionDef')
		bodies = [body for c in getter(self.entries) for body in c]
		bodies.extend(self.generateComponentFunc())

		return bodies

	def generateComponentFunc(self):
		funcs = []
		for key in self.ComponentFuncArgs:
			stmts = []			
			containers = self.components_func[key]
			if not containers:
				continue

			args = self.ComponentFuncArgs[key]
			for func in containers:
				stmts.append(self._generateFuncCall(func, args))

			funcs.append(self._generateFuncDef(key, args, stmts))

		return funcs

	def _generateFuncCall(self, func, args):
		func = ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr=func, ctx=ast.Load())
		args = [ast.Name(id=args, ctx=ast.Load())]
		return ast.Expr(value=ast.Call(func=func, args=args, keywords=[], starargs=None, kwargs=None))

	def _generateFuncDef(self, key, args, stmts):
		name = '_host_%s' % key
		args = [ast.Name(id='self', ctx=ast.Param()), ast.Name(id=args, ctx=ast.Param())]
		arguments = ast.arguments(args=args, vararg=None, kwarg=None, defaults=[])
		return ast.FunctionDef(name=name, args=arguments, body=stmts, decorator_list=[])

	def getEntryModule(self, name):
		return self.stmt_names[name][-1]

	def check_FunctionDef(self, node):
		return True

	def check_Expr(self ,node):
		return True

	def check_Assign(self, node):
		comp_name = node.parent.name
		for target in node.targets:
			names = get_names(target)

			if not names:
				self.logger.warning('Strange assignment is defined in %s, Component(%s)', node.nModule().__file__, comp_name)
				return False

			for name in names :
				if name in self.stmt_names:
					self.markDuplicate(name, comp_name, node.nModule().__file__, self.getEntryModule(name))
					return False

		return True

	def check_ClassDef(self, node):
		accept = node.name not in self.stmt_names
		if not accept:
			self.markDuplicate(node.name, node.parent.name, node.nModule().__file__, self.getEntryModule(node.name))

		return accept

	def merge_FunctionDef(self, node):
		if node.name.endswith('component__'):
			name = '%s%s' % (node.name, node.nModule().__name__.replace('.', '_'))
			key = node.name.split('_')[2]
			self.components_func[key].append(name)
			node.name = name

		if False and node.name in self.func_names:
			_, _, index = self.func_names[node.name]
			self.entries['FunctionDef'][index] = node
		else:
			self.func_names[node.name] = ('FunctionDef', node.nModule().__file__, len(self.func_names))
			self.entries['FunctionDef'].append(node)

	def merge_Expr(self, node):
		self.entries['Stmt'].append(node)

	def merge_Assign(self, node):
		self.entries['Stmt'].append(node)
		path = node.nModule().__file__

		for target in node.targets:
			names = get_names(target)
			for name in names:
				self.stmt_names[name] = ('Stmt', path)

	def merge_ClassDef(self, node):
		self.entries['Stmt'].append(node)
		self.stmt_names[node.name] = ('Stmt', node.nModule().__file__)

	def markDuplicate(self, name, comp, dst, src):
		self.logger.warning('Component(%s) definition of name %s in %s is duplicate with file in %s', name, comp, dst, src)


class ComponentTransformer(MessiahStepTransformer):

	def __init__(self, optimizer):
		super(ComponentTransformer, self).__init__(optimizer)

	def onVisitFile(self, fullpath, relpath):
		self.global_merger = None
		self.comp_merger = None

	def visit_ClassDef(self, node, context):
		for deco in node.decorator_list:
			if isinstance(deco, ast.Call) and deco.func.id == 'Components':
				self.logger.debug('Start merge class %s', node.name)

				self.comp_merger = ComponentEntryMerger(self.logger)
				if not self.global_merger:
					self.global_merger = GlobalEntryMerger(self.logger)

				context.markDirty(True)
				return self.mergeComponents(node, deco)

		return node

	def mergeComponents(self, node, deco):
		locals = dict(node.parent.nScope().scope.locals)
		globals = dict(node.nModule().scope.locals)
		frame = PyFrame(locals, globals)

		components = self.getAllComponents(node.name, deco, frame)
		if not components:
			return node

		skips = self.doMergeComponents(node, components)
		self.updateDecorator(node, deco, skips)
		self.updateHostComponent(node)

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
						continue
						raise RuntimeError('Merge Component get unknown component')

				if isinstance(args, ast.ClassDef):
					components.append(args)
				else:
					raise RuntimeError('Merge Component with unknown type')
		except MEvalException:
			self.logger.debug('Merge is skip because of get component Error')
			components = []

		return components

	def doMergeComponents(self, host, components):
		methods, attrs, properties = {}, [], []
		skips, host_module = [], host.nModule()

		for comp in components:
			comp_module = comp.nModule()

			if comp_module is not host_module and not self.mergeGlobalEntries(comp_module):
				skips.append(comp)
				continue

			"""这里就算跳过了也要处理完，有些有依赖关系的Component, 如iCombatUnit中的calcRideProps是要被impRide覆盖的，因此如果impCombat不能合并，impRide也不能合并"""
			if not self.mergeComponentEntries(comp):
				skips.append(comp)
				continue

		return skips

	def mergeGlobalEntries(self, module):
		"""
		1) 模块里的命名不能和其他component模块一样且指向不同内容
		2）除了Assign，AugAssign，Import, Import_from, ClassDef, FunctionDef, If, Try, 还有其他stmt
		3）除了Import和ImportFrom可能是相同Import，其他的name def不能重名
		"""

		if module.__file__ in self.global_merger.merged_files:
			return self.global_merger.merged_files[module.__file__]

		for body in module.body:
			if isinstance(body, ast.Expr) and isinstance(body.value, ast.Str):
				continue

			if not isinstance(body, (ast.Import, ast.ImportFrom, ast.Assign, ast.FunctionDef, ast.ClassDef)):
				self.global_merger.merged_files[module.__file__] = False #TODO
				return False
				raise RuntimeError('Invalid Stmt defined in Component of %s, type: %s' % (module.__file__, body.__class__.__name__))

			if isinstance(body, ast.ClassDef) and body.name.endswith('Member'):
				continue

			if not self.global_merger.check(body):
				self.global_merger.merged_files[module.__file__] = False
				return False

		for body in module.body:
			if isinstance(body, ast.Expr) and isinstance(body.value, ast.Str):
					continue

			if isinstance(body, ast.ClassDef) and body.name.endswith('Member'):
				continue

			self.global_merger.merge(body)

		self.global_merger.merged_files[module.__file__] = True
		return True

	def mergeComponentEntries(self, comp):
		module = comp.nModule()
		mro = comp.nMro()

		if not self.canMerge(mro):
			return False

		for cls in reversed(mro):
			for body in cls.body:
				if isinstance(body, ast.Pass):
					continue

				if not isinstance(body, (ast.Expr, ast.Assign, ast.FunctionDef, ast.ClassDef)):
					return False #TODO
					raise RuntimeError('Invalid Stmt defined in Component of %s, src: \n%s' % (module.__file__, unparse_src(body)))

				if not self.comp_merger.check(body):
					return False

			for body in cls.body:
				if isinstance(body, ast.Pass):
					continue

				self.comp_merger.merge(body)

		return True

	def updateDecorator(self, node, deco, skips):
		if not skips:
			return node.decorator_list.remove(deco)

		deco.args = []
		deco.starargs = None
		host_module = node.nModule()
		for cls in skips:
			module = cls.nModule()
			if module is host_module:
				deco.args.append(ast.Name(id=cls.name, ctx=ast.Load()))
			else:
				name = '%s_%s_%d' % (module.__name__.split('.')[-1], cls.name, len(deco.args))
				deco.args.append(ast.Name(id=name, ctx=ast.Load()))
				isnert_node = new_importfrom(module.__name__, cls.name, name, parent=host_module)
				self.global_merger.merge_ImportFrom(isnert_node)

	def updateHostComponent(self, host):
		if self.comp_merger:
			host.body.extend(self.comp_merger.dump())

		self.comp_merger = None

	def canMerge(self, mro):
		# """
		if len(mro) > 1:
			self.logger.warning('Merge was skip because inherit %s in %s', mro[0].name, mro[0].nModule().__file__)
			return False
		# """

		for cls in mro:
			if not cls or cls.decorator_list:
				self.logger.warning('Merge was skip because decorator_list %s in %s', mro[0].name, mro[0].nModule().__file__)
				return False
		return True

	def isPropertyDef(self, node):
		return isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)

	def postvisit_Module(self, node):
		if self.global_merger:
			body = self.global_merger.dump()
			body.extend(node.body)
			node.body = body

		self.global_merger = None
		return node


ComponentOptimizeStep = MessiahOptimizerStep(tokenizer=ComponentTokenizer, visitor=ComponentVisitor, transformer=ComponentTransformer)
