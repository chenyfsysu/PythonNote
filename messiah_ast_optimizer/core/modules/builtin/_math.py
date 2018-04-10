# -*- coding:utf-8 -*-

import ast


SRC = """
"""


def setup(loader):
	module = ast.parse(SRC)
	module.__preinit__('math', '', None, internal=True)
	loader.setupBuiltin('math', module)
