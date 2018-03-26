import _ast


class AstNodeExtendMeta(type):
	def __new__(mcls, name, bases, attrs):
		setattr(_ast.Module, 'func', attrs['func'])
		return super(AstNodeExtendMeta, mcls).__new__(mcls, name, bases, attrs)


class NodeEx(object):
	__metaclass__ = AstNodeExtendMeta

	def func(self):
		pass

print _ast.Module.func()