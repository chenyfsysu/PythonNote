# -*- coding:utf-8 -*-

import ast


SRC = """
"""


def setup(loader):
	module = ast.parse(SRC)
	module.__preinit__('contextlib', '', None, internal=True)
	loader.setupStandrad('contextlib', module)
