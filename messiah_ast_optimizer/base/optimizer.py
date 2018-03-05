# -*- coding:utf-8 -*-

import ast


class MessiahVisitorDelegate(ast.NodeVisitor):
	def __init__(self, steps):
		self.steps = steps

	def __getattr__(self, attr):
		if attr.startswith('visit_'):
			for step in steps:
				return getattr(step.visitor, attr)


class MessiahTransformerDelegate(ast.NodeTransformer):
	pass



class MessiahAbstractOptimizer(object):
	def visit(self):
		pass

	def transform(self):
		pass

	def process_visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

	def process_transform(self, node):
		pass
