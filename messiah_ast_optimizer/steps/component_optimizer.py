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
import common.classutils


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
		bases = node.nBases()
		if bases and bases[0]:
			base = bases[0]
			print base.parent.scope.locals
		print 'MRO of %s: %s' % (node.name, [n.name for n in node.nMro()])
		return node

	def visit_ImportFrom(self, node, context):
		# print '11111111111', node.lookup('AvatarMember')
		return node


ComponentOptimizeStep = MessiahOptimizerStep(tokenizer=ComponentTokenizer, visitor=ComponentVisitor, transformer=ComponentTransformer)
