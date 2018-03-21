# -*- coding:utf-8 -*-

from utils import enum, compare_path

import os
import ast
import unparser
import scandir


class OptimizeStatus(object):
	Status = enum(INIT=1, EXECUTING=2, ERROR=3, COMPLETED=4)

	def __init__(object):
		self.status = self.Status.INIT
		self.error_msg = ''


class OptimizeExecutor(object):
	def __init__(self , optimizer, path, ignore_dirs, ignore_files):
		self.optimizer = optimizer
		self.path = path
		self.ignore_dirs = [os.path.normpath(d) for d in ignore_dirs]
		self.ignore_files = [os.path.normpath(f) for f in ignore_files]

		self.file = None
		self.filter_files = {}

	def execute(self):
		self.filterExecuteFiles()

		self.executeTokenize()
		self.executeVisit()
		self.executeTransform()

	def filterExecuteFiles(self):
		self.filter_files = {}
		for root, dirs, files in scandir.walk(self.path, topdown=True):
			dirs[:] = [d for d in dirs if os.path.normpath(os.path.join(root, d)) not in self.ignore_dirs]

			for file in files:
				if file.endswith('.py'):
					fullpath = os.path.join(root, file)
					relpath = os.path.relpath(fullpath, self.path)
					self.filter_files[fullpath] = relpath

	def executeTokenize(self):
		for fullpath, relpath in self.filter_files.iteritems():
			self._executeTokenize(fullpath, relpath)

		self.optimizer.endTokenize()

	def _executeTokenize(self, path, relpath):
		self.file = open(path)
		self.optimizer.executeTokenize(relpath, self.file.readline)
		self.file.close()

		print 'tokenizer completed, %s' % path

	def executeVisit(self):
		for fullpath, relpath in self.filter_files.iteritems():
			self.file = open(fullpath)
			tree = ast.parse(self.file.read())
			self.optimizer.executeVisit(relpath, tree)
			print 'vistor completed, %s' % fullpath

		self.optimizer.endVisit()

	def executeTransform(self):
		modifys = {}

		for fullpath, relpath in self.filter_files.iteritems():
			self.file = open(fullpath)
			tree = ast.parse(self.file.read())
			modify = self.optimizer.executeTransform(relpath, tree)
			if True or tree.dirty:
				self.unparse(fullpath, tree)
			print 'transformer completed, %s' % fullpath

	def unparse(self, path, tree):
		src = '\n'.join(['# -*- coding:utf-8 -*-', unparser.unparse(tree)])
		# print src
		open(path, 'w').write(src)
