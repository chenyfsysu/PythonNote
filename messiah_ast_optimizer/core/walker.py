# -*- coding:utf-8 -*-

import ast
import utils
import const
import tokenize
import nodes

from itertools import imap, izip
from collections import defaultdict
from base import AstHostVisitor, HostVisitor, IVisitor
from context import TokenizeContext, AstContext
from module_loader import ModuleLoader


class AstConstantMixin(IVisitor):
	def postvisit_Num(self, node):
		node.assignConst(node.n)

	def postvisit_Str(self, node):
		node.assignConst(node.s)

	def postvisit_Name(self, node):
		node.id in const.BUILTIN_NAME and node.assignConst(utils.get_pure_constant(node))

	def postvisit_Tuple(self, node):
		if not isinstance(node.ctx, ast.Load):
			return
		if self._allEltsConstant(node.elts):
			node.assignConst(tuple((elt.n_val for elt in node.elts)))

	def postvisit_Set(self, node):
		if self._allEltsConstant(node.elts):
			node.assignConst({elt.n_val for elt in node.elts})

	def postvisit_List(self, node):
		if not isinstance(node.ctx, ast.Load):
			return
		if self._allEltsConstant(node.elts):
			node.assignConst([elt.n_val for elt in node.elts])

	def postvisit_Dict(self, node):
		if self._allEltsConstant(node.keys) and self._allEltsConstant(node.values):
			node.assignConst({k.n_val: v.n_val for k, v in izip(node.keys, node.values)})

	def _allEltsConstant(self, elts):
		return all((elt.n_isconstant for elt in elts))


class AstScopeMixin(IVisitor):
	def __init__(self):
		self.scopes = []

	@property
	def scope(self):
		return self.scopes[-1]

	def enterChildScope(self, node, name=''):
		self.scopes.append(node.scope)
		node = self.genericWalk(node)
		self.scopes.pop()

		return node

	def fullvisit_Module(self, node):
		return self.enterChildScope(node)

	def fullvisit_ClassDef(self, node):
		return self.enterChildScope(node)

	def fullvisit_FunctionDef(self, node):
		return self.enterChildScope(node)

	def fullvisit_Lambda(self, node):
		return self.enterChildScope(node)

	def fullvisit_GeneratorExp(self, node):
		return self.enterChildScope(node)

	def postvisit_ClassDef(self, node):
		self.scope.addLocals(node.name, node)

	def postvisit_FunctionDef(self, node):
		self.scope.addLocals(node.name, node)

	def postvisit_Assign(self, node):
		scope = self.scope
		for target in node.targets:
			for name in utils.get_names(target, pure_only=False) or []:
				scope.addLocals(name, node)

	def postvisit_AugAssign(self, node):
		if isinstance(node.target, ast.Name):
			self.scope.addLocals(node.target.id, node)
		return node

	def postvisit_Import(self, node):
		scope = self.scope
		for alias in node.names:
			name, asname = alias.name, alias.asname
			if name != "*":
				scope.addLocals(name, node)
		return node

	def postvisit_ImportFrom(self, node):
		scope = self.scope
		for alias in node.names:
			name, asname = alias.name, alias.asname
			name = name[:name.find('.')] if '.' in name else name
			scope.addLocals(asname or name, node)
		return node

	def postvisit_Delete(self, node):
		for target in node.targets:
			self.scope.batchRemoveLocals(utils.get_names(target, pure_only=False) or [])
		return node


class TokenizeWalker(HostVisitor):
	TokenMapping = {
		tokenize.COMMENT: 'Comment'
	}

	def __init__(self, rootpath):
		super(TokenizeWalker, self).__init__(rootpath)
		self.context = None

	def walk(self, fullpath, relpath):
		print '>>>>>>>>>tokenize: %s' % relpath
		self.notifyVisitFile(fullpath, relpath)

		self.context = TokenizeContext(fullpath, relpath)
		readline = open(fullpath).readline
		tokenize.tokenize(readline, self.tokeneater)

		self.notifyLeaveFile(fullpath, relpath)

	def tokeneater(self, type, token, srow_scol, erow_ecol, line):
		if type not in self.TokenMapping:
			return
		key = self.TokenMapping[type]
		self.visit(key, token, srow_scol, erow_ecol, line, self.context)


class VisitWalker(AstHostVisitor, AstConstantMixin, AstScopeMixin):
	def __init__(self, rootpath):
		super(VisitWalker, self).__init__(rootpath)
		AstScopeMixin.__init__(self)
		self.context = None
		self.selfvisitors = defaultdict(list)
		self.register(self)

	def walk(self, fullpath, relpath):
		self.notifyVisitFile(fullpath, relpath)
		self.context = AstContext(self.rootpath, relpath, '__main__')

		ModuleLoader().setPath(['Python/entities/client', 'Pythonentities/common', 'Python/engine'])
		tree = ModuleLoader().reloadRoot(fullpath)
		tree = self._walk(tree)

		self.notifyLeaveFile(fullpath, relpath)
		return tree

	def _walk(self, node, parent=None):
		key = node.__class__.__name__
		if hasattr(self, 'fullvisit_%s' % key):
			self.fullvisit(node)
		else:
			self.genericWalk(node)

		self.previsit(key, node)
		self.visit(key, node, self.context)
		self.postvisit(key, node)

		return node

	def genericWalk(self, node):
		for field in node._fields:
			cnode = getattr(node, field)
			if isinstance(cnode, list):
				for item in cnode:
					if isinstance(item, ast.AST):
						self._walk(item, parent=node)
			elif isinstance(cnode, ast.AST):
				self._walk(cnode, parent=node)

		return node

	def postvisit(self, key, node):
		node.__postinit__()
		return super(VisitWalker, self).postvisit(key, node)


class TransformWalker(VisitWalker):
	def __init__(self, rootpath):
		super(TransformWalker, self).__init__(rootpath)

	def _walk(self, node, parent=None):
		key = node.__class__.__name__
		if hasattr(self, 'fullvisit_%s' % key):
			node = self.fullvisit(node)
		else:
			node = self.genericWalk(node)

		self.previsit(key, node)
		node = self.visit(key, node, self.context)
		self.postvisit(key, node)
		return node

	def genericWalk(self, node):
		for field in node._fields:
			old_value = getattr(node, field)
			if isinstance(old_value, list):
				new_values = []
				for value in old_value:
					if isinstance(value, ast.AST):
						value = self._walk(value, node)
						if value is None:
							continue
						elif not isinstance(value, ast.AST):
							new_values.extend(value)
							continue
					new_values.append(value)
				old_value[:] = new_values
			elif isinstance(old_value, ast.AST):
				new_node = self._walk(old_value, node)
				if new_node is None:
					delattr(node, field)
				else:
					setattr(node, field, new_node)
		return node
