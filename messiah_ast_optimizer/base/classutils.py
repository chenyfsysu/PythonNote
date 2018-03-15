# -*- coding:utf-8 -*-

import ast
import astinspect


def predicate_entity_property(node):
	return isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and node.value.func.id == 'Property'


def predicate_class_attr(node):
	return isinstance(node, ast.Assign)


def merge_component(cls, component):
	body = []
	for comp in component:
		body.extend(astinspect.getclassbodies(comp, predicate_entity_property))
		body.extend(astinspect.getclassbodies(comp, predicate_class_attr))
		body.extend(astinspect.getmembers(component, astinspect.ismethod))
	body.extend(cls.body)
	cls.body = body

	return cls


def _fold_property(props):
	pass



def fold_properties(props):
	property_all=property_flag=property_delay = []

	for prop in props:
		name, all, flag, delay = _fold_property(prop)
		property_all[name] = all
		property_flag[name] = flag
		property_delay[name] = delay

	return property_all, property_flag, property_delay


if __name__ == '__main__':
	src = """
class A(object):
	name = 'coco'
	Property('coco')
	1 + 1

class B(A):
	B = 2
	def func(object):
		pass

	def func2(object):
		pass

	def inner(object):
		pass

	@property
	def aaa(self):
		pass
"""

	import astunparse
	node = ast.parse(src)
	# print getmembers([node.body[0], node.body[1]], ismethod)
	# print getbodies([node.body[0], node.body[1]], ismethod)
	cls1 = node.body[0]
	cls2 = node.body[1]
	merge_component(cls2, [[cls1],])
	print cls2.body
	print astunparse.unparse(node)
