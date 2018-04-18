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


class Entry(object):
	def __init__(self, name, node, mname, mpath):
		self.name = name
		self.node = node
		self.mname = mname
		self.mpath = mpath


class ImportEntry(Entry):
	def __init__(self, name, node, mname, mpath, fullname):
		super(ImportEntry, self).__init__(name, node, mname, mpath)
		self.fullname = fullname


	def equals(self, node, name):
		return self.node.findModule(self.fullname) is node.findModule(name)


class ImportFromEntry(Entry):
	def __init__(self, name, node, mname, mpath, fromlist):
		super(ImportFromEntry, self).__init__(name, node, mname, mpath)
		self.fromlist = fromlist


	def equals(self, node, name):
		return self.fromlist == name and self.node.findModule() is node.findModule()


class EntryMerger(object):

	def __init__(self, logger):
		self.logger = logger

	def dump(self):
		raise NotImplementedError

	def check(self, node):
		checker = getattr(self, 'check_%s' % node.__class__.__name__, self.check_Default)
		return checker(node)

	def check_Default(self, node):
		raise NotImplementedError

	def merge(self, node):
		merger = getattr(self, 'merge_%s' % node.__class__.__name__, self.merge_Default)
		return merger(node)

	def merge_Default(self, node):
		raise NotImplementedError


class GlobalEntryMerger(EntryMerger):

	def __init__(self, logger):
		super(GlobalEntryMerger, self).__init__(logger)
		self.globals_def = OrderedDict()
		self.globals_imports = defaultdict(list)
		self.globals_imports_def = {}
		self.processed_files = {}

	def dump(self):
		getter = operator.itemgetter('Import', 'ImportFrom')
		bodies = [node for c in getter(self.globals_imports) for node in c]

		bodies.extend(self.inferDef())

		return bodies

	def inferDef(self):
		infers = {}
		for name, entry in self.globals_def.iteritems():
			if entry.mname not in infers:
				infers[entry.mname]= [entry.name]
			else:
				infers[entry.mname].append(entry.name)

		nodes = []
		for mname, fromlist in infers.iteritems():
			names = [(name, '') for name in fromlist]
			nodes.append(new_importfrom(mname, names))

		return nodes

	def check_Import(self, node):
		path = node.nModule().__file__

		for alias in node.names:
			name = alias.inferName()

			if name in self.globals_def:
				self.markDuplicate(name, path, self.globals_def[name].mpath)
				return False

			if name in self.globals_imports_def:
				entry = self.globals_imports_def[name]
				accept = isinstance(entry, ImportEntry) and entry.equals(node, alias.name)
				if not accept:
					self.markDuplicate(name, path, entry.mpath)
					return False

		return True

	def check_ImportFrom(self, node):
		path = node.nModule().__file__

		for alias in node.names:
			name = alias.inferName()

			if name == '*':
				self.logger.warning('componennt %s import star, merge is skip', path)
				return False

			if name in self.globals_def:
				self.markDuplicate(name, path, self.globals_def[name].mpath)
				return False

			if name in self.globals_imports_def:
				entry = self.globals_imports_def[name]
				accept = isinstance(entry, ImportFromEntry) and entry.equals(node, name)
				if not accept:
					self.markDuplicate(name, path, entry.mpath)
					return False

		return True

	def check_Assign(self, node):
		path = node.nModule().__file__
		
		for target in node.targets:
			names = get_names(target)

			if not names:
				self.logger.warning('Strange assignment is defined in %s', path)
				return False

			for name in names:
				if not self._checkGlobalName(name, path):
					return False

		return True

	def check_FunctionDef(self, node):
		return self._checkGlobalName(node.name, node.nModule().__file__)

	def check_ClassDef(self, node):
		return self._checkGlobalName(node.name, node.nModule().__file__)

	def _checkGlobalName(self, name, path):
		entry = None
		if name in self.globals_def:
			entry = self.globals_def[name]

		if name in self.globals_imports_def:
			entry = self.globals_imports_def[name]

		if entry:
			self.markDuplicate(name, path, entry.mpath)
			return False

		return True

	def merge_Import(self, node):
		self._mergeImport(node, ImportEntry)
		for alias in node.names:
			module = node.findModule(alias.name)
			if alias.name != module.__name__:
				alias.name = module.__name__

	def merge_ImportFrom(self, node):
		self._mergeImport(node, ImportFromEntry)
		
		module = node.findModule()
		if module.__name__ != node.module:
			node.module = module.__name__

	def _mergeImport(self, node, entry_cls):
		"""有些相对Import"""
		remove = True

		module = node.nModule()
		for alias in node.names:
			name = alias.inferName()
			if name in self.globals_imports_def:
				continue

			remove = False
			self.globals_imports_def[name] = entry_cls(name, node, module.__name__, module.__file__, alias.name)

		if not remove:
			self.globals_imports[node.__class__.__name__].append(node)

	def merge_Assign(self, node):
		module = node.nModule()
		for target in node.targets:
			names = get_names(target)
			for name in names:
				self.globals_def[name] = Entry(name, node, module.__name__, module.__file__)

	def merge_FunctionDef(self, node):
		module = node.nModule()
		self.globals_def[node.name] = Entry(node.name, node, module.__name__, module.__file__)

	def merge_ClassDef(self, node):
		module = node.nModule()
		self.globals_def[node.name] = Entry(node.name, node, module.__name__, module.__file__)

	def markDuplicate(self, name, dst, src):
		self.logger.warning('Global definition of name %s in %s is duplicate with file in %s', name, dst, src)


