class A(object):
	def __init__(self):
		self.name = 'coco'

A().name
import dis
dis.dis(A)