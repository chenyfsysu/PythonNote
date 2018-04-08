B = 10

def wrapper(x):
	def wrapper(func):
		pass

	return wrapper

class A(object):

	def func(self):
		global B
		B = 100

print dir(wrapper)