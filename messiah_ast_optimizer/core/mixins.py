# -*- coding:utf-8 -*-

import logging
import time


class LogHandlerMixin(object):
	def __init__(self):
		self.create_time = time.strftime("%Y%m%d_%H%M%S")
		self.log_level = logging.DEBUG

	def getLogger(self, name):
		logger = logging.getLogger(name)
		logger.setLevel(self.log_level)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		
		fhanlder = logging.FileHandler('log/%s.log' % self.create_time, encoding='utf8')
		fhanlder.setFormatter(formatter)
		logger.addHandler(fhanlder)

		shandler = logging.StreamHandler()
		shandler.setFormatter(formatter)
		logger.addHandler(shandler)

		return logger



class OptionHandlerMixin(object):
	pass



class ModifyHandlerMixin(object):
	pass
