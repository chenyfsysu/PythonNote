# -*- coding:utf-8 -*-

import ast


SRC = """
"""


def setup(loader):
	module = ast.parse(SRC)
	module.__preinit__('zlib', '', None, internal=True)
	loader.setupBuiltin('zlib', module)
