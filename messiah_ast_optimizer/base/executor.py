# -*- coding:utf-8 -*-

from utils import enum, compare_path
from file import LazyFile

import os
import ast


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

		self.nodes = {}

	def execute(self):
		self.executeTokenize()
		self.executeVisit()
		self.executeTransform()

	def executeTokenize(self):
		for root, dirs, files in os.walk(self.path, topdown=True):
			dirs[:] = [d for d in dirs if os.path.normpath(os.path.join(root, d)) not in self.ignore_dirs]

			for file in files:
				if not file.endswith('.py'):
					continue

				self._executeTokenize(os.path.join(root, file))
		self.optimizer.endTokenize()

	def _executeTokenize(self, path):
		file = open(path)
		self.optimizer.executeTokenize(path, file.readline)

		file.seek(0)
		tree = ast.parse(file.read())
		self.nodes[path] = tree

	def executeVisit(self):
		for path, tree in self.nodes.iteritems():
			self.optimizer.visit(tree, path)
		self.optimizer.endVisit()

	def executeTransform(self):
		modifys = {}

		for path, tree in self.nodes.iteritems():
			modify = self.optimizer.transform(tree, path)
			if tree.dirty:
				modifys[path] = tree
