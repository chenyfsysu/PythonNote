# -*- coding:utf-8 -*-

import ast


SRC = """
"""


def setup(loader):
	module = ast.parse(SRC)
	module.__preinit__('gc', '', None, internal=True)
	loader.setupBuiltin('gc', module)
