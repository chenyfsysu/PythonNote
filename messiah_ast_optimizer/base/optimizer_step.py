# -*- coding:utf-8 -*-


class MessiahVisitor(ast.NodeVisitor):
	SKIP = False


class MessiahTransformer(ast.NodeTransformer):
	pass


class MessiahLocator(object):
	pass


class MessiahOptimizerStep(object):
	def __init__(self, visitor, transformer, locator):
		self.visitor = visitor
		self.transformer = transformer
		self.locator = locator

	def skip_visit(self):
		return False

	def skip_file_visit(self):
		return False

	def skip_file_transform(self):
		return False

	def visit(self):
		pass

	def transform(self):
		pass