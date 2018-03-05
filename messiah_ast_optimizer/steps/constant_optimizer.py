# -*- coding:utf-8 -*-

from base.optimizer import MessiahVisitor, MessiahTransformer, MessiahLocator, MessiahOptimizerStep



class ConstantVisitor(MessiahVisitor):
	pass


class ConstantTransformer(MessiahTransformer):
	pass


class ConstantLocator(MessiahLocator):
	pass


ConstantOptimizer = MessiahOptimizerStep(ConstantVisitor(), ConstantTransformer(), ConstantLocator())
