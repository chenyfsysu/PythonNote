# -*- coding:utf-8 -*-
"""
1) classutils提供合并两个class的功能
2) 添加文件依赖，保证优化不会覆盖
3）插入Import的功能
"""
from base.optimizer_step import MessiahStepVisitor, MessiahStepTransformer, MessiahStepTokenizer, MessiahOptimizerStep


class ComponentTokenizer(MessiahStepTokenizer):
	pass


class ComponentVisitor(MessiahStepVisitor):
	def visit_ClassDef(self, node, context):
		if node.decorator_list:
			pass
		return node


class ComponentTransformer(MessiahStepTransformer):
	def __init__(self):
		super(ComponentTransformer, self).__init__()
		self.merge_cls = {}

	def visit_ClassDef(self, node, context):
		if node.decorator_list:
			cls = self.merge_cls.get('AvatarModelComponent', None)
			cls and node.body.extend(cls.body)
		else:
			self.merge_cls['AvatarModelComponent'] = node
		return node


class ComponentOptimizerStep(MessiahOptimizerStep):
	__tokenizer__ = ComponentTokenizer
	__visitor__  = ComponentVisitor
	__transformer__ = ComponentTransformer
