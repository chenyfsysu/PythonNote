# -*- coding:utf-8 -*-

from utils import enum

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
	def __init__(self , optimizer):
		self.optimizer = optimizer

	def execute(self):
		self.optimizer.optimize()
