# -*- coding:utf-8 -*-

from core.optimizer_step import MessiahStepVisitor, MessiahStepTransformer, MessiahStepTokenizer, MessiahOptimizerStep

class InlineTokenizer(MessiahStepTokenizer):
	pass


class InlineVisitor(MessiahStepVisitor):
	def visit_Name(self, node, context):
		pass


class InlineTransformer(MessiahStepTransformer):
	def visit_Name(self, node, context):
		return node


class InlineOptimizerStep(MessiahOptimizerStep):
	__tokenizer__ = InlineTokenizer
	__visitor__  = InlineVisitor
	__transformer__ = InlineTransformer
