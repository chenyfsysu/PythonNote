# -*- coding:utf-8 -*-
"""
1) 2018.3.6: 需要提供一个获取import的文件路径的功能
2) 2018.3.29: 现在要考虑rely module怎么处理
"""

import os
import ast
import imp
import utils

import nodes
from context import BuilderScope
from itertools import imap
from const import ST_MODULE, ST_CLASS, ST_FUNCTION, ST_GENERATOR


class ModuleBuilder(object):
	def __init__(self):
		self.scopes = []
		self.lookups = []
		self.is_rely = True

	def pushScope(self, node, type, name=''):
		scope = BuilderScope(type, name)
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

	def build(self, node, fqname, file, path, is_rely=True):
		self.is_rely = is_rely
		node.__preinit__(fqname, file, path)
		self.visit(node)
		self.dump()
		self.scopes = []

	def dump(self):
		for node, scope in self.lookups:
			node.scope = scope.dump()
		self.lookups = []

	def visit(self, node, parent=None):
		parent and node.__preinit__(parent)

		visitor = getattr(self, 'visit_%s' % node.__class__.__name__, self.genricVisit)
		visitor(node)

		self.is_rely and node.__postinit__()

	def genricVisit(self, node):
		for field in node._fields:
			cnode = getattr(node, field)
			if isinstance(cnode, list):
				for item in cnode:
					if isinstance(item, ast.AST):
						self.visit(item, parent=node)
			elif isinstance(cnode, ast.AST):
				self.visit(cnode, parent=node)

		return node

	def visit_Module(self, node):
		self.pushScope(node, ST_MODULE)
		self.genricVisit(node)
		self.popScope()

	def visit_ClassDef(self, node):
		self.pushScope(node, ST_CLASS)
		for body in node.body:
			self.visit(body, parent=node)

		scope, parent = self.scope, self.parentScope
		if parent.nested or parent.type == ST_FUNCTION:
			scope.nested = True
		scope.updateFreevars()
		self.popScope()

		for base in node.bases:
			self.visit(base, parent=node)
			base.n_use_pscope = True

		for deco in node.decorator_list:
			self.visit(deco, parent=node)
			deco.n_use_pscope = True

		self.scope.addDef(node.name)
		self.enableStaticLocals() and self.scope.addLocals(node.name, node)

	def visit_FunctionDef(self, node):
		self.pushScope(node, ST_FUNCTION)
		self.visit(node.args, parent=node)
		for body in node.body:
			self.visit(body, parent=node)

		scope, parent = self.scope, self.parentScope
		if parent.nested or parent.type == ST_FUNCTION:
			scope.nested = True
		scope.updateFreevars()
		self.popScope()

		for deco in node.decorator_list:
			self.visit(deco, parent=node)
			deco.n_use_pscope = True
	
		for n in node.args.defaults:
			self.visit(n, parent=node.args)
			n.n_use_pscope = True

		self.scope.addDef(node.name)
		self.enableStaticLocals() and self.scope.addLocals(node.name, node)

	def visit_GeneratorExp(self, node):
		self.pushScope(node, ST_GENERATOR)
		self.genricVisit(node)
		scope, parent = self.scope, self.parentScope
		if parent.nested or parent.type in (ST_FUNCTION, ST_GENERATOR):
			scope.nested = True
		scope.updateFreevars()
		self.popScope()

	def visit_Lambda(self, node):
		self.pushScope(node, ST_FUNCTION)
		self.visit(node.args, parent=node)
		self.visit(node.body, parent=node)

		scope, parent = self.scope, self.parentScope
		if parent.nested or parent.type == ST_FUNCTION:
			scope.nested = True
		scope.updateFreevars()
		self.popScope()

		for n in node.args.defaults:
			self.visit(n, parent=node.args)
			n.n_use_pscope = True

	def visit_arguments(self, node):
		for args in node.args:
			self.scope.addArgvars(args.id)
		node.vararg and self.scope.addArgvars(node.vararg)
		node.kwarg and self.scope.addArgvars(node.kwarg)

	def visit_ImportFrom(self, node):
		for alias in node.names:
			name, asname = alias.name, alias.asname
			if name != "*":
				self.scope.addDef(asname or name)
				self.enableStaticLocals() and self.scope.addLocals(asname or name, node)

	def visit_Import(self, node):
		for alias in node.names:
			name, asname = alias.name, alias.asname
			name = name[:name.find('.')] if '.' in name else name
			self.scope.addDef(asname or name)
			self.enableStaticLocals() and self.scope.addLocals(asname or name, node)

	def visit_Global(self, node):
		map(self.scope.addGlobal, node.names)

	def visit_Name(self, node):
		if isinstance(node.ctx, ast.Load):
			self.scope.addUse(node.id)
		else:
			self.scope.addDef(node.id)

	def visit_Assign(self, node):
		if not self.enableStaticLocals():
			return self.genricVisit(node)

		scope = self.scope
		for target in node.targets:
			for name in utils.get_names(target, pure_only=False) or []:
				scope.addLocals(name, node)
		self.genricVisit(node)

	def visit_AugAssign(self, node):
		if isinstance(node.target, ast.Name):
			self.scope.addLocals(node.target.id, node)
		self.genricVisit(node)

	def visit_Delete(self, node):
		for target in node.targets:
			self.scope.batchRemoveLocals(utils.get_names(target, pure_only=False) or [])
		self.genricVisit(node)

	def enableStaticLocals(self):
		return self.is_rely and self.scope.type in (ST_MODULE, ST_CLASS)

	 
class AttributeFinder(ast.NodeVisitor):

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


if __name__ == '__main__':
	node = ast.parse(open('../test.py').read())
	# finder = AttributeFinder(['A'], True)
	# print finder.find(node)

	finder = ModuleBuilder()
	finder.build(node, is_rely=True)
	print node.scope
	# print node.body[0].body[1].scope.show()
