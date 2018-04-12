# -*- coding:utf-8 -*-

import ast


SRC = """
"""


def setup(loader):
	module = ast.parse(SRC)
	module.__preinit__('MObject', '', None, internal=True)
	loader.setupEngine('MObject', module)
