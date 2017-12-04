class A(object):
	def call(self, p1):
		pass

class B(A):
	def call(self, p1, p2):
		super(B, self).call(p1)

class C(A):
	def call(self):
		pass


class D(B, C):
	def call(self, p1, p2):
		super(D, self).call(p1, p2)


# d = D()
# d.call(1, 2)
# TypeError: call() takes exactly 1 argument (2 given)

print  D.__mro__