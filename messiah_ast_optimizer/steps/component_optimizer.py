# -*- coding:utf-8 -*-
"""
1)合并的class拥有装饰器
@sutils.crosserver_forbidden_class
class AvatarMember(iPokemonComponent):
2） hotfix怎么办
3） Property这种有很多import回来的值
"""

# -*- coding:utf-8 -*-

import ast
from core.base import MessiahStepVisitor, MessiahStepTransformer, MessiahStepTokenizer, MessiahOptimizerStep
import core.classutils


class ComponentTokenizer(MessiahStepTokenizer):
	pass


class ComponentVisitor(MessiahStepVisitor):
	def visit_ClassDef(self, node, context):
		if node.decorator_list:
			pass
		return node


class ComponentTransformer(MessiahStepTransformer):
	def __init__(self, optimizer):
		super(ComponentTransformer, self).__init__(optimizer)
		self.merge_cls = {}

	def visit_ClassDef(self, node, context):
		for deco in node.decorator_list:
			if isinstance(deco, ast.Call) and deco.func.id == 'Components':
				components = []
				for cls in deco.args:
					cls_node = context.load(cls.id, lazy=False)
					components.append([cls_node.node])
				node = core.classutils.merge_component([node], components)

		return node


ComponentOptimizeStep = MessiahOptimizerStep(tokenizer=ComponentTokenizer, visitor=ComponentVisitor, transformer=ComponentTransformer)
