# -*- coding:utf-8 -*-

import ast


SRC = """
"""


def setup(loader):
	module = ast.parse(SRC)
	module.__preinit__('cc', '', None, internal=True)
	loader.setupEngine('cc', module)
