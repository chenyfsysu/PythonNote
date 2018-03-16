# -*- coding:utf-8 -*-
"""
	注意！
	1.具体的作用域必须运行时才能决定，这里分析得到的作用域不能处理
	  1）运行时修改
	  2）在ast访问顺序后定义的， 如下面运行时添加到globals运行是正确的，但是在ast分析func时是没有a的
		 def func():
			print a
		 a = 1
		 func()
	2.闭包未处理
	3.global声明已处理

	namespace建议做辅助分析，比如检查某个属性是否是一个Class Definition这种一般不会运行时替换函数内容。不要强依赖，例如
	利用namespace来分析属性值，但是locals一般够保证正确。
"""

import utils
from collections import defaultdict


class Definition(object):
	class DefinitionType(object):
		def __init__(self):
			super(Definition.DefinitionType, self).__init__()

	class ModuleType(DefinitionType):
		def __init__(self):
			super(Definition.ModuleType, self).__init__()

		@classmethod
		def create(cls, node):
			return {node.__class__.__name__ : cls()}

	class ImportType(DefinitionType):
		def __init__(self, name, asname):
			super(Definition.ImportType, self).__init__()
			self.name = name
			self.asname = asname

		@classmethod
		def create(cls, node):
			return {alias.name: cls(alias.name, alias.asname) for alias in node.names}

	class ImportFromType(DefinitionType):
		def __init__(self, name, asname, module, level):
			super(Definition.ImportFromType, self).__init__()
			self.module = module
			self.name = name
			self.asname = asname
			self.level = level

		@classmethod
		def create(cls, node):
			return {alias.name: cls(alias.name, alias.asname, node.module, node.level) for alias in node.names}

	class ClassDefType(DefinitionType):
		def __init__(self, name):
			super(Definition.ClassDefType, self).__init__()
			self.name = name

		@classmethod
		def create(cls, node):
			return {node.name: cls(node.name)}

	class FunctionDefType(DefinitionType):
		def __init__(self, name):
			self.name = name

		@classmethod
		def create(cls, node):
			return {node.name: cls(node.name)}

	class AssignType(DefinitionType):
		@classmethod
		def create(cls, node):
			definitions = {}
			value = utils.get_constant(node.value)

			for target in node.targets:
				names = utils.get_pure_names(target)
				items = utils.unfold_assign(names, value) if names else {}
				definitions.update(items)

			return definitions

	@classmethod
	def create(cls, node):
		kcls = getattr(cls, '%sType' % node.__class__.__name__, None) 
		return kcls.create(node) if kcls else {}


class Namespace(dict):
	def __init__(self):
		super(Namespace, self).__init__()


class Context(object):
	"""包括作用域和当前分析node属于哪个function、哪个class"""

	def __init__(self):
		super(Context, self).__init__()
		self.locals_stack = []
		self.globals = Namespace()

		self.frames = []

		self.file_outdegrees = defaultdict(list) # 依赖
		self.file_indegrees = defaultdict(list) # 被依赖


	def addDefinition(self, vars):
		self.locals.update(vars)
		if isinstance(self.frame, Definition.ModuleType):
			self.globals.update(vars)

	def setDefinition(self, key, value):
		self.locals[key] = value
		if isinstance(self.frame, Definition.ModuleType):
			self.globals[key] = value

	def getAttribute(self, attr, only_locals=False):
		if attr in self.locals:
			return self.locals[attr]
		return self.globals.get(attr, None)

	def incFileDependency(self, src, dst):
		self.file_outdegrees[src].append(dst)
		self.file_indegrees[dst].append(src)

	@property
	def locals(self):
		return self.locals_stack[-1]

	@property
	def frame(self):
		return self.frames[-1]
