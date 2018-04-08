# -*- coding:utf-8 -*-

class Builtin(object):
	_handlers = {}

	@classmethod
	def handler(cls, _handler):
		cls._handlers[_handler.__name__] = _handler

		return _handler

	@classmethod
	def get(cls):
		return cls._handler()


@Builtin.handler
def __import__(frame, name, globals=None, locals=None, fromlist=None, level=-1):
	pass


@Builtin.handler
def globals(frame):
	return frame.f_globals


@Builtin.handler
def any(seq):
    for x in seq:
        if x:
            return True
    return False


if __name__ == '__main__':
	pass
