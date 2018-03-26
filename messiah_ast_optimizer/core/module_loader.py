# -*- coding:utf-8 -*-

"""
和Python2的源码Import实现一致，根据import内容返回对应的AST Node
Module对象Attribute对象的返回类型不一样，丢
"""

import os
import sys
import imp
import ast
import utils
from finder import AttributeFinder


class Singleton(object):
	_instance = None
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(Singleton, cls).__new__(cls)
			cls._instance.init(*args, **kwargs)
		return cls._instance  


class ModuleLoader(Singleton):
	"""modulefinder以兼容ast类型的import, 暂时不支持import *"""

	def init(self):
		self.root = None
		self.path = []
		self.modules = {}

	def setPath(self, path):
		self.path = path

	def clear(self):
		self.root = None
		self.modules = {}

	def reloadRoot(self, fullpath):
		self.clear()

		tail = ''
		pname = self.getModuleName(fullpath)
		for i, name in enumerate(reversed(pname.split('.'))):
			if name == '__init__':
				continue
			tail = '.'.join([name, tail]) if tail else name
			path = None if i <= 0 else utils.get_parent_dir(fullpath, i)
			file = os.path.join(path, '__init__.py') if path else fullpath

			m = ast.parse(open(file).read())
			m.__postinit__(tail, file, path)
			self.modules[tail] = m

			if not tail:
				self.root = m

		return self.root

	def getModuleName(self, path):
		pname = ''
		for p in self.path:
			if path.startswith(p):
				name = os.path.relpath(path, p)
				if not pname or pname.startswith(pname):
					pname = name

		return '.'.join(pname.split(os.path.sep)).rstrip('.py')

	def load(self, name, fromlist=None, level=-1, caller=None):
		if not caller:
			caller = self.root
		try:
			if name in self.modules:
				m = self.modules[name]
			else:
				m = self.loadModuleLevel(name, fromlist, level, caller)
		except ImportError as e:
			print e
			m = None

		return m

	def loadModuleLevel(self, name, fromlist, level, caller):
		parent = self.getParent(caller, level=level)
		q, tail = self.loadHead(parent, name)
		m = self.loadTail(q, tail)

		if not fromlist:
			return m

		return self.ensureFromlist(m, fromlist)

	def getParent(self, caller, level=-1):
		if not caller or level == 0:
			return None
		pname = caller.name
		if level >= 1:
			if caller.path:
				level -= 1
			if level == 0:
				parent = self.modules[pname]
				assert parent is caller
				return parent
			if pname.count(".") < level:
				raise ImportError, "relative importpath too deep"
			pname = ".".join(pname.split(".")[:-level])
			parent = self.modules[pname]
			return parent
		if caller.path:
			parent = self.modules[pname]
			assert caller is parent
			return parent
		if '.' in pname:
			i = pname.rfind('.')
			pname = pname[:i]
			parent = self.modules[pname]
			assert parent.name == pname
			return parent
		return None

	def loadHead(self, parent, name):
		if '.' in name:
			i = name.find('.')
			head = name[:i]
			tail = name[i+1:]
		else:
			head = name
			tail = ""
		if parent:
			qname = "%s.%s" % (parent.name, head)
		else:
			qname = head
		q = self.importModule(head, qname, parent)
		if q:
			return q, tail
		if parent:
			qname = head
			parent = None
			q = self.importModule(head, qname, parent)
			if q:
				return q, tail
		raise ImportError, "No module named " + qname

	def loadTail(self, q, tail):
		m = q
		while tail:
			i = tail.find('.')
			if i < 0: i = len(tail)
			head, tail = tail[:i], tail[i+1:]
			mname = "%s.%s" % (m.__name__, head)
			m = self.importModule(head, mname, m)
			if not m:
				raise ImportError, "No module named " + mname
		return m

	def ensureFromlist(self, m, fromlist):
		if fromlist == '*':
			raise RuntimeError('Do not support importstar')

		if fromlist in m.locals:
			return m.locals[fromlist]

		if m.__path__:
			mname = "%s.%s" % (m.__name__, fromlist)
			sub = self.importModule(fromlist, mname, m)
			if not sub:
				raise ImportError, 'No module named ' + mname
			return sub
		else:
			raise ImportError, 'No attr named ' + fromlist

	def findAllSubmodules(self, m):
		if not m.__path__:
			return
		modules = {}
		for triple in imp.get_suffixes():
			suffixes.append(triple[0])
		for dir in m.__path__:
			try:
				names = os.listdir(dir)
			except os.error:
				continue
			for name in names:
				mod = None
				for suff in suffixes:
					n = len(suff)
					if name[-n:] == suff:
						mod = name[:-n]
						break
				if mod and mod != "__init__":
					modules[mod] = mod
		return modules.keys()

	def importModule(self, partname, fqname, parent):
		if fqname in self.modules:
			return self.modules[fqname]
		if parent and parent.__path__ is None:
			return None

		fp, pathname, stuff = self.findModule(partname, parent and parent.__path__, parent)
		try:
			m = self.loadModule(fqname, fp, pathname, stuff)
		finally:
			fp and fp.close()
		return m

	def findModule(self, name, path, parent=None):
		if parent is not None:
			fullname = parent.__name__+'.'+name
		else:
			fullname = name

		if path is None:
			if name in sys.builtin_module_names:
				return (None, None, ("", "", imp.C_BUILTIN))
			path = self.path
		return imp.find_module(name, path)


	def loadModule(self, fqname, fp, pathname, desc):
		suffix, mode, type = desc

		mod = path = None
		if type == imp.PKG_DIRECTORY:
			path = [pathname]
			fp, pathname, desc = self.findModule("__init__", path)
			mod = self.addModule(fp, fqname, pathname, path=path)
			fp and fp.close()

		elif type == imp.PY_SOURCE:
			mod = self.addModule(fp, fqname, pathname, path=path)

		return mod

	def addModule(self, fp, fqname, file, path=None):
		mod = ast.parse(fp.read())
		mod.__postinit__(fqname, file, path)
		finder = AttributeFinder(findall=True)
		mod.locals = finder.find(mod)
		self.modules[fqname] = mod

		return mod

	
if __name__ == '__main__':
	import nodes

	path = [
		'../entities/client',
		'../entities/common',
	]
	finder = ModuleLoader()
	finder.setPath(path)

	root = finder.reloadRoot('../entities/client/avtmembers/impPokemon.py')
	m = finder.load('pokemon', fromlist='pconst')
	print m
