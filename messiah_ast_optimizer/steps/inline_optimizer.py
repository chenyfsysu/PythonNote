# -*- coding:utf-8 -*-

from core.base import MessiahStepVisitor, MessiahStepTransformer, MessiahStepTokenizer, MessiahOptimizerStep
from core.tools import RenameVisitor

import ast

"""
1）
2）如果有引用禁止名字：__name__, __file__, __doc__, __package__, globals, locals等，不能内联
3）如果内联函数有引用globals：如果是import的内容，则在宿主函数的模块中添加import，否则不能内联

问题：
1）Visitor引用inline func会导致内存泄漏，要release
2）Import内容合并看下能不能做成通用的
3）能否做成通用的Inline，而不是只能合并Return
"""


class Callee(object):
	__slots__ = ('name', 'func', 'is_method', 'infers')

	def __init__(self, name, func, is_method, infers):
		self.name = name
		self.func = func
		self.is_method = is_method
		self.infers = infers


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
		if not isinstance(deco, ast.Name) or deco.id != self.optimizer.config.INLINE_FUNC_TAG:
			return

		if not self.canCalleeInline(node):
			return

		global_names = node.scope.globals()
		module = node.nModule()
		
		global_infers = {}
		for name in global_names:
			if name not in module.scope.locals:
				continue
			infer = module.scope.locals[name]
			if not isinstance(infer, (ast.Import, ast.ImportFrom)):
				return

			global_infers[name] = infer

		self.inline_funcs[node.name] = Callee(node.name, node, isinstance(node.parent, ast.ClassDef), global_infers)

	def canCalleeInline(self, node):
		args = node.args
		if args.vararg or args.kwarg or args.defaults:
			return False

		return True


class InlineTransformer(MessiahStepTransformer):
	def onEnter(self):
		self.inline_funcs = self.optimizer.loadData(InlineVisitor, default={})
		self.global_infers = {}

	def onVisitFile(self, fullpath, relpath):
		self.global_infers = {}

	def visit_Call(self, node, context):
		if not self.canCallsiteInline(node):
			return node

		func = node.func
		name = func.id if isinstance(func, ast.Name) else func.attr if isinstance(func, ast.Attribute) else ''

		if not name or name not in self.inline_funcs:
			return node

		if isinstance(func, ast.Attribute) and not isinstance(func.value, ast.Name):
			return node

		callee = self.inline_funcs[name]
		body = callee.func.body[0]
		if not isinstance(body, ast.Return):
			return node

		if not self.mergeGlobalInfers(node, callee.infers):
			return node

		mapping = callee.func.args.unpackPosArgs(node, callee.is_method)
		RenameVisitor('', names_mapping=mapping).visit(body)
		context.markDirty(True)
		return body.value

	def mergeGlobalInfers(self, node, infers):
		module = node.nModule()

		global_infers = {}
		for name, infer in infers.iteritems():
			cur = None
			if name in self.global_infers:
				cur = self.global_infers[name]
			elif name in module.scope.locals:
				cur = module.scope.locals[name]

			if not cur:
				global_infers[name] = infer
			else:
				if not isinstance(cur, (ast.Import, ast.ImportFrom)) or type(cur) != type(infer):
					return False

		self.global_infers.update(global_infers)
		return True

	def postvisit_Module(self, node):
		body = self.global_infers.values()
		body.extend(node.body)
		node.body = body

	def canCallsiteInline(self, callsite):
		return not callsite.starargs and not callsite.kwargs



InlineOptimizeStep = MessiahOptimizerStep(tokenizer=InlineTokenizer, visitor=InlineVisitor, transformer=InlineTransformer)
