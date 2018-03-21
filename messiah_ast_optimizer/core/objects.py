# -*- coding:utf-8 -*-

import ast
import utils
import const


class ObjectAllocator(object):
	__mapping__ = {}

	@classmethod
	def lookup(cls, *ntypes):
		def _lookup(kcls):
			for node in ntypes:
				cls.__mapping__[node.__name__] = kcls
			return kcls
		return _lookup

	@classmethod
	def allocate(cls, node, *args):
		creator = cls.__mapping__.get(node.__class__.__name__, Object)
		return creator.create(node, *args)


@ObjectAllocator.lookup(ast.Assign)
class AssignmentAllocator(object):

	@classmethod
	def create(cls, node):
		objs = {}
		for target in node.targets:
			if isinstance(target, ast.Name):
				name, value = cls._create(target, node.value)
				objs[name] = value
			elif isinstance(target, (ast.Tuple, ast.List)):
				items = utils.unpack_sequence(target, node.value)
				for name, value in items:
					name, value = cls._create(name, value)
					objs[name] = value
		return objs					

	@classmethod
	def _create(cls, target, val):
		name = target.id
		value = utils.get_constant(val) if val else const.UNKNOW
		obj =  Object(name, val) if value == const.UNKNOW else ConstantObject(name, val, value)

		return name, obj


class Object(object):
	def __init__(self, name, node):
		self.name = name
		self.node = node

	@classmethod
	def create(cls, node, *args):
		return cls(node)


class ConstantObject(Object):
	def __init__(self, name, node, val):
		super(ConstantObject, self).__init__(name, node)
		self.val = val



@ObjectAllocator.lookup(ast.Import, ast.ImportFrom)
class LazyImportObject(Object):
	def __init__(self, module, asname, fromlist=None, level=-1):
		super(LazyImportObject, self).__init__(asname if asname else module, None)
		self.module = module
		self.asname = asname
		self.fromlist = fromlist
		self.level = level

	@classmethod
	def create(cls, node):
		if isinstance(node, ast.Import):
			return {al.asname if al.asname else al.name: cls(al.name, al.asname) for al in node.names}
		else:
			return {al.asname if al.asname else al.name: 
					cls(node.module, al.asname, al.name, node.level) for al in node.names}


@ObjectAllocator.lookup(ast.FunctionDef)
class FunctionObject(Object):
	def __init__(self, node, name):
		super(FunctionObject, self).__init__(name, node)

	@classmethod
	def create(cls, node):
		return {node.name: cls(node.name, node)}


@ObjectAllocator.lookup(ast.ClassDef)
class ClassObject(Object):
	def __init__(self, node, name):
		super(ClassObject, self).__init__(name, node)

	@classmethod
	def create(cls, node):
		return {node.name: cls(node.name, node)}



@ObjectAllocator.lookup(ast.Module)
class ModuleObject(Object):
	def __init__(self, name, file=None, path=None, node=None):
		super(ModuleObject, self).__init__(name, node)
		self.file = file
		self.path = path

		self.locals = {}

	def getParent(self):
		return os.path.dirname(self.file)

	def load(self, name):
		pass

	@classmethod
	def create(cls, node, name):
		return {name: cls(name, node=node)}



if __name__ == '__main__':
	node = ast.parse('a, (b, (c, d)) = 1, (2, (3, (4, 5)))').body[0]
	node = ast.parse('a, (b, (c, d)) = 1, (2, self.test())').body[0]
	node = ast.parse('import a as b, c as d').body[0]
	node = ast.parse('from a import b as c').body[0]
	node = ast.parse('def func():pass').body[0]
	node = ast.parse('class A:pass').body[0]
	node = ast.parse('class A:pass')

	print ObjectAllocator.allocate(node, '__main__')
