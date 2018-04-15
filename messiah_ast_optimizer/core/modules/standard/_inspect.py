# -*- coding:utf-8 -*-

import ast


SRC = """
"""


def setup(loader):
	module = ast.parse(SRC)
	module.__preinit__('inspect', '', None, internal=True)
	loader.setupStandrad('inspect', module)
