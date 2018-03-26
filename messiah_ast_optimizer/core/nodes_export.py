# -*- coding:utf-8 -*-
import ast
import _ast
import inspect


NODES_TEMPLATE ="""
@dynamic_extend(_ast.%s)
class %s(Node):
	pass
""" 


def is_ast_subclass(cls):

	return inspect.isclass(cls) and issubclass(cls, _ast.AST) and cls != _ast.AST


def export_all_nodes():
	for k, v in inspect.getmembers(_ast, is_ast_subclass):
		if issubclass(v, _ast.AST) and v != _ast.AST:
			print NODES_TEMPLATE % (v.__name__, v.__name__)


def export_all_visits():
	pass

export_all_nodes()