# -*- coding:utf-8 -*-
"""
1)合并的class拥有装饰器
@sutils.crosserver_forbidden_class
class AvatarMember(iPokemonComponent):
2） hotfix怎么办
3） Property这种有很多import回来的值
"""

from core.base import MessiahStepVisitor, MessiahStepTransformer, MessiahStepTokenizer, MessiahOptimizerStep


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

	def onStart(self, file):
		super(ComponentTransformer, self).onStart(file)
		self.loader = None

	def visit_ClassDef(self, node, context):
		if node.decorator_list:
			cls = self.merge_cls.get('AvatarModelComponent', None)
			cls and node.body.extend(cls.body)
		else:
			self.merge_cls['AvatarModelComponent'] = node
		return node


ComponentOptimizeStep = MessiahOptimizerStep(tokenizer=ComponentTokenizer, visitor=ComponentVisitor, transformer=ComponentTransformer)
