CODE = """
class A(object):
	@property
	def func(self):
		pass

	@property.setter
	def func(self):
		pass

"""

import ast
print ast.parse(CODE).body[0].body[1].decorator_list[0].value