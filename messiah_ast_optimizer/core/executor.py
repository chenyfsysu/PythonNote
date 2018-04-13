# -*- coding:utf-8 -*-

import os
import sys
import argparse
import logging
import importlib


class OptimizeExecutor(object):
	LOG_LEVEL = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
	COMMAND_SETTING = {
		'loglevel': 'LOG_LEVEL',
	}

	def __init__(self, optimizer):
		self.optimizer = optimizer

	def execute(self):
		root, path, settings, cmd_settings = self.loadCommandConfig()
		optimizer = self.optimizer(root, path, settings, cmd_settings)
		optimizer.optimize()

	def loadCommandConfig(self):
		parser = argparse.ArgumentParser()
		parser.add_argument('root', help='the root dir of optimize project')
		parser.add_argument('--path', help='file or dir to optimize relative to root')
		parser.add_argument('--settings', default='setting', help='setting files')
		parser.add_argument('--loglevel', type=str, choices=self.LOG_LEVEL, help='log level')
		args = parser.parse_args()

		root = args.root
		path = os.path.join(root, args.path) if args.path else root
		setting = importlib.import_module(args.settings)
		cmd_settings = {}

		if args.loglevel:
			args.loglevel = getattr(logging, args.loglevel)

		for name in self.COMMAND_SETTING:
			val = getattr(args, name)
			if val is not None:
				cmd_settings[self.COMMAND_SETTING[name]] = val

		return root, path, setting, cmd_settings
