# -*- coding:utf-8 -*-

import ast


SRC = """
"""


def setup(loader):
	module = ast.parse(SRC)
	module.__preinit__('os', '', None, internal=True)
	loader.setupStandrad('os', module)
