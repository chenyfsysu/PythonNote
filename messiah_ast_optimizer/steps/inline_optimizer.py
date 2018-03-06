# -*- coding:utf-8 -*-

from base.optimizer_step import MessiahStepVisitor, MessiahStepTransformer, MessiahStepTokenizer, MessiahOptimizerStep



class InlineVisitor(MessiahStepVisitor):
	def visit_Name(self, node):
		print '2222222222222222', node


class InlineTransformer(MessiahStepTransformer):
	def visit_Name(self, node):
		print 'bbbbbbbbbbbbbbbbbbbb', node
		return node


class InlineTokenizer(MessiahStepTokenizer):
	pass


class InlineOptimizerStep(MessiahOptimizerStep):
	__tokenizer__ = InlineTokenizer
	__visitor__  = InlineVisitor
	__transformer__ = InlineTransformer
