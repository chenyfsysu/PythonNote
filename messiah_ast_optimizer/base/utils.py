# -*- coding:utf-8 -*-

import os


def OptimizeStep(*steps):
	def _OptimizeStep(kclass):
		kclass.__optimize_steps = steps

		return kclass

	return _OptimizeStep


def enum(*sequential, **named):
	enums = dict(zip(sequential, range(len(sequential))), **named)
	return type('Enum', (), enums)


def compare_path(src, dst):
	return os.path.normpath(src) == os.path.normpath(dst)
