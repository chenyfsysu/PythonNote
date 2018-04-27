# -*- coding:utf-8 -*-

import ast


class RenameVisitor(ast.NodeTransformer):
	FORBIDDEN_NAMES = ('__name__', '__file__', '__package__', '__doc__', 'globals', 'locals')

	def __init__(self, name, rename_prefix='', names_mapping=None):
		self.name = name
		self.rename_prefix = rename_prefix
		self.names_mapping = names_mapping or {}

	def visit_Name(self, node):
		if node.id in self.FORBIDDEN_NAMES:
			raise RuntimeError('Inline function of %s cannot use fobidden name %s' % (self.name, node.id))

		if node.id in self.names_mapping:
			return self.names_mapping[node.id]

		return node
