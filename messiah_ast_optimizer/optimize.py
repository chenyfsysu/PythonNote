# -*- coding:utf-8 -*-


from base.optimizer import MessiahAbstractOptimizer
from base.utils import OptimizeStep

from steps.constant_optimizer import ConstantOptimizer


@OptimizeStep(ConstantOptimizer)
class Optimizer(MessiahAbstractOptimizer):
	pass
