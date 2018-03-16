# -*- coding:utf-8 -*-
"""
1) 2018.3.6: 需要提供一个获取import的文件路径的功能
"""

import os
import ast
import imp
import utils
import itertools


class GlobalFinder(object):
	pass


class AttributeFinder(ast.NodeVisitor):
	"""
	1）不能处理获取import的内容
	2）赋值不支持嵌套嵌套赋值， a, (b, (c, d)), e = [1, (2, (3, 4)), 5]
	3）简单的展开a, b, c = 1, 2, 3, 4支持
	4) 赋值支持多个target，如a=b=c
	"""
	def __init__(self, findattrs=None, findall=False, predicate=None):
		"""self.findall or key in self.findattrs or self.predicate and self.predicate(value)"""

		self.findattrs = findattrs or []
		self.findall = findall
		self.predicate = predicate

		self.attrs = {}

	def find(self, node):
		self.attrs = {}

		key = node.__class__.__name__
		func = getattr(self, 'find_%s' % key, None)
		func and func(node)

		return self.attrs

	def find_Module(self, node):
		for item in node.body:
			self.visit(item)

	def find_ClassDef(self, node):
		for item in node.body:
			self.visit(item)

	def visit(self, node):
		key = node.__class__.__name__
		func = getattr(self, 'visit_%s' % key, None)
		func and func(node)

	def visit_ClassDef(self, node):
		self.addAttribute(node.name, node)

	def visit_FunctionDef(self, node):
		self.addAttribute(node.name, node)

	def visit_Assign(self, node):
		for target in node.targets:
			if isinstance(target, ast.Name):
				self.addAttribute(target.id, node.value)
			elif all(isinstance(t, ast.Name) for t in target.elts):
				for elt, value in itertools.izip(target.elts, node.value.elts):
					self.addAttribute(elt.id, value)

	def addAttribute(self, key, value):
		if self.findall or key in self.findattrs or self.predicate and self.predicate(value):
			self.attrs[key] = value


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


if __name__ == '__main__':
	# node = ast.parse(open('../test.py').read())
	# finder = AttributeFinder(['A'], True)
	# print finder.find(node)

	pname = os.path.dirname('')
	finder = ImportFinder(pname, None)
	print finder.findImportNode('pkg.mod', pname)
	print '*' * 100
	print finder.findImportFromNode('pkg', ['A'],  -1, pname)
