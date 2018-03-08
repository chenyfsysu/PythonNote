# -*- coding:utf-8 -*-

from base.optimizer_step import MessiahStepVisitor, MessiahStepTransformer, MessiahStepTokenizer, MessiahOptimizerStep

class InlineTokenizer(MessiahStepTokenizer):
	pass


class InlineVisitor(MessiahStepVisitor):
	def visit_Name(self, node):
		pass


class InlineTransformer(MessiahStepTransformer):
	def visit_Name(self, node):
		return node


class InlineOptimizerStep(MessiahOptimizerStep):
	__tokenizer__ = InlineTokenizer
	__visitor__  = InlineVisitor
	__transformer__ = InlineTransformer
