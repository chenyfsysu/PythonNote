# -*- coding:utf-8 -*-
"""
1) 若有Class Attr和FunctionDef重名， 抛错
2）若有除Class Attr、FunctionDef、Property以外的其他AstNode， 抛错
3）import有重名且不一样 ， 抛错， 有些有try import这种如何处理？
4）若有Class及其自类带有无法识别的Meta，跳过合并（后续增加handler，自定义处理）
"""

import ast
import itertools
import common.classutils

from core.base import MessiahStepVisitor, MessiahStepTransformer, MessiahStepTokenizer, MessiahOptimizerStep


class ComponentTokenizer(MessiahStepTokenizer):
	pass

  
class ComponentVisitor(MessiahStepVisitor):
	def visit_ClassDef(self, node, context):
		if node.decorator_list:
			pass
		return node

	def visit_Name(self, node, context):
		pass
		# if isinstance(node.ctx, ast.Load):
		# 	print node.load()


class ComponentTransformer(MessiahStepTransformer):
	def __init__(self, optimizer):
		super(ComponentTransformer, self).__init__(optimizer)
		self.merge_cls = {}

	def visit_ClassDef(self, node, context):
		for deco in node.decorator_list:
			if isinstance(deco, ast.Call) and deco.func.id == 'Components':
				components = []
				for comp in deco.args:
					components.append(comp.load())
				self.mergeComponents(node, components)
		# print 'MRO of %s: %s' % (node.name, [n.name for n in node.nMro()])
		# print 'FullBases of %s: %s' % (node.name, [n.name for n in node.nFullBases()])
		return node

	def mergeComponents(self, host, components):
		methods, attrs, properties = {}, [], []

		skips = []
		components.insert(0, host)
		for component in components:
			mro = component.nMro()
			if not self.checkMerge(mro):
				if component is host:
					return
				skips.append(component)
				continue
			_methods, _attrs, _properties = self._fetchComponent(component, mro)
			methods.update(_methods)
			attrs.extend(_attrs)
			properties.extend(_properties)
		host.body = [b for b in itertools.chain(properties, attrs, methods.values())]

	def _fetchComponent(self, component, mro):
		methods, attrs = component.fullGetmembers(mro)
		properties = component.fullGetbodies(mro=mro, predicate=self.isPropertyDef)

		return methods, attrs, properties

	def isPropertyDef(self, node):
		if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
			return True

	def checkMerge(self, mro):
		for cls in mro:
			pass
		return True


ComponentOptimizeStep = MessiahOptimizerStep(tokenizer=ComponentTokenizer, visitor=ComponentVisitor, transformer=ComponentTransformer)
