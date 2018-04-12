# -*- coding:utf-8 -*-

import ast


SRC = """
"""


def setup(loader):
	module = ast.parse(SRC)
	module.__preinit__('urllib', '', None, internal=True)
	loader.setupStandrad('urllib', module)
