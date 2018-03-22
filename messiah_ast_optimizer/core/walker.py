# -*- coding:utf-8 -*-

import ast
import utils
import const

from collections import defaultdict
from base import NodeVisitor
from context import Context, Frame, Namespace
from objects import ObjectAllocator, Object


class ContextVisitor(NodeVisitor):

	def visitDefinitionBlock(self, node):
		context = self.context
		context.frames.append(Frame.create(node))
		context.locals_stack.append(Namespace())
		
		node = self.visit(node)
		definitions = ObjectAllocator.allocate(node)
		context.storeAll(definitions)
		context.frames.pop()
		context.locals_stack.pop()

		return node

	def visitClosureBlock(self, node):
		self.context.locals_stack.append(Namespace())
		node = self.visit(node)
		self.context.locals_stack.pop()

		return node

	def visitDefinition(self, node):
		self.context.storeAll(ObjectAllocator.allocate(node))

	def fullvisit_Module(self, node):
		self.context.frames.append(Frame.create(node))
		self.context.locals_stack.append(Namespace())
		return self.visit(node)

	def fullvisit_ClassDef(self, node):
		return self.visitDefinitionBlock(node)

	def fullvisit_FunctionDef(self, node):
		return self.visitDefinitionBlock(node)

	def fullvisit_DictComp(self, node):
		return self.visitClosureBlock(node)

	def fullvisit_ListComp(self, node):
		return self.visitClosureBlock(node)

	def fullvisit_SetComp(self, node): 
		return self.visitClosureBlock(node)

	def fullvisit_GeneratorExp(self, node):
		return self.visitClosureBlock(node)

	def fullvisit_Lambda(self, node):
		return  self.visitClosureBlock(node)

	def visit_Assign(self, node):
		self.visitDefinition(node)
		return node

	def visit_AugAssign(self, node):
		if isinstance(node.target, ast.Name):
			name = node.target.id
			self.context.store(name, Object(name, None))
		return node

	def visit_For(self, node):
		return node

	def visit_Import(self, node):
		self.visitDefinition(node)
		return node

	def visit_ImportFrom(self, node):
		self.visitDefinition(node)
		return node

	def visit_Delete(self, node):
		locals_attr = self.context.locals
		for target in node.targets:
			if isinstance(target, ast.Name) and target.id in locals_attr:
				del locals_attr[target.id]
		return node


class Walker(object):
	def __init__(self):
		self.visitors = defaultdict(list)
		self.fullvisitors = defaultdict(list)

	def activate(self, visitors):
		map(self.register, visitors)

	def register(self, visitor):
		for func in visitor._visitors:
			key = func[6:]
			method = getattr(visitor, func)
			self.visitors[key].append(method)

		for func in visitor._fullvisitors:
			key = func[10:]
			method = getattr(visitor, func)
			self.fullvisitors[key].append(method)

	def walk(self):
		raise NotImplementedError

	def dispatch(self, key, *args):
		if key not in self.visitors:
			return

		for visitor in self.visitors:
			visitor(*args)

	def dispatchFull(self, key, *args):
		if key not in self.fullvisitors:
			return

		for visitor in self.fullvisitors:
			visitor(*args)


class TokenizeWalker(Walker):
	TokenMapping = {
		tokenize.COMMENT: 'Comment'
	}

	def __init__(self):
		self.tokenizers = tokenizers

	def walk(self, realine):
		tokenize.tokenize(readline, self.tokeneater)

	def tokeneater(self, type, token, srow_scol, erow_ecol, line):
		if type not in self.TokenMapping:
			return
		key = self.TokenMapping[type]
		self.dispatch(key, token, srow_scol, erow_ecol, line)


class VisitWalker(Walker, ContextVisitor):
	def __init__(self):
		super(VisitWalker, self).__init__()
		self.selfvisitors = defaultdict(list)

	def registerSelf(self):
		for func in visitor._visitors:
			key = func[6:]
			method = getattr(visitor, func)
			self.selfvisitors[key].append(method)

		for func in visitor._fullvisitors:
			key = func[10:]
			method = getattr(visitor, func)
			self.fullvisitors[key].append(method)

	def walk(self, node):
		pass

	def visit(self, node):
		key = node.__class__.__name__
		if key in self.fullvisitors:
			self.dispatchFull(key)
		else:
			self.genericVisit(node)

		self.dispatch(node)

		if key in self.selfvisitors:
			for visitor in self.selfvisitors[key]:
				visitor(self, node)

		return node

	def genericVisit(self, node):
		for field, value in ast.iter_fields(node):
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
			elif isinstance(value, ast.AST):
				self.visit(value)

		return node


class TransformWalker(VisitWalker):
	def __init__(self):
		super(TransformWalker, self).__init__()

	def visit(self, node):
		key = node.__class__.__name__
		if key in self._fullvisitors:
			visitors = self._fullvisitors[key]
			for visitor in visitors:
				node = visitor(self, node)
		else:
			node = self.generalVisit(node)

		if key in self.visit_steps:
			for step in self.visit_steps[key]:
				node = step.transform(key, node, self.context)

		if key in self._selfvisitors:
			for visitor in self._selfvisitors[key]:
				visitor(self, node)

		return node

	def generalVisit(self, node):
		for field, old_value in ast.iter_fields(node):
			old_value = getattr(node, field, None)
			if isinstance(old_value, list):
				new_values = []
				for value in old_value:
					if isinstance(value, ast.AST):
						value = self.visit(value)
						if value is None:
							continue
						elif not isinstance(value, ast.AST):
							new_values.extend(value)
							continue
					new_values.append(value)
				old_value[:] = new_values
			elif isinstance(old_value, ast.AST):
				new_node = self.visit(old_value)
				if new_node is None:
					delattr(node, field)
				else:
					setattr(node, field, new_node)
		return node
