# -*- coding:utf-8 -*-


class MException(Exception):
	pass

class MEvalException(Exception):
	pass


class MLoadNameException(Exception):
	pass


class MImportException(MException):
	pass


class MMroResolutionException(MException):
	pass


class MUnpackSequenceException(MException):
	pass
