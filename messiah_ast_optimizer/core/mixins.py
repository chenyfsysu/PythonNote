# -*- coding:utf-8 -*-

import os
import time
import logging
import utils

from exception import MConfigException


class LogHandlerMixin(object):
	def __init__(self):
		self.create_time = time.strftime("%Y%m%d_%H%M%S")

	def getLogger(self, name):
		logger = logging.getLogger(name)
		logger.setLevel(self.config.LOG_LEVEL)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		
		fhanlder = logging.FileHandler('log/%s.log' % self.create_time, encoding='utf8')
		fhanlder.setFormatter(formatter)
		logger.addHandler(fhanlder)

		shandler = logging.StreamHandler()
		shandler.setFormatter(formatter)
		logger.addHandler(shandler)

		return logger


class Config(object):
	def __init__(self, setting, overide):
		self.names = set()
		for name in dir(setting):
			if name.isupper():
				setattr(self, name, getattr(setting, name))
				self.names.add(name)
		self.overide(overide)

	def overide(self, settings):
		for name, setting in settings.iteritems():
			if name .isupper():
				setattr(self, name, setting)
				self.names.add(name)


class ConfigHandlerMixin(object):
	def __init__(self, root, setting, cmd_settings):
		self.config = Config(setting, cmd_settings)

		self.check()
		self.formatPath(root)

	def check(self):
		if not self.config.SYS_PATH_ROUTINE:
			raise MConfigException('Setting of SYS_PATH_ROUTINE must be specified to optimze')

	def formatPath(self, root):
		self.config.IGNORE_DIRS = [utils.format_path(root, _path) for _path in self.config.IGNORE_DIRS]
		self.config.IGNORE_FILES = [utils.format_path(root, _path) for _path in self.config.IGNORE_FILES]
		self.config.INLINE_CONST = [utils.format_path(root, _path) for _path in self.config.INLINE_CONST]
		self.config.CONFIG_INLINE_CONST = [utils.format_path(root, _path) for _path in self.config.CONFIG_INLINE_CONST]
		self.config.INLINE_CONST_FILES = [utils.format_path(root, _path) for _path in self.config.INLINE_CONST_FILES]

		routines = []
		for path, sys_path in self.config.SYS_PATH_ROUTINE:
			routines.append((utils.format_path(root, path), [utils.format_path(root, _path) for _path in sys_path]))
		self.config.SYS_PATH_ROUTINE = routines

	def getSysPath(self, file):
		for dir, path in self.config.SYS_PATH_ROUTINE:
			if utils.is_parent_dir(dir, file):
				return path

		raise MConfigException('file of %s is not define sys path' % file)


class ModifyHandlerMixin(object):
	pass
