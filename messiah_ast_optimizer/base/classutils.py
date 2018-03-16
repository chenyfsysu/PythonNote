# -*- coding:utf-8 -*-

import ast
import astinspect
import utils


def predicate_entity_property(node):
	return isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and node.value.func.id == 'Property'


def predicate_class_attr(node):
	return isinstance(node, ast.Assign)


def _fold_property(props):
	print props
	return 'coco', 0, 0, 0
	for prop in props:
		name, all, flag, delay = _fold_property(prop)
		property_all[name] = all
		property_flag[name] = flag
		property_delay[name] = delay

	return property_all, property_flag, property_delay


def split_cls_body(cls):
	prop = astinspect.getclassbodies(cls, predicate_entity_property)
	attr = astinspect.getclassbodies(cls, predicate_class_attr)
	method = astinspect.getmembers(cls, astinspect.ismethod)

	return prop, attr, method


def merge_component(host, component):
	attrs, methods, properties, decorator_list = [], {}, [], []

	component.insert(0, [host])
	for comp in component:
		prop, attr, method = split_cls_body(comp)

		properties.append(prop)
		attrs.append(attr)
		methods.update(method)
		decorator_list.extend([deco for cls in comp for deco in cls.decorator_list])

	body = properties + attrs + methods.values()

	# property_all, property_flag, property_delay = fold_properties(properties) # 离线生成Property

	host.body = body
	host.decorator_list = decorator_list

	return host



if __name__ == '__main__':
	src = """
class A(object):
	A = 1
	def func():
		pass

class B(object):
	B = 2
"""

	import astunparse
	node = ast.parse(open('../test.py').read())
	cls1 = node.body[0]
	cls2 = node.body[1]
	merge_component(cls2, [[cls1],])
	print astunparse.unparse(cls2)
