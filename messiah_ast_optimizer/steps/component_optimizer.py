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
	def __init__(self, node, type, module_path):
		self.type = type
		self.module_path = module_path
		self.node = node


class ImportEntry(Entry):
	def __init__(self, node, type, module_path, fullname):
		super(ImportEntry, self).__init__(node, type, module_path)
		self.fullname = fullname


class ImportFromEntry(Entry):
	def __init__(self, node, type, module_path, fromlist):
		super(ImportFromEntry, self).__init__(node, type, module_path)
		self.fromlist = fromlist


class ComponentAnalyser(object):
	"""
	Component的Mro的内容分割输出，不能合并的Component也要继续分析，因为可能有其他模块依赖该模块内容
	"""
	def __init__(self, comp_postfix='Member'):
		self.comp_postfix = comp_postfix
		self.dirty = False

		self.processed_files = set()
		self.globals_entries = OrderedDict()
		self.globals_redirects = set()

		self.classes_meths = OrderedDict()
		self.classes_stmts = []
		self.classes_stmts_names = {}
		self.reserved_funcs = {}
		self.reserved_args_tmpl = {}

	def analyze(self, node, host_module, ignore_globals=False):
		mro = node.nMro()

		for cls in reversed(mro):
			module = cls.nModule()
			self.processed_files.add(module.__file__)

			if not ignore_globals and not self.dirty:
				module is not host_module and self.mergeGlobals(module)

			self.mergeClasses(cls)
			self.globals_redirects.add(cls.name)

	def mergeGlobals(self, module):
		for body in module.body:
			if self.dirty:
				return

			if isinstance(body, ast.ClassDef) and body.name.endswith(self.comp_postfix):
				continue

			if isinstance(body, ast.Expr) and isinstance(body.value, ast.Str):
				continue

			if isinstance(body, (ast.Import, ast.ImportFrom, ast.Assign, ast.FunctionDef, ast.ClassDef)):
				merger = getattr(self, 'mergeGlobals_%s' % body.__class__.__name__)
				accept = merger(body)
				self.dirty = not accept

	def mergeGlobals_Import(self, node):
		path = node.nModule().__file__

		for alias in node.names:
			module = node.findModule(alias.name)
			if alias.name != module.__name__:
				alias.name = module.__name__

			name = alias.inferName()
			if name not in self.globals_entries:
				self.globals_entries[name] = ImportEntry(node, 'Import', path, alias.name)

			else:
				entry = self.globals_entries[name]
				if not isinstance(entry, ImportEntry):
					self.markGlobalsDuplicate(name, path, entry.path)
					return False

				if not entry.node.findModule(entry.fullname) is node.findModule(alias.name):
					self.markGlobalsDuplicate(name, path, entry.path)
					return False

		return True

	def mergeGlobals_ImportFrom(self, node):
		path = node.nModule().__file__
		module = node.findModule()
		if module.__name__ != node.module:
			node.module = module.__name__

		for alias in node.names:
			name = alias.inferName()

			if name == '*':
				self.logger.warning('componennt %s import star from %s, merge is skip', node.nModule().__file__, node.module)
				return False

			if name not in self.names:
				self.globals_entries[name] = ImportFrom(node, 'ImportFrom', path, alias.name)
			else:
				entry = self.globals_entries[name]
				if not isinstance(entry, ImportFromEntry):
					self.markGlobalsDuplicate(name, path, entry.path)
					return False

				if entry.node.findModule() is not module:
					return False

		self.globals_entries['ImportFrom'].append(node)
		return True

	def mergeGlobals_Assign(self, node):
		path = node.nModule().__file__

		for target in node.targets:
			names = get_names(target)

			if not names:
				self.logger.warning('Strange assignment is defined in %s', node.nModule().__file__)
				return False

			for name in names :
				if name in self.globals_entries:
					self.markGlobalsDuplicate(name, path, self.globals_entries[name].path)
					return False

				self.globals_entries[name] = Entry(node, 'Stmt', path)

		return True

	def mergeGlobals_FunctionDef(self, node):
		return self._mergeGlobals_FunctionOrClass(node)

	def mergeGlobals_ClassDef(self, node):
		return self._mergeGlobals_FunctionOrClass(node)

	def _mergeGlobals_FunctionOrClass(self, node):
		path = node.nModule().__file__
		accept = node.name not in self.globals_entries
		if not accept:
			name = node.name
			self.markGlobalsDuplicate(name, path, self.globals_entries[name].path)
		else:
			self.globals_entries[node.name] = Entry(node, 'Stmt', path)

		return accept

	def mergeClasses(self, cls):
		if not self.canMergeClass(cls):
			self.dirty = True
			return

		for body in cls.body:
			if isinstance(body, ast.Pass):
				continue

			if isinstance(ast.Assign, ast.FunctionDef, ast.ClassDef):
				merger = getattr(self, 'mergeClasses_%s' % body.__class__.__name__)
				accept = merger(body)
				self.dirty = not accept

	def mergeClasses_Assign(self, node):
		comp_name = node.parent.name
		path = node.nModule().__file__

		for target in node.targets:
			names = get_names(target)

			if not names:
				self.logger.warning('Strange assignment is defined in %s, Component(%s)', path, comp_name)
				self.dirty = True
				continue

			for name in names:
				self.classes_stmts_names[name] = node

	def mergeClasses_FunctionDef(self, node):
		if node.name.endswith('component__'):
			self.handleReservedFunc(node)

		module = node.nModule()
		path = module.__file__

		if node.name in self.classes_stmts_names:
			cur_path = self.classes_stmts_names[name].path
			raise RuntimeError('Global definition of name %s in %s is duplicate with file in %s' % (node.name, path, cur_path))

		newer = node.name in self.classes_meths or self.classes_meths[node.name][-1].nModule() is module
		if newer:
			self.classes_meths[node.name] = [node]
		else:
			self.classes_meths[node.name].append(node)				

	def mergeClasses_ClassDef(self, node):
		path = node.nModule().__file__
		self.classes_stmts_names[node.name] = Entry(node, 'ClassDef', path)
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

	def canMergeClass(self, cls):
		if cls.decorator_list:
			return False

	def markGlobalsDuplicate(self, name, dst, src):
		self.logger.warning('Global definition of name %s in %s is duplicate with file in %s', name, dst, src)

	def markClassesDuplicate(self, name, comp, dst, src):
		self.logger.warning('Component(%s) definition of name %s in %s is duplicate with file in %s', name, comp, dst, src)


