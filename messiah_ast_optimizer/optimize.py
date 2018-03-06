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
	file = open('entities/common/const.py', 'r')
	optimizer.tokenize(file.readline)
	file.seek(0)
	print file.read()
