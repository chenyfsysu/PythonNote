# -*- coding:utf-8 -*-
"""
1) 2018.3.6: 需要提供一个获取import的文件路径的功能
"""

import os
import ast
import imp
import utils
import itertools

from objects import ObjectAllocator


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
		self.store(node)

	def visit_FunctionDef(self, node):
		self.store(node)

	def visit_Assign(self, node):
		self.store(node)

	def visit_Delete(self, node):
		for target in node.targets:
			if isinstance(target, ast.Name) and target.id in self.attrs:
				del self.attrs[target.id]

	def store(self, node):
		if self.predicate and not self.predicate(node):
			return

		attrs = ObjectAllocator.allocate(node)
		attrs = {name: value for name, value in attrs.iteritems() if self.findall or name in self.findattrs}
		self.attrs.update(attrs)


if __name__ == '__main__':
	node = ast.parse(open('../test.py').read())
	finder = AttributeFinder(['A'], True)
	print finder.find(node)

	# pname = os.path.dirname('')
	# finder = ImportFinder(pname, None)
	# print finder.findImportNode('pkg.mod', pname)
	# print '*' * 100
	# print finder.findImportFromNode('pkg', ['A'],  -1, pname)
