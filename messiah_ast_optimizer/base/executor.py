# -*- coding:utf-8 -*-

from utils import enum, compare_path
import os

os.path.sep = '/'
os.sep = '/'


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

		self.source_cache = []

	def execute(self):
		for root, dirs, files in os.walk(self.path, topdown=True):
			dirs[:] = [d for d in dirs if os.path.normpath(os.path.join(root, d)) not in self.ignore_dirs]

			for file in files:
				pass
				# self.source_cache.append(root, file, )
