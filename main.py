class A(object):
	def call(self):
		print 'call A'

class B(A):
	def call(self):
		super(B, self).call()
		print 'call B'

# b = B()
# b.call()  # call A call B
print B.__mro__