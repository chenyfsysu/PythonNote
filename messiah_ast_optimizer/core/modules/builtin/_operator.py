# -*- coding:utf-8 -*-

import ast


SRC = """
"""


def setup(loader):
	module = ast.parse(SRC)
	module.__preinit__('operator', '', None, internal=True)
	loader.setupBuiltin('operator', module)
