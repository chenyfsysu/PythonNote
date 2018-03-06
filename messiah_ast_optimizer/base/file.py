# -*- coding:utf-8 -*-

class LazyFile(object):
	def __init__(self, path):
		self.path = path
		self.file = None
		self.src = ''

		self.ready = False

	def loadFile(self):
		self.file = open(self.path, 'r')

	def readline(self):
		not self.file and self.loadFile()

		for line in self.file.readlines():
			self.src = '\n'.join([self.src, line])
			return line

		self.ready = True
