# -*- coding:utf-8 -*-

"""
和Python2的源码Import实现一致，根据import内容返回对应的AST Node
"""

from finder import AttributeFinder


class RoutinePath(object):
	def addRoutine(self, routine, paths):
		pass

	def routine(self, path):
		pass


class Module(object):
	"""通过.可获取"""
	def __init__(self, name, file=None, path=None):
		super(Module, self).__init__()
		self.__name__ = name
		self.__file__ = file
		self.__path__ = path

		self.node = node
		self.locals = {}

	def _loadLocals(self):
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
			raise
		else:
			pass
		finally:
			pass

	def getParent(self):
		pass

	def loadNext(self):
		pass

	def ensureFromlist(self):
		pass








class ImportFinder(object):
	"""模拟import, 返回对应的astNode"""

	class Module(object):
		def __init__(self, name, path, type, node=None):
			self.name = name
			self.path = path
			self.type = type
			self.node = None

		def __repr__(self):
			return 'Module(name: %s, path: %s' % (self.name, self.path)

	def __init__(self, root, path):
		super(ImportFinder, self).__init__()
		self.root = root
		self.path = [root]
		
		path and self.path.extend(path)

	def findImportNode(self, module, pdir):
		caller = ImportFinder.Module('', pdir, imp.PY_SOURCE)
		return self._loadImport(module, caller)

	def findImportFromNode(self, module, fromlist, level, pdir):
		if not isinstance(fromlist, (list, tuple)):
			fromlist = [fromlist]

		caller = ImportFinder.Module('', pdir, imp.PY_SOURCE)
		return self._loadImport(module, caller, fromlist=fromlist, level=level)

	def _loadImport(self, name, caller, fromlist=None, level=-1):
		find_paths = ["/".join(caller.path.split("/")[:-level])] if level > 0 else [caller.path] if level == 0 else None
		try:
			split_path = name.split('.')
			pkg, tail = split_path[0], split_path[1:]
			module = self._findImport(pkg, find_paths)

			if tail:
				pkg, find_paths = tail[-1], [os.path.join(module.path, *tail[:-1])]
				module = self._findImport(pkg, find_paths)
		except ImportError as e:
			print 'ImportError: %s' % e
			return None
		else:
			node = self._getAstNode(module)
			if fromlist:
				return self._enusreFromlist(node, module, fromlist)
			return {name: node}

	def _findImport(self, name, find_paths=None):
		if not find_paths:
			find_paths = self.path

		_, path, (_, _, type) = imp.find_module(name, find_paths)
		return ImportFinder.Module(name, path, type)

	def _getAstNode(self, module):
		if module.type == imp.PY_SOURCE:
			return ast.parse(open(module.path).read())
		elif module.type == imp.PKG_DIRECTORY:
			module = self._findImport('__init__', [module.path])
			return ast.parse(open(module.path).read())

		return None

	def _enusreFromlist(self, node, module, fromlist):
		importall = '*' in fromlist
		finder = AttributeFinder(fromlist, importall)
		result = finder.find(node)

		if module.type == imp.PKG_DIRECTORY:
			remains = [i for i in fromlist if i not in result]
			if not importall and remains:
				for remain in remains:
					remain_module = self._loadImport(remain, module, level=0)
					if remain_module and remain in remain_module:
						result[remain] = remain_module[remain]
		
		return result
