# -*- coding:utf-8 -*-

import ast


SRC = """
"""


def setup(loader):
	module = ast.parse(SRC)
	module.__preinit__('functools', '', None, internal=True)
	loader.setupStandrad('functools', module)
