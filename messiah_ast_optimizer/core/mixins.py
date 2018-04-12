# -*- coding:utf-8 -*-

import logging
import time

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
	def __init__(self, setting):
		for name in dir(setting):
			val = getattr(setting, name)
			setattr(self, name, val)

	def overide(self, settings):
		for name, setting in settings.iteritems():
			setattr(self, name, setting)


class ConfigHandlerMixin(object):
	def __init__(self, setting, cmd_settings):
		self.config = Config(setting)
		self.config.overide(cmd_settings)

		if not self.config.SYS_PATH_MAPPING:
			raise MConfigException('Setting of SYS_PATH_MAPPING must be specified to optimze')



class ModifyHandlerMixin(object):
	pass
