# -*- coding:utf-8 -*-

import ast


SRC = """
"""


def setup(loader):
	module = ast.parse(SRC)
	module.__preinit__('itertools', '', None, internal=True)
	loader.setupBuiltin('itertools', module)
