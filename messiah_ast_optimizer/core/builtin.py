# -*- coding:utf-8 -*-

from module_loader import ModuleLoader
from exception import MEvalException


class Builtin(object):
	_delegates = {}

	@classmethod
	def delegate(cls, _delegate):
		cls._delegates[_delegate.__name__] = _delegate
		_delegate.__builtin_delegate__ = True

		return _delegate

	@classmethod
	def get(cls):
		return cls._delegates


delegate = Builtin.delegate


@delegate
def __import__(frame, name, globals, locals=None, fromlist=None, level=-1):
	module = globals.get('__module__', None)
	if not module:
		raise MEvalException('__import__ with no __module__')

	return ModuleLoader().load(name.asConstant(), fromlist, level, caller=module)


@delegate
def globals(frame):
	return frame.f_globals


@delegate
def any(seq):
    for x in seq:
        if x:
            return True
    return False


if __name__ == '__main__':
	pass
