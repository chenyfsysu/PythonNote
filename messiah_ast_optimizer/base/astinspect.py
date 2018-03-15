# -*- coding:utf-8 -*-

import ast
from finder import AttributeFinder


def ismethod(node):
	return isinstance(node, ast.FunctionDef)


def getmembers(mro, predicate=None):
	result = {}
	finder = AttributeFinder(predicate=predicate)
	for cls in mro:
		for key, value in finder.find(cls).iteritems():
			if key not in result:
				result[key] = value

	return result


def getclassbodies(mro, predicate=None):
	return [node for cls in mro for node in cls.body if not predicate or predicate(node)]



if __name__ == '__main__':
# 	src = """
# class A(object):
# 	Property('coco')
# 	1 + 1

# class B(A):
# 	B = 2
# 	def func(object):
# 		pass

# 	def func2(object):
# 		pass

# 	def inner(object):
# 		pass

# 	@property
# 	def aaa(self):
# 		pass
# """

# 	node = ast.parse(src)
# 	# print getmembers([node.body[0], node.body[1]], ismethod)
# 	# print getbodies([node.body[0], node.body[1]], ismethod)
# 	print node.body[0].body[0]
	print [(a, b) for a in (1, 2, 3) for b in ('a', 'b', 'c')]