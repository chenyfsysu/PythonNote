# -*- coding:utf-8 -*-

import os
import ast
import const
import itertools


def enum(*sequential, **named):
	enums = dict(zip(sequential, range(len(sequential))), **named)
	return type('Enum', (), enums)


def compare_path(src, dst):
	return os.path.normpath(src) == os.path.normpath(dst)


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


def is_pure_constant(node):
	return isinstance(node, (ast.Num, ast.Str)) or isinstance(node, ast.Name) and node.id in const.BUILTIN_NAME


def get_pure_constant(node):
	if isinstance(node, ast.Name) and node.id in const.BUILTIN_NAME:
		value = True if node.id == 'True' else False if node.id == 'False' else None
	elif isinstance(node, ast.Num):
		value = node.n
	elif isinstance(value, ast.Str):
		value = node.s  
	else:
		value = const.UNKNOW

	return value


def get_constant(node):
	if is_pure_constant(node):
		value = get_pure_constant(node)
	elif isinstance(node, (ast.Tuple, ast.List)):
		value = []
		for _node in node.elts:
			value.append(get_constant(_node))
		if isinstance(node, ast.Tuple):
			value = tuple(value)
		if any((x == const.UNKNOW for x in value)):
			value = const.UNKNOW
	elif isinstance(node, ast.Dict):
		value = {}
		for _key, _value in itertools.izip(node.keys, node.values):
			k, v = get_constant(_key), get_constant(_value)
			if k == const.UNKNOW or v == const.UNKNOW:
				return const.UNKNOW
			value[k] = v
	else:
		value = const.UNKNOW

	return value
 

def get_names(node):
	if isinstance(node, ast.Name): 
		return node.id

	if isinstance(node, ast.Tuple):
		names = []
		for item in node.elts:
			item_names = get_names(item)
			names.append(item_names)
		return names


def unfold_assign(names, values):
	if not isinstance(names, (list, tuple)):
		return {names: values}

	items = {}
	for name, value in itertools.izip(names, values):
		if isinstance(name, list):
			_items = unfold_assign(name, value)
			items.update(_items)
		else:
			items[name] = value
	return items


def fold_binop(op, src, dst):
	cls = op.__class__
	return cosnt.UNKNOW if cls not in const.BIN_OPERATOR else const.BIN_OPERATOR[cls](src, dst)


def calc_augassign(src, op, value):
	dst = utils.get_constant(node.value)
	return const.UNKNOW if dst == const.UNKNOW else fold_binop(op, src, dst)


def set_comment(node, comment):
	node.__comment__ = comment


def set_dependency(node, filename, dependency):
	pass


if __name__ == '__main__':
	# constant
	node = ast.parse('a, (b, c) = {1: a}, (1, 2)').body[0]
	names = get_names(node.targets[0])
	value = get_constant(node.value)
	print names, value
	print unfold_assign(names, value)
