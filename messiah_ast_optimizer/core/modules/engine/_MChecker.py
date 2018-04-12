# -*- coding:utf-8 -*-

import ast


SRC = """
"""


def setup(loader):
	module = ast.parse(SRC)
	module.__preinit__('MChecker', '', None, internal=True)
	loader.setupEngine('MChecker', module)
