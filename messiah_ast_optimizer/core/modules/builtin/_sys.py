# -*- coding:utf-8 -*-

import ast


SRC = """
"""


def setup(loader):
	module = ast.parse(SRC)
	module.__preinit__('sys', '', None, internal=True)
	loader.setupBuiltin('sys', module)
