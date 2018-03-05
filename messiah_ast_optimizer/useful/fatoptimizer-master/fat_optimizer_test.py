import os
import ast
import astunparse
import textwrap
import fatoptimizer.convert_const
import fatoptimizer.namespace
import fatoptimizer.optimizer
import fatoptimizer.tools
import io
import re
import sys
from fatoptimizer.tools import UNSET

def format_code(code):
    return textwrap.dedent(code).strip()


def compile_ast(source):
    source = format_code(source)
    return ast.parse(source, '<string>', 'exec')


def compile_ast_expr(source):
    module = ast.parse(source, '<string>', 'exec')
    assert isinstance(module, ast.Module)
    body = module.body
    assert len(body) == 1
    expr = body[0]
    assert isinstance(expr, ast.Expr)
    return expr.value


class Transformer(ast.NodeTransformer):

	def __init__(self, file_path):
		super(Transformer, self).__init__()

		self.namespaces = dict()

		self.file_path = file_path
		self.file_name = os.path.basename(file_path)
		self.module_name = os.path.splitext(self.file_name)[0]
		self.lines = []
		self.config = fatoptimizer.Config()

	def process(self):
		with open(self.file_path, "r") as f:
			self.lines = f.readlines()

		with open(self.file_path, "r") as f:
			str = f.read()
			print(str)
			tree = self.optimize(str)
			print(tree)
			content = astunparse.unparse(tree)

		with open(self.file_path, mode='w') as f:
			f.write("# -*- coding:utf-8 -*-\n\n\n")
			f.write(content)

	def optimize(self, source):
		tree = compile_ast(source)
		return fatoptimizer.optimize(tree, "<string>", self.config)

transform = Transformer('test.py')
transform.process()