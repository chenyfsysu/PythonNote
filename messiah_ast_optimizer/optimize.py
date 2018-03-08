# -*- coding:utf-8 -*-


from base.optimizer import MessiahOptimizer, OptimizeStep
from steps.constant_optimizer import ConstantOptimizerStep
from steps.inline_optimizer import InlineOptimizerStep


# @OptimizeStep(ConstantOptimizerStep, InlineOptimizerStep)
@OptimizeStep()
class Optimizer(MessiahOptimizer):
	pass

# if __name__ == '__main__':
# 	import ast

# 	optimizer = Optimizer()
# 	file = open('entities/test.py', 'r')
# 	# optimizer.tokenize(file.readline)
# 	# file.seek(0)
# 	# print file.read()
# 	import ast
# 	tree = ast.parse(file.read())
# 	print tree
# 	import inspect
# 	import astunparse
# 	print astunparse.unparse(tree)
