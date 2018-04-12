# -*- coding:utf-8 -*-

from core.base import MessiahStepVisitor, MessiahStepTransformer, MessiahStepTokenizer, MessiahOptimizerStep
from collections import defaultdict
from core import utils


import ast
import os

Constant = ('True', 'False', 'None')


def is_inline_file(root, file, const_files):
	return any(utils.is_same_file(os.path.join(root, f), file) for f in const_files)


class ConstantTokenizer(MessiahStepTokenizer):
	def __init__(self, optimizer):
		super(ConstantTokenizer, self).__init__(optimizer)

		self.inline_consts = defaultdict(list)

	def onExit(self):
		self.optimizer and self.optimizer.storeData(self.__class__, self.inline_consts)

	def visit_Comment(self, token, srow_scol, erow_ecol, line, context):
		if context.__relpath__ not in self.optimizer.config.CONFIG_INLINE_CONST:
			return

		self.optimizer.config.CONST_INLINE_TAG in token and self.inline_consts[self._file].append(srow_scol[0])


class ConstantVisitor(MessiahStepVisitor):
	def __init__(self, optimizer):
		super(ConstantVisitor, self).__init__(optimizer)
		self.inline_consts = defaultdict(list)
		self.constants = {}

	def onEnter(self):
		self.inline_consts = self.optimizer.loadData(ConstantTokenizer)

	def onExit(self):
		self.optimizer and self.optimizer.storeData(self.__class__, self.constants)

	def visit_Assign(self, node, context):
		if context.__relpath__  not in self.optimizer.config.INLINE_CONST_FILES:
			return

		if context.__relpath__  not in self.optimizer.config.INLINE_CONST and \
			utils.get_lineno(node) not in self.inline_consts.get(context.__relpath__ , []):
			return

		if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
			return 

		if not self.isConstant(node.value):
			return

		constant = utils.get_constant(node.value)
		self.constants[(self.getConstName(context.__relpath__ ), node.targets[0].id)] = constant

	def isConstant(self, node):
		if isinstance(node, (ast.Num, ast.Str)):
			return True
		if isinstance(node, ast.Name) and node.id in Constant:
			return True

		return False

	def getConstName(self, path):
		if path in self.optimizer.config.INLINE_CONST:
			return self.optimizer.config.INLINE_CONST[path]
		return self.optimizer.config.CONFIG_INLINE_CONST[path]


class ConstantTransformer(MessiahStepTransformer):
	def __init__(self, optimizer):
		super(ConstantTransformer, self).__init__(optimizer)
		self.constants = {}

	def onEnter(self):
		self.constants = self.optimizer.loadData(ConstantVisitor, default={})

	def visit_Attribute(self, node, context):
		if not isinstance(node.value, ast.Name) or not isinstance(node.ctx, ast.Load):
			return node

		attrid = (node.value.id, node.attr)
		if attrid not in self.constants:
			return node

		refer = node.value.load(only_locals=False)
		if isinstance(refer , ast.Module) and is_inline_file(context.__rootpath__, refer.__file__, self.optimizer.config.INLINE_CONST_FILES):
			constant = self.constants[attrid]
			node = utils.new_constant(constant, node)
			utils.set_comment(node, '%s.%s=%s' % (attrid[0], attrid[1], constant))
		return node


ConstantOptimizeStep = MessiahOptimizerStep(tokenizer=ConstantTokenizer, visitor=ConstantVisitor, transformer=ConstantTransformer)
