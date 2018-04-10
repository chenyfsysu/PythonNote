# -*- coding:utf-8 -*-

import ast


SRC = """
"""


def setup(loader):
	module = ast.parse(SRC)
	module.__preinit__('time', '', None, internal=True)
	loader.setupBuiltin('time', module)
