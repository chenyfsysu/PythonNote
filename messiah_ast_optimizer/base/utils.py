# -*- coding:utf-8 -*-

import os
import ast


def enum(*sequential, **named):
	enums = dict(zip(sequential, range(len(sequential))), **named)
	return type('Enum', (), enums)


def compare_path(src, dst):
	return os.path.normpath(src) == os.path.normpath(dst)

def get_constant(node):
	if isinstance(node, ast.Num):
		return node.n
	elif isinstance(node, ast.Str):
		return node.s

	return None


def get_lineno(node):
	return getattr(node, 'lineno', -1)


def copy_lineno(node, new_node):
	ast.fix_missing_locations(new_node)
	ast.copy_location(new_node, node)
	return new_node


def new_constant(node, value):
	if isinstance(value, bool):
		new_node = ast.Name(id='True' if value else 'False', ctx=Load())
	elif isinstance(value, (int, float, long)):
		new_node = ast.Num(n=value)
	elif isinstance(value, (unicode, str)):
		new_node = ast.Str(s=value)
	else:
		raise TypeError("unknown type: %s" % type(value).__name__)

	copy_lineno(node, new_node)
	return new_node


def set_comment(node, comment):
	node.__comment__ = comment
