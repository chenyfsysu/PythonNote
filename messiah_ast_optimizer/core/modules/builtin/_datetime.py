# -*- coding:utf-8 -*-

import ast


SRC = """
"""


def setup(loader):
	module = ast.parse(SRC)
	module.__preinit__('datetime', '', None, internal=True)
	loader.setupBuiltin('datetime', module)
