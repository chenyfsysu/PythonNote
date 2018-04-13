# -*- coding:utf-8 -*-

from core.base import MessiahStepVisitor, MessiahStepTransformer, MessiahStepTokenizer, MessiahOptimizerStep
from core.exception import MImportException
from collections import defaultdict
from core import utils


import ast
import os

Constant = ('True', 'False', 'None')


class ConstantTokenizer(MessiahStepTokenizer):
	def __init__(self, optimizer):
		super(ConstantTokenizer, self).__init__(optimizer)

		self.inline_consts = defaultdict(list)
		self.allow_visit = False

	def onVisitFile(self, fullpath, relpath):
		self.allow_visit = fullpath in self.optimizer.config.CONFIG_INLINE_CONST

	def onExit(self):
		self.optimizer and self.optimizer.storeData(self.__class__, self.inline_consts)

	def visit_Comment(self, token, srow_scol, erow_ecol, line, context):
		if not self.allow_visit:
			return

		self.optimizer.config.CONST_INLINE_TAG in token and self.inline_consts[self._file].append(srow_scol[0])


class ConstantVisitor(MessiahStepVisitor):
	def __init__(self, optimizer):
		super(ConstantVisitor, self).__init__(optimizer)
		self.inline_consts = defaultdict(list)
		self.constants = defaultdict(dict)

	def onEnter(self):
		self.inline_consts = self.optimizer.loadData(ConstantTokenizer)

	def onExit(self):
		self.optimizer and self.optimizer.storeData(self.__class__, self.constants)

	def onVisitFile(self, fullpath, relpath):
		self.allow_visit = fullpath in self.optimizer.config.INLINE_CONST_FILES

	def visit_Assign(self, node, context):
		if not self.allow_visit:
			return

		if context.__fullpath__ not in self.optimizer.config.INLINE_CONST and \
			utils.get_lineno(node) not in self.inline_consts.get(context.__fullpath__ , []):
			return

		if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
			return 

		if not self.isConstant(node.value):
			return

		constant = utils.get_constant(node.value)
		self.constants[context.__fullpath__][node.targets[0].id] = constant

	def isConstant(self, node):
		if isinstance(node, (ast.Num, ast.Str)):
			return True
		if isinstance(node, ast.Name) and node.id in Constant:
			return True

		return False


class ConstantTransformer(MessiahStepTransformer):
	def __init__(self, optimizer):
		super(ConstantTransformer, self).__init__(optimizer)
		self.constants = {}

	def onEnter(self):
		self.constants = self.optimizer.loadData(ConstantVisitor, default={})

	def visit_Attribute(self, node, context):
		if not isinstance(node.value, ast.Name) or not isinstance(node.ctx, ast.Load):
			return node

		if node.value.id not in self.optimizer.config.CONST_ATTRIBUTES:
			return node

		try:
			refer = node.value.load(only_locals=False)
		except MImportException as e:
			self.logger.info(e)
			return node

		if isinstance(refer , ast.Module) and refer.__file__ in self.optimizer.config.INLINE_CONST_FILES:
			if node.attr in self.constants[refer.__file__]:
				name, attr = node.value.id, node.attr
				constant = self.constants[refer.__file__][node.attr]
				node = utils.new_constant(constant, node)
				utils.set_comment(node, '%s.%s=%s' % (name, attr, constant))
				context.markDirty(True)
		return node


ConstantOptimizeStep = MessiahOptimizerStep(tokenizer=ConstantTokenizer, visitor=ConstantVisitor, transformer=ConstantTransformer)
