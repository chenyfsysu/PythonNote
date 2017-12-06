class Property(object):
	def __init__(self, fget, fset):
		self.fget = fget
		self.fset = fset

	def __get__(self, obj, cls):
		return self.fget(obj)

	def __set__(self, obj, val):
		self.fset(obj, val)

class Object(object):
	def fget(self):
		print 'fget called'

	def fset(self, val):
		print 'fset called', val

	f = Property(fget, fset)

o = Object()
o.f