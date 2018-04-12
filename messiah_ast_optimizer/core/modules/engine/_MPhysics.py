# -*- coding:utf-8 -*-

import ast


SRC = """
"""


def setup(loader):
	module = ast.parse(SRC)
	module.__preinit__('MPhysics', '', None, internal=True)
	loader.setupEngine('MPhysics', module)
