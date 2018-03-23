# -*- coding:utf-8 -*-


from core.optimizer import MessiahOptimizer, OptimizeStep
from steps.constant_optimizer import ConstantOptimizeStep
from steps.inline_optimizer import InlineOptimizeStep
from steps.component_optimizer import ComponentOptimizeStep


@OptimizeStep(ConstantOptimizeStep, InlineOptimizeStep, ComponentOptimizeStep)
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
