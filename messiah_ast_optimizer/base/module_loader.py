# -*- coding:utf-8 -*-

"""
和Python2的源码Import实现一致，根据import内容返回对应的AST Node
"""

import os
from finder import AttributeFinder


class RoutinePath(object):
	def addRoutine(self, routine, paths):
		pass

	def routine(self, path):
		pass


class Module(object):
	"""通过.可获取"""
	def __init__(self, name, file, path=False, node=None):
		super(Module, self).__init__()
		self.name = name
		self.file = file
		self.path = path

		self.node = node
		self.locals = {}

	def getParent(self):
		return os.path.dirname(self.file)

	def _loadLocals(self):
		if not self.node:
			return
		self.locals = {}

	def load(self, name):
		pass

	def __getattr__(self, name):
		pass


class ModuleLoader(object):
	def __init__(self, path, routine_paths=None):
		self.path = path or []
		self.routine_paths = routine_paths
		self.modules = {}

	def load(self, caller, importdef):
		pass

	def loadModuleLevel(self, name, caller, fromlist, level=1):
		try:
			pass
		except ImportError:
			print '111'
		else:
			pass
		finally:
			pass

	def _loadModuleLevel(self, name, caller, level=-1):
		parent = self._loadParent(caller, level=level)

		# names = name.split('.')
		# head = self._loadNext(name, caller, parent)


	def _loadParent(self, caller, level):
		if not caller or level == 0:
			return None

		pname, ppath = caller.name, caller.getParent()
		if level >= 1:
			if caller.path:
				level -= 1
			if level:
				pname = '.'.join(pname.split('.')[:-level])
				ppath = os.path.abspath('%s%s%s'(pname, os.path.sep, '.' * level))
		else:
			pname = pname if caller.path else pname[:pname.rfind('.')] if '.' in pname else None

		if not pname:
			return None

		if pname in self.modules:
			return self.modules[pname]

		return imp._loadModule(pname, '__init__', [ppath], package=True)

	def _loadNext(self):
		pass

	def _loadModule(self, name, fullname, path=None, package=False):
		path = path or self.path
		fp, pathname, desc = imp.find_module(name, path)
		_, _, typ = desc

		if typ == imp.PKG_DIRECTORY:
			pathname, mod = self._loadPackage(pathname)
		elif typ == imp.imp.PY_SOURCE:
			pass


	def _loadPackage(self, fullname, path):
		pkg = imp.find_module('__init__', [path])
