# -*- coding:utf-8 -*-

from const import NT_LOCAL, NT_GLOBAL_IMPLICIT, NT_GLOBAL_EXPLICIT, NT_FREE, NT_CELL, NT_UNKNOWN, NT_DUMP
import ast


class PyScope(object):
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

	def cells(self):
		return [name for name, val in self.lookup.iteritems() if val == NT_CELL]

	def __repr__(self):
		msg = '\n'.join(['%s:  %s' % (name, NT_DUMP[sc]) for name, sc in self.lookup.iteritems()])
		msg = '%s\n%s' % (msg, self.locals)
		return msg



class PyFrame(object):
	def __init__(self, locals, globals, builtins=None, cells=None):
		self.f_locals = locals		
		self.f_globals = globals or {}
		self.f_builtins = builtins or {}
		self.f_cells = cells or {}

	def loadName(self, name):
		return self.f_locals.get(name, None)

	def loadGlobal(self, name):
		return self.f_globals.get(name, None)

	def loadDeref(self, name):
		return self.f_cells.get(name, None)


class PyClass(object):
	pass


class PyCell(object):
	pass


class PyFunction(object):
	def __init__(self, closure, defaults, globals):
		self.is_bad = False # 如果有不能解析的内容，则会设置为is_bad

		self.func_closure = closure
		self.func_defaults = defaults
		self.func_globals = globals

	def setBad(self, bad):
		self.is_bad = bad


class PyMethod(object):
	def __init__(self, inst, func, cls):
		self.im_self = inst
		self.im_func = func
		self.im_class = cls
