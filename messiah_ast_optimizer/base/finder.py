# -*- coding:utf-8 -*-

import ast


class GlobalFinder(ast.NodeVisitor):
	pass


class ImportFinder(ast.NodeVisitor):
	"""根据import内容返回对应的node"""
	pass
