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

from collections import defaultdict
from itertools import imap
from const import NT_LOCAL, NT_GLOBAL_IMPLICIT, NT_GLOBAL_EXPLICIT, NT_FREE, NT_CELL, NT_UNKNOWN, NT_DUMP
from const import ST_MODULE, ST_CLASS, ST_FUNCTION, ST_GENERATOR


class Scope(object):
	def __init__(self, type, name, lookup, locals):
		self.type = type
		self.name = name
		self.lookup = lookup
		self.locals = locals

	def identify(self, name):
		return self.lookup.get(name, NT_UNKNOWN)

	def addLocals(self, name, node):
		self.locals[name] = node

	def batchRemoveLocals(self, names):
		for name in names:
			if name and name in self.locals:
				del self.locals[name]

	def __repr__(self):
		msg = '\n'.join(['%s:  %s' % (name, NT_DUMP[sc]) for name, sc in self.lookup.iteritems()])
		msg = '%s\n%s' % (msg, self.locals)
		return msg


class BuilderScope(object):
	"""modify By inner module compiler.symbols"""

	def __init__(self, type, name=''):
		self.type = type
		self.name = name
		self.defs = {}
		self.uses = {}
		self.globalvars = {}
		self.argvars = {}
		self.freevars = {}
		self.cellvars = {}
		self.child_scope = []
		self.nested = False
		self.generator = False

		self.locals = {}

	def __repr__(self):
		return """defs: %s\nuses: %s\nglobalvars: %s\nargvars: %s\nfreevars: %s \ncellvars: %s
		""" % (self.defs, self.uses, self.globalvars, self.argvars, self.freevars, self.cellvars)

	def dump(self):
		names = self.defs.keys() + self.uses.keys() + self.globalvars.keys()
		lookup = {name : self.identify(name) for name in names}
		return Scope(self.type, self.name, lookup, self.locals)

	def addDef(self, name):
		self.defs[name] = 1

	def addUse(self, name):
		self.uses[name] = 1

	def addLocals(self, name, node):
		if name:
			self.locals[name] = node

	def batchRemoveLocals(self, names):
		map(self.removeLocals, names)
	
	def removeLocals(self, name):
		if name and name in self.locals:
			del self.locals[name]
	
	def addGlobal(self, name):
		if name in self.uses or name in self.defs:
			pass
		if name in self.argvars:
			raise SyntaxError, "%s in %s is global and parameter" % (name, self.name)
		self.globalvars[name] = 1

	def addArgvars(self, name):
		self.defs[name] = 1
		self.argvars[name] = 1

	def getNames(self):
		d = {}
		imap(d.update, (self.defs, self.uses, self.globalvars))
		return d.keys()

	def addChildScope(self, scope):
		self.child_scope.append(scope)

	def addFreevars(self, names):
		child_globals = []
		for name in names:
			sc = self.identify(name)
			if self.nested:
				if sc == NT_UNKNOWN or sc == NT_FREE or self.type == ST_CLASS:
					self.freevars[name] = 1
				elif sc == NT_GLOBAL_IMPLICIT:
					child_globals.append(name)
				elif self.type == ST_FUNCTION and sc == NT_LOCAL:
					self.cellvars[name] = 1
				elif sc != NT_CELL:
					child_globals.append(name)
			else:
				if sc == NT_LOCAL:
					self.cellvars[name] = 1
				elif sc != NT_CELL:
					child_globals.append(name)
		return child_globals

	def identify(self, name):
		if name in self.globalvars:
			return NT_GLOBAL_EXPLICIT
		if name in self.cellvars:
			return NT_CELL
		if name in self.defs:
			return NT_LOCAL
		if self.nested and (name in self.freevars or name in self.uses):
			return NT_FREE
		if self.nested:
			return NT_UNKNOWN
		else:
			return NT_GLOBAL_IMPLICIT

	def getFreeVars(self):
		if not self.nested:
			return ()
		freevars = {}
		freevars.update(self.freevars)
		for name in self.uses.keys():
			if name not in self.defs and name not in self.globalvars:
				freevars[name] = 1
		return freevars.keys()

	def getCellVars(self):
		return self.cellvars.keys()

	def updateFreevars(self):
		for child in self.child_scope:
			freevars = child.getFreeVars()
			globalvars = self.addFreevars(freevars)
			for name in globalvars:
				child.forceGlobal(name)

	def forceGlobal(self, name):
		self.globalvars[name] = 1
		if name in self.freevars:
			del self.freevars[name]
		for child in self.child_scope:
			if child.identify(name) == NT_FREE:
				child.forceGlobal(name)


class IContext(object):
	def __init__(self, rootpath, relpath):
		self.__rootpath__ = rootpath
		self.__relpath__ = relpath


class TokenizeContext(IContext):
	def __init__(self, rootpath, relpath):
		super(TokenizeContext, self).__init__(rootpath, relpath)


class AstContext(IContext):
	"""包括作用域和当前分析node属于哪个function、哪个class"""

	def __init__(self, rootpath, relpath, name):
		super(AstContext, self).__init__(rootpath, relpath)
		self.__name__ = name

		self.scopes = []

	def load(self, name, lazy=False):
		return None

	@property
	def scope(self):
		return self.scopes[-1]
