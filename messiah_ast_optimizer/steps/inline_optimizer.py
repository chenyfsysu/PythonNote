# -*- coding:utf-8 -*-

from core.base import MessiahStepVisitor, MessiahStepTransformer, MessiahStepTokenizer, MessiahOptimizerStep

import ast


class Callee(object):
	__slots__ = ('name', 'func', 'is_method')

	def __init__(self, name, func, is_method):
		self.name = name
		self.func = func
		self.is_method = is_method


class InlineTokenizer(MessiahStepTokenizer):
	def __init__(self, optimizer):
		super(InlineTokenizer, self).__init__(optimizer)

	def onVisitFile(self, fullpath, relpath):
		pass

	def onExit(self):
		pass

	def visit_Comment(self, token, srow_scol, erow_ecol, line, context):
		pass


class InlineVisitor(MessiahStepVisitor):
	def __init__(self, optimizer):
		super(InlineVisitor, self).__init__(optimizer)
		self.inline_funcs = {}

	def onExit(self):
		self.optimizer and self.optimizer.storeData(self.__class__, self.inline_funcs)

	def visit_FunctionDef(self, node, context):
		if not node.decorator_list:
			return

		deco = node.decorator_list[0]
		if not isinstance(deco, ast.Name) and deco.id == self.optimizer.config.INLINE_FUNC_TAG:
			return

		if self.canInline(node):
			self.inline_funcs[node.name] = Callee(node.name, node, isinstance(node.parent, ast.ClassDef))

	def canInline(self, node):

		args = node.args
		if args.vararg or args.kwarg or args.defaults:
			return False

		return True


class InlineTransformer(MessiahStepTransformer):
	def onEnter(self):
		self.inline_funcs = self.optimizer.loadData(InlineVisitor, default={})

	# def postvisit_FunctionDef(self, node):
	# 	print '1111111111', self.inline_func_names
	# 	if node.name in self.inline_func_names:
	# 		self.inline_funcs[node.name] = node

	def visit_Call(self, node, context):
		func = node.func
		if isinstance(func, ast.Attribute):
			print func.value
		name = func.id if isinstance(func, ast.Name) else func.attr if isinstance(func, ast.Attribute) else ''

		if not name or name not in self.inline_funcs:
			return node

		callee = self.inline_funcs[name]
		context.markDirty(True)
		if isinstance(callee.func.body[0], ast.Return):
			return callee.func.body[0].value

		return node


InlineOptimizeStep = MessiahOptimizerStep(tokenizer=InlineTokenizer, visitor=InlineVisitor, transformer=InlineTransformer)
