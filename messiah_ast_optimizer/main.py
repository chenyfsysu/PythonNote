# -*- coding:utf-8 -*-

from core.executor import OptimizeExecutor
from optimize import Optimizer
import argparse
import sys


sys.path.append('lib')  


def execute(path, ignore_dirs, ignore_files):
	executor = OptimizeExecutor(Optimizer(path, ignore_dirs, ignore_files))
	executor.execute()


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('path', help='Path to optimize')
	parser.add_argument('--ignore_dirs', nargs='*', help='Set ignore directory')
	parser.add_argument('--ignore_files', nargs='*', help='Set ignore directory')
	args = parser.parse_args()

	execute(args.path, args.ignore_dirs or [], args.ignore_files or [])
