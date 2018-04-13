# -*- coding:utf-8 -*-

import os
import ast
import const
import unparser
import itertools
from collections import defaultdict


def enum(*sequential, **named):
	enums = dict(zip(sequential, range(len(sequential))), **named)
	enums['__enum__'] = enums.keys()
	return type('Enum', (), enums)


def get_parent_dir(dir, level):
	return os.path.abspath('%s%s' % (dir, '%s%s' % (os.path.sep, '..') * level))


def is_parent_dir(parent, path):
	return not os.path.relpath(path, parent).startswith(os.pardir)


def is_same_file(src, dst):
	return os.stat(src) == os.stat(dst)


def format_path(root, path):
	return os.path.normpath(os.path.join(root, path))


def get_lineno(node):
	return getattr(node, 'lineno', -1)


def copy_lineno(node, new_node):
	ast.fix_missing_locations(new_node)
	ast.copy_location(new_node, node)
	return new_node


def new_assignment(name, value):
	name = ast.Name(id=name)
	value = new_constant(value)

	return ast.Assign(targets=[name], value=value)


def new_constant(value, node=None):
	if isinstance(value, bool):
		new_node = ast.Name(id='True' if value else 'False', ctx=ast.Load())
	elif isinstance(value, (int, float, long, complex)):
		new_node = ast.Num(n=value)
	elif isinstance(value, (unicode, str)):
		new_node = ast.Str(s=value)
	elif isinstance(value, (tuple, list)):
		cls = ast.Tuple if isinstance(value, tuple) else ast.List
		elts = [new_constant(elt, node) for elt in value]
		new_node = cls(elts=elts, ctx=ast.Load)
	elif isinstance(value, set):
		elts = [new_constant(elt, node) for elt in value]
		new_node = ast.Set(elts=elts)
	elif isinstance(value, dict):
		keys = [new_constant(k, node) for k in value.keys()]
		values = [new_constant(v, node) for v in value.values()]
		new_node = ast.Dict(keys=keys, values=values)
	elif isinstance(value, frozenset):
		elts = [new_constant(elt, node) for elt in value]
		arg = ast.Tuple(elts=elts, ctx=ast.Load())
		func = ast.Name(id='frozenset', ctx=ast.Load())
		new_node = ast.Call(func=func, args=[arg], keywords=[], starargs=None, kwargs=None)
	elif value is None:
		new_node = ast.Name(id='None', ctx=ast.Load())
	else:
		raise TypeError("unknown type: %s" % type(value).__name__)

	node and copy_lineno(node, new_node)
	new_node.__preinit__(parent=node.parent if node else node.parent)
	new_node.__postinit__()
	return new_node


def is_pure_constant(node):
	return isinstance(node, (ast.Num, ast.Str)) or isinstance(node, ast.Name) and node.id in const.BUILTIN_NAME


def get_pure_constant(node):
	if isinstance(node, ast.Name) and node.id in const.BUILTIN_NAME:
		value = True if node.id == 'True' else False if node.id == 'False' else None
	elif isinstance(node, ast.Num):
		value = node.n
	elif isinstance(node, ast.Str):
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
 

def get_names(node, pure_only=True):
	if isinstance(node, ast.Name): 
		return [node.id]

	if isinstance(node, ast.Tuple):
		names = []
		for item in node.elts:
			item_names = get_names(item)
			if pure_only and item_names is None:
				return None
			names.append(item_names) if item_names is None else names.extend(item_names)
		return names


def unpack_sequence(target, value):
	try:
		items = []
		for i, _target in enumerate(target.elts):
			if isinstance(_target, (ast.Tuple, ast.List)):
				_items = unpack_sequence(_target, value.elts[i] if value else None)
				items.extend(_items)
			elif isinstance(_target, ast.Name):
				items.append((_target, value.elts[i] if value else None))
		return items
	except:
		return unpack_sequence(target, None)


def fold_binop(op, src, dst):
	cls = op.__class__
	return cosnt.UNKNOW if cls not in const.BIN_OPERATOR else const.BIN_OPERATOR[cls](src, dst)


def new_importfrom(module, name, asname, level=0, parent=None):
	names = [ast.alias(name=name, asname=asname)]
	node = ast.ImportFrom(module=module, names=names, level=level)
	node.__preinit__(parent)
	node.__postinit__()

	return node

def calc_augassign(src, op, value):
	dst = utils.get_constant(node.value)
	return const.UNKNOW if dst == const.UNKNOW else fold_binop(op, src, dst)


def unparse_src(node):
	return unparser.unparse(node)


def set_comment(node, comment):
	node.__comment__ = comment


def set_dependency(node, filename, dependency):
	pass


def topo_sort(verts, edges, relies=None):
	"""
	edges: 依赖了哪些文件
	relies：被哪些文件依赖列表
	"""
	if not relies:
		relies = defaultdict(list)
		for v, rvs in edges.iteritems():
			for rv in rvs:
				relies[rv].append(v)
	

	q = [v for v in verts if v not in relies]
	print q

	sorted_lst = []
	while q:
		v = q.pop()

		for rv in edges.get(v, []):
			relies[rv].remove(v)
			if not relies[rv]:
				q.insert(0, rv)

		sorted_lst.append(v)

	if len(sorted_lst) != len(verts):
		remains = [v for v in verts if v not in sorted_lst]
		raise RuntimeError('cannot process topological sorting, recursive dependency exsits, %s' % remains)

	return sorted_lst


if __name__ == '__main__':
	node = ast.parse('part_a, part_b, (v_type, value) = fml').body[0]
	node = ast.parse('a, self.name = 1').body[0]
	print get_names(node.targets[0], pure_only=False)