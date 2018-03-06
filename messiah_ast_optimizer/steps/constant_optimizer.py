# -*- coding:utf-8 -*-

from base.optimizer_step import MessiahStepVisitor, MessiahStepTransformer, MessiahStepTokenizer, MessiahOptimizerStep

class ConstantTokenizer(MessiahStepTokenizer):
	def visit_Comment(self, token, srow_scol, erow_ecol, line):
		print '1111111111111111', token

class ConstantVisitor(MessiahStepVisitor):
	def visit_Name(self, node):
		print '1111111111', node


class ConstantTransformer(MessiahStepTransformer):
	def visit_Call(self, node):
		print 'aaaaaaaaaaaaaaaaa', node
		return node


class ConstantOptimizerStep(MessiahOptimizerStep):
	__tokenizer__ = ConstantTokenizer
	__visitor__  = ConstantVisitor
	__transformer__ = ConstantTransformer