class GlobalMerger(object):
	pass


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
		skips, host_module = [], host.nModule()

		analysers = []
		for comp in components:
			analyser = ComponentAnalyser()
			analyser.analyze(comp, host_module)
			analysers.append(analyser)

		for analyser in analysers:
			if analyser.dirty:
				skips.append(analyser)
				continue

			# 1）如果Globals名字空间有冲突，不能合并
			# 2）如果前面被调过的Component有名字覆盖关系, 不能合并
			for skip in skips:
				"""检查有没有名字覆盖关系，如果有，则当前也不能合并"""
				if skip.checkDuplicate(analyser):
					skips.append(analyser)

			# 合并

			# comp_module = comp.nModule()
			# mro = comp.nMro()

			# if comp_module is not host_module and not self.mergeGlobalEntries(comp_module):
			# 	skips.append(comp)
			# 	continue

			# """这里就算跳过了也要处理完，有些有依赖关系的Component, 如iCombatUnit中的calcRideProps是要被impRide覆盖的，因此如果impCombat不能合并，impRide也不能合并"""
			# if not self.mergeComponentEntries(comp):
			# 	skips.append(comp)
			# 	continue

		return skips

	def checkMergeEntries(self, host_module, mro):
		for comp in components:
			pass

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

			if isinstance(body, (ast.Import, ast.ImportFrom, ast.Assign, ast.FunctionDef, ast.ClassDef)):
				pass

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
