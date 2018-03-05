# -*- coding:utf-8 -*-

from base.optimizer import MessiahVisitor, MessiahTransformer, MessiahOptimizerStep



class InlineVisitor(MessiahVisitor):
	SKIP = True


class InlineTransformer(MessiahTransformer):
	pass


class InlineRecorder(MessiahRecorder):
	pass


MessiahOptimizer(InlineVisitor(), InlineTransformer(), InlineRecorder())
