# -*- coding:utf-8 -*-

import sys
import argparse
import importlib


class OptimizeExecutor(object):
	CmdSetting = {
		'loglevel': 'LOG_LEVEL',
	}

	def __init__(self, optimizer):
		self.optimizer = optimizer

	def execute(self):
		path, settings, cmd_settings = self.loadCommandConfig()
		optimizer = self.optimizer(path, settings, cmd_settings)
		optimizer.optimize()

	def loadCommandConfig(self):
		parser = argparse.ArgumentParser()
		parser.add_argument('path', help='file or dir to optimize')
		parser.add_argument('--settings', default='setting', help='setting files')
		parser.add_argument('--loglevel')
		args = parser.parse_args()

		path = args.path
		setting = importlib.import_module(args.settings)
		cmd_settings = {}

		for name in self.CmdSetting:
			val = getattr(args, name)
			if val is not None:
				cmd_settings[self.CmdSetting[name]] = val

		return path, setting, cmd_settings
