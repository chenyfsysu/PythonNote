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
from objects import ObjectAllocator, Object
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
			node.assignConst(tuple((elt.val for elt in node.elts)))

	def postvisit_Set(self, node):
		if not isinstance(node.ctx, ast.Load):
			return
		if self._allEltsConstant(node.elts):
			node.assignConst({elt.val for elt in node.elts})

	def postvisit_List(self, node):
		if not isinstance(node.ctx, ast.Load):
			return
		if self._allEltsConstant(node.elts):
			node.assignConst([elt.val for elt in node.elts])

	def postvisit_Dict(self, node):
		if self._allEltsConstant(node.keys) and self._allEltsConstant(node.values):
			node.assignConst({k.val: v.val for k, v in izip(node.keys, node.values)})

	def _allEltsConstant(self, elts):
		return all((elt.is_constant for elt in elts))


class AstDefMixin(IVisitor):
	def storeDef(self):
		pass

	def visitDefinition(self, node):
		self.context.storeAll(ObjectAllocator.allocate(node))

	def postvisit_Assign(self, node):
		return node

	def postvisit_AugAssign(self, node):
		if isinstance(node.target, ast.Name):
			name = node.target.id
		return node

	def postvisit_For(self, node):
		return node

	def postvisit_Import(self, node):
		return node

	def postvisit_ImportFrom(self, node):
		return node

	def postvisit_Delete(self, node, context):
		# locals_attr = self.context.locals
		# for target in node.targets:
		# 	if isinstance(target, ast.Name) and target.id in locals_attr:
		# 		del locals_attr[target.id]
		return node


class AstScopeMixin(IVisitor):

	def enterChildScope(self, node, name=''):
		scope = AstScope(name)
		self.context.scopes.append(scope)
		node.setScope(scope)
		node = self.genericWalk(node)
		self.context.scopes.pop()

		return node

	def fullvisit_Module(self, node):
		return self.enterChildScope(node)

	def fullvisit_ClassDef(self, node):
		return self.enterChildScope(node)

	def fullvisit_FunctionDef(self, node):
		print '11111111', node.scope
		return self.enterChildScope(node)

	def fullvisit_Lambda(self, node):
		return self.enterChildScope(node)

	def fullvisit_GeneratorExp(self, node):
		return self.enterChildScope(node)

	def previsit_ClassDef(self, node):
		pass

	def previsit_Name(self, node):
		if isinstance(node.ctx, ast.Store):
			self.context.scope.addDef(node.id)
		else:
			self.context.scope.addUse(node.id)


class TokenizeWalker(HostVisitor):
	TokenMapping = {
		tokenize.COMMENT: 'Comment'
	}

	def __init__(self, rootpath):
		super(TokenizeWalker, self).__init__(rootpath)
		self.context = None

	def walk(self, fullpath, relpath):
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


class VisitWalker(AstHostVisitor, AstConstantMixin, AstDefMixin):
	def __init__(self, rootpath):
		super(VisitWalker, self).__init__(rootpath)
		self.context = None
		self.selfvisitors = defaultdict(list)
		self.register(self)

	def walk(self, fullpath, relpath):
		self.notifyVisitFile(fullpath, relpath)
		self.context = AstContext(self.rootpath, relpath, '__main__')

		ModuleLoader().setPath(['entities', 'entities/client', 'entities/common'])
		tree = ModuleLoader().reloadRoot(fullpath)
		tree = self._walk(tree)

		self.notifyLeaveFile(fullpath, relpath)
		return tree

	def _walk(self, node, parent=None):
		parent and node.__postinit__(parent)

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


class TransformWalker(VisitWalker):
	def __init__(self, rootpath):
		super(TransformWalker, self).__init__(rootpath)

	def _walk(self, node, parent=None):
		parent and node.__postinit__(parent)

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
