# -*- coding:utf-8 -*-

import setup
import sys
from core.executor import OptimizeExecutor  
from core.optimizer import MessiahOptimizer, OptimizeStep
from steps.constant_optimizer import ConstantOptimizeStep
from steps.inline_optimizer import InlineOptimizeStep
from steps.component_optimizer import ComponentOptimizeStep



@OptimizeStep(ConstantOptimizeStep, InlineOptimizeStep, ComponentOptimizeStep)
class Optimizer(MessiahOptimizer):
	pass


if __name__ == '__main__':
	executor = OptimizeExecutor(Optimizer)
	executor.execute()
