# -*- coding:utf-8 -*-

from base.optimizer_step import MessiahStepVisitor, MessiahStepTransformer, MessiahStepTokenizer, MessiahOptimizerStep
from base import utils
from base.context import Definition
from collections import defaultdict

import setting
import ast


Constant = ('True', 'False', 'None')


class ConstantTokenizer(MessiahStepTokenizer):
	def __init__(self):
		self.inline_consts = defaultdict(list)

	def visit_Comment(self, token, srow_scol, erow_ecol, line):
		if self.executing_file not in setting.CONFIG_INLINE_CONST:
			return

		if setting.CONST_INLINE_TAG in token:
			self.inline_consts[self.executing_file].append(srow_scol[0])

	def dump(self):
		return self.inline_consts


class ConstantVisitor(MessiahStepVisitor):
	def __init__(self):
		self.constants = {}

	def visit_Assign(self, node, context):
		if self.executing_file not in setting.INLINE_CONST_FILES:
			return

		if self.executing_file not in setting.INLINE_CONST and \
			utils.get_lineno(node) not in self.tokenizer_data.get(self.executing_file, []):
			return

		if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
			return 

		if not self.isConstant(node.value):
			return

		constant = utils.get_constant(node.value)
		self.constants[(self.getConstName(self.executing_file), node.targets[0].id)] = constant

	def isConstant(self, node):
		if isinstance(node, (ast.Num, ast.Str)):
			return True
		if isinstance(node, ast.Name) and node.id in Constant:
			return True

		return False

	def getConstName(self, path):
		if path in setting.INLINE_CONST:
			return setting.INLINE_CONST[path]
		return setting.CONFIG_INLINE_CONST[path]

	def dump(self):
		return self.constants


class ConstantTransformer(MessiahStepTransformer):

	def visit_Attribute(self, node, context):
		if not isinstance(node.value, ast.Name) or not isinstance(node.ctx, ast.Load):
			return node

		var = context.getAttribute(node.value.id)
		if not isinstance(var, (Definition.ImportType, Definition.ImportFromType)):
			return node
		
		attrid = (node.value.id, node.attr)
		if attrid in self.visitor_data:
			constant = self.visitor_data[attrid]
			node = utils.new_constant(constant, node)
			utils.set_comment(node, '%s.%s=%s' % (attrid[0], attrid[1], constant))
		return node


class ConstantOptimizerStep(MessiahOptimizerStep):
	__tokenizer__ = ConstantTokenizer
	__visitor__  = ConstantVisitor
	__transformer__ = ConstantTransformer
