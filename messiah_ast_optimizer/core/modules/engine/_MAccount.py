# -*- coding:utf-8 -*-

import ast


SRC = """
"""


def setup(loader):
	module = ast.parse(SRC)
	module.__preinit__('MAccount', '', None, internal=True)
	loader.setupEngine('MAccount', module)
