# -*- coding:utf-8 -*-

import ast
import utils

from finder import AttributeFinder


def ismethod(node):
	return isinstance(node, ast.FunctionDef)


def getmembers(mro, predicate=None):
	result = {}
	finder = AttributeFinder(findall=True, predicate=predicate)
	for cls in mro:
		for key, value in finder.find(cls).iteritems():
			if key not in result:
				result[key] = value.node

	return result


def getclassbodies(mro, predicate=None):
	return [node for cls in mro for node in cls.body if not predicate or predicate(node)]


def predicate_entity_property(node):
	return isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and node.value.func.id == 'Property'


def predicate_class_attr(node):
	return isinstance(node, ast.Assign)


def _fold_property(props):
	return 'coco', 0, 0, 0
	for prop in props:
		name, all, flag, delay = _fold_property(prop)
		property_all[name] = all
		property_flag[name] = flag
		property_delay[name] = delay

	return property_all, property_flag, property_delay


def split_cls_body(cls):
	prop = getclassbodies(cls, predicate_entity_property)
	attr = getclassbodies(cls, predicate_class_attr)
	method = getmembers(cls, ismethod)

	return prop, attr, method


def merge_component(host, component):
	attrs, methods, properties, decorator_list = [], {}, [], []

	component.insert(0, host)
	print component
	for comp in component:
		prop, attr, method = split_cls_body(comp)

		properties.append(prop)
		attrs.append(attr)
		methods.update(method)
		decorator_list.extend([deco for cls in comp for deco in cls.decorator_list])

	body = properties + attrs + methods.values()

	# property_all, property_flag, property_delay = fold_properties(properties) # 离线生成Property

	host[0].body = body
	host[0].decorator_list = decorator_list

	return host



if __name__ == '__main__':
	src = """
if True:
	A = 100
else:
	A = 10
"""

	import astunparse
	node = ast.parse(src)
	for body in node.body:
		print body
