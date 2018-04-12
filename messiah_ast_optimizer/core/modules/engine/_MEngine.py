# -*- coding:utf-8 -*-

import ast


SRC = """
"""


def setup(loader):
	module = ast.parse(SRC)
	module.__preinit__('MEngine', '', None, internal=True)
	loader.setupEngine('MEngine', module)
