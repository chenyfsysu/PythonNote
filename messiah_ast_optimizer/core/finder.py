# -*- coding:utf-8 -*-
"""
1) 2018.3.6: 需要提供一个获取import的文件路径的功能
"""

import os
import ast
import imp
import utils

from objects import ObjectAllocator
from context import FinderScope
from itertools import imap
from const import ST_MODULE, ST_CLASS, ST_FUNCTION, ST_GENERATOR


class ScopeFinder(ast.NodeVisitor):
	def __init__(self):
		self.scopes = []
		self.lookups = []

	def pushScope(self, node, type, name=''):
		scope = FinderScope(type, name)
		self.scopes and self.scope.addChildScope(scope)
		self.scopes.append(scope)
		self.lookups.append((node, scope))

	def popScope(self):
		self.scopes.pop()

	@property
	def scope(self):
		return self.scopes[-1]

	@property
	def parentScope(self):
		return self.scopes[-2]

	def find(self, node, name=''):
		self.visit(node)
		self.dump()
		self.scopes = []

	def dump(self):
		for node, scope in self.lookups:
			node.scope = scope.dump()
		self.lookups = []

	def visit_Module(self, node):
		self.pushScope(node, ST_MODULE)
		self.generic_visit(node)
		self.popScope()

	def visit_ClassDef(self, node):
		self.pushScope(node, ST_CLASS)
		for body in node.body:
			self.visit(body)

		scope, parent = self.scope, self.parentScope
		if parent.nested or parent.type == ST_FUNCTION:
			scope.nested = True
		scope.updateFreevars()
		self.popScope()

		self.scope.addDef(node.name)
		for base in node.bases:
			self.visit(base)

		for deco in node.decorator_list:
			self.visit(deco)

	def visit_FunctionDef(self, node):
		self.pushScope(node, ST_FUNCTION)
		self.visit(node.args)
		for body in node.body:
			self.visit(body)

		scope, parent = self.scope, self.parentScope
		if parent.nested or parent.type == ST_FUNCTION:
			scope.nested = True
		scope.updateFreevars()
		self.popScope()

		for deco in node.decorator_list:
			self.visit(deco)
	
		for n in node.args.defaults:
			self.visit(n)

		self.scope.addDef(node.name)

	def visit_GeneratorExp(self, node):
		self.pushScope(node, ST_GENERATOR)
		self.generic_visit(node)
		scope, parent = self.scope, self.parentScope
		if parent.nested or parent.type in (ST_FUNCTION, ST_GENERATOR):
			scope.nested = True
		scope.updateFreevars()
		self.popScope()

	def visit_Lambda(self, node):
		self.pushScope(node, ST_FUNCTION)
		self.visit(node.args)
		self.visit(node.body)

		scope, parent = self.scope, self.parentScope
		if parent.nested or parent.type == ST_FUNCTION:
			scope.nested = True
		scope.updateFreevars()
		self.popScope()

		for n in node.args.defaults:
			self.visit(n)

	def visit_arguments(self, node):
		for args in node.args:
			self.scope.addArgvars(args.id)
		node.vararg and self.scope.addArgvars(node.vararg)
		node.kwarg and self.scope.addArgvars(node.kwarg)

	def visit_ImportFrom(self, node):
		for alias in node.names:
			name, asname = alias.name, alias.asname
			name != "*" and self.scope.addDef(asname or name)

	def visit_Import(self, node):
		for alias in node.names:
			name, asname = alias.name, alias.asname
			name = name[:name.find('.')] if '.' in name else name
			self.scope.addDef(asname or name)

	def visit_Global(self, node):
		map(self.scope.addGlobal, node.names)

	def visit_Name(self, node):
		if isinstance(node.ctx, ast.Load):
			self.scope.addUse(node.id)
		else:
			self.scope.addDef(node.id)

	 
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
	# finder = AttributeFinder(['A'], True)
	# print finder.find(node)

	finder = ScopeFinder()
	finder.find(node)
	# print node.body[0].scope
	# print node.body[0].body[1].scope.show()
