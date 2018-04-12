# -*- coding:utf-8 -*-

import ast


SRC = """
"""


def setup(loader):
	module = ast.parse(SRC)
	module.__preinit__('MPlatform', '', None, internal=True)
	loader.setupEngine('MPlatform', module)
