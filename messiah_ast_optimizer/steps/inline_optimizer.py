# -*- coding:utf-8 -*-

from core.base import MessiahStepVisitor, MessiahStepTransformer, MessiahStepTokenizer, MessiahOptimizerStep

class InlineTokenizer(MessiahStepTokenizer):
	pass


class InlineVisitor(MessiahStepVisitor):
	def visit_Name(self, node, context):
		pass


class InlineTransformer(MessiahStepTransformer):
	def visit_Name(self, node, context):
		return node


InlineOptimizeStep = MessiahOptimizerStep(tokenizer=InlineTokenizer, visitor=InlineVisitor, transformer=InlineTransformer)
