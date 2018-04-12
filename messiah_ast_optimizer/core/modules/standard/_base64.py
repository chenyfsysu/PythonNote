# -*- coding:utf-8 -*-

import ast


SRC = """
"""


def setup(loader):
	module = ast.parse(SRC)
	module.__preinit__('base64', '', None, internal=True)
	loader.setupStandrad('base64', module)
