# -*- coding:utf-8 -*-
import ast
import _ast
import inspect


NODES_TEMPLATE ="""
class %s(%s):
	_fields = %s

	def __init__(self, parent=None):
		super(%s, self).__init__(parent)

	def postinit(%s):
%s
""" 


def is_ast_subclass(cls):

	return inspect.isclass(cls) and issubclass(cls, _ast.AST) and cls != _ast.AST


def export_all_nodes():
	for k, v in inspect.getmembers(_ast, is_ast_subclass):
		bases = ','.join([cls.__name__ for cls in v.__bases__ if issubclass(cls, _ast.AST) and cls != _ast.AST])
		name = v.__name__
		args_fields = ['self'] + list(v._fields)
		args = ', '.join(args_fields)
		stmt = '\n'.join(['		self.%s = %s' % (k, k) for k in v._fields])

		if not bases:
			bases = 'INode'
		if not stmt:
			stmt = '		pass'

		print NODES_TEMPLATE % (name, bases, v._fields, name, args, stmt)


def export_all_visits():
	pass

export_all_nodes()