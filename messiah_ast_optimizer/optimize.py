# -*- coding:utf-8 -*-


from base.optimizer import MessiahOptimizer, OptimizeStep
from steps.constant_optimizer import ConstantOptimizerStep
from steps.inline_optimizer import InlineOptimizerStep


@OptimizeStep(ConstantOptimizerStep, InlineOptimizerStep)
class Optimizer(MessiahOptimizer):
	pass


if __name__ == '__main__':
	import ast

	optimizer = Optimizer()
	file = open('test.py', 'r')
	tree = ast.parse(file.read())
	optimizer.executeVisit('eeee', tree)

	# import astunparse
	# print astunparse.unparse(tree)
