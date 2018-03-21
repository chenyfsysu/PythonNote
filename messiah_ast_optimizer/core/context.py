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

	mark:
	不能解析value的要保证target是正确存储的，没有在namespace的为None，有但是不能解析的为UnknowDefinition
	try ..:
		A = 1
	except:
		A = 2
	这种类型应该为不能解析
"""

import ast
import utils
import const
from collections import defaultdict
from objects import ObjectAllocator, LazyImportObject


class Frame(object):
	def __init__(self, name, type):
		self.name = name
		self.type = type

	@classmethod
	def create(kcls, node):
		name = 'Module' if isinstance(node, ast.Module) else node.name
		return kcls(name, node.__class__.__name__)


class Namespace(dict):
	def __init__(self):
		super(Namespace, self).__init__()


class Context(object):
	"""包括作用域和当前分析node属于哪个function、哪个class"""

	def __init__(self):
		super(Context, self).__init__()
		self.__file__ = ''
		self.__name__ = ''

		self.locals_stack = []
		self.globals = Namespace()

		self.frames = []
		self.module_loader = None

		self.file_outdegrees = defaultdict(list) # 依赖
		self.file_indegrees = defaultdict(list) # 被依赖


	def storeAll(self, vars):
		"""store"""
		self.locals.update(vars)
		if self.frame.type == 'Module':
			self.globals.update(vars)

	def store(self, name, value):
		"""store"""
		self.locals[name] = value
		if self.frame.type == ast.Module.__name__:
			self.globals[name] = value

	def load(self, name, lazy=True):
		"""load"""
		if name in self.locals:
			val = self.locals[name]
		else:
			val = self.globals.get(name, None)
		if val and not lazy:
			val = self.loadImport(val)

		return val

	def loadImport(self, val):
		if not isinstance(val, LazyImportObject) or val.node:
			return val

		module, node = self.loader.load(*val.dump())
		val.module = module
		val.node = node

		return val


	def incFileDependency(self, src, dst):
		self.file_outdegrees[src].append(dst)
		self.file_indegrees[dst].append(src)

	@property
	def locals(self):
		return self.locals_stack[-1]

	@property
	def frame(self):
		return self.frames[-1]
