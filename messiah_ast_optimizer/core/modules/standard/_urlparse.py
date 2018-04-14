# -*- coding:utf-8 -*-

import ast


SRC = """
"""


def setup(loader):
	module = ast.parse(SRC)
	module.__preinit__('urlparse', '', None, internal=True)
	loader.setupStandrad('urlparse', module)