class ComponentEntryMerger(EntryMerger):

	def __init__(self, logger):
		super(ComponentEntryMerger, self).__init__(logger)
		self.skip_names = {}

		self.classes_meths = OrderedDict()
		self.classes_stmts = []
		self.classes_stmts_names = {}
		self.reserved_comp_cls = []
		self.reserved_funcs = defaultdict(list)
		self.reserved_args_tmpl = {}

	def dump(self):
		bodies = self.classes_stmts
		bodies.extend([body for name, meths in self.classes_meths.iteritems() for body in meths])
		bodies.extend(self.dumpReservedFuncs())

		return bodies

	def addSkipNames(self, cls):
		file = cls.nModule.__file__

		for name in cls.scope.lookups.iterkesy():
			self.skip_names[name] = file

	def check_Default(self, node):
		return True

	def check_FunctionDef(self, node):
		if node.name in self.skip_names:
			self.markSkip(node.name, node.nModule().__file__, self.skip_names[node.name])
			return False

		return True

	def check_Assign(self, node):
		path = node.nModule().__file__
		comp_name = node.parent.name
		for target in node.targets:
			names = get_names(target)

			if not names:
				self.logger.warning('Strange assignment is defined in %s, Component(%s), merge is skip', path, comp_name)
				return False

			for name in names :
				if name == '__metaclass__':
					self.logger.warning('MetaClass is defined in %s, Component(%s), merge is skip', path, comp_name)
					return False

				if name in self.skip_names:
					self.markSkip(name, path, self.skip_names[name])
					return False

		return True

	def check_ClassDef(self, node):
		if node.name in self.skip_names:
			self.markSkip(node.name, node.nModule().__file__, self.skip_names[node.name])
			return False

		return True

	def merge_Default(self, node):
		self.classes_stmts.append(node)

	def merge_FunctionDef(self, node):
		if node.name.endswith('component__'):
			self.handleReservedFunc(node)
		
		if node.name.startswith("__") and node.name.endswith("__"):
			return

		module = node.nModule()
		newer = node.name not in self.classes_meths or self.classes_meths[node.name][-1].nModule() is not module
		if newer:
			self.classes_meths[node.name] = [node]
		else:
			self.classes_meths[node.name].append(node)

	def merge_Assign(self, node):
		self.classes_stmts.append(node)

	def merge_ClassDef(self, node):
		self.classes_stmts.append(node)

	def handleReservedFunc(self, node):
		name = '%s%s' % (node.name, node.nModule().__name__.replace('.', '_'))
		key = node.name.split('_')[2]

		if key not in self.reserved_args_tmpl:
			self.reserved_args_tmpl[key] = node.args
		else:
			tmpl = self.reserved_args_tmpl[key]
			if tmpl.argsFlag() != node.args.argsFlag():
				self.reserved_args_tmpl[key] = ast.arguments(args=[], vararg='args', kwarg='kwargs', defaults=[])

		self.reserved_funcs[key].append(name)
		node.name = name

	def dumpReservedFuncs(self):
		funcs = []
		for key, containers in self.reserved_funcs.iteritems():
			if not containers:
				continue

			stmts = []			
			tmpl = self.reserved_args_tmpl[key]
			for func in containers:
				stmts.append(self._dumpFuncCall(func, tmpl))

			funcs.append(self._dumpFuncDef(key, tmpl, stmts))

		return funcs

	def _dumpFuncCall(self, func, tmpl):
		func = ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr=func, ctx=ast.Load())
		args = [ast.Name(id=name.id, ctx=ast.Load()) for name in tmpl.args[1:]] if tmpl.args else []
		starargs = ast.Name(id=tmpl.vararg, ctx=ast.Load()) if tmpl.vararg else None
		kwargs = ast.Name(id=tmpl.kwarg, ctx=ast.Load()) if tmpl.kwarg else None
		return ast.Expr(value=ast.Call(func=func, args=args, keywords=[], starargs=starargs, kwargs=kwargs))

	def _dumpFuncDef(self, key, args, stmts):
		name = '_host_%s' % key
		return ast.FunctionDef(name=name, args=args, body=stmts, decorator_list=[])

	def markDuplicate(self, name, comp, dst, src):
		self.logger.warning('Component(%s) definition of name %s in %s is duplicate with file in %s', name, comp, dst, src)

	def markSkip(self, name, dst, src):
		self.logger.warning('Component definition of name %s in %s, name is skip by %s' % name, dst, src)


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

		# print 'MRO of %s: %s' % (node.name, [n.name for n in node.nMro()])
		# print 'FullBases of %s: %s' % (node.name, [n.name for n in node.nFullBases()])
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
			mro = comp.nMro()
			dirty = not self.mergeGlobalEntries(mro, host_module)

			if not dirty:
				dirty = not self.mergeComponentEntries(mro)

			if dirty:
				skips.append(comp)
				# 记录被skip的name

		return skips

	def mergeGlobalEntries(self, mro, host_module):
		"""
		1) 模块里的命名不能和其他component模块一样且指向不同内容
		2）除了Assign，AugAssign，Import, Import_from, ClassDef, FunctionDef, If, Try, 还有其他stmt
		3）除了Import和ImportFrom可能是相同Import，其他的name def不能重名
		"""

		pending, processed = [], []
		for cls in mro:
			module = cls.nModule()
			self.logger.debug('start merge global entries of %s' % module.__file__)

			if module is host_module:
				continue

			if module.__file__ in self.global_merger.processed_files:
				accept = self.global_merger.processed_files[module.__file__]

				if not accept:
					return False
				else:
					continue

			for body in module.body:
				if not isinstance(body, (ast.Import, ast.ImportFrom, ast.Assign, ast.FunctionDef, ast.ClassDef)):
					continue

				if isinstance(body, ast.ClassDef) and body.name.endswith('Member'):
					continue

				if not self.global_merger.check(body):
					self.global_merger.processed_files[module.__file__] = False
					return False

				pending.append(body)

			processed.append(module.__file__)

		for body in pending:
			self.global_merger.merge(body)

		for file in processed:
			self.global_merger.processed_files[file] = True

		return True

	def mergeComponentEntries(self, mro):
		for cls in reversed(mro):
			module = cls.nModule()

			if not self.canMergeClasses(cls):
				return False

			for body in cls.body:
				if isinstance(body, ast.Pass):
					continue

				if not self.comp_merger.check(body):
					return False

		for cls in reversed(mro):
			for body in cls.body:
				if isinstance(body, ast.Pass):
					continue

				self.comp_merger.merge(body)

		return True

	def addSkipComponentNames(self, mro):
		for cls in mro:
			self.comp_merger.addSkipNames(cls)

	def updateDecorator(self, node, deco, skips):
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
				isnert_node = new_importfrom(module.__name__, ((cls.name, name),), parent=host_module)
				self.global_merger.merge_ImportFrom(isnert_node)

	def updateHostComponent(self, host):
		if self.comp_merger:
			host.body.extend(self.comp_merger.dump())

		self.comp_merger = None

	def canMergeClasses(self, cls):
		if cls.decorator_list:
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
