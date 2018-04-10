# -*- coding:utf-8 -*-

import _cPickle
import _datetime
import _gc
import _itertools
import _marshal
import _math
import _operator
import _sys
import _thread
import _time
import _zlib


def setup(loader):
	_cPickle.setup(loader)
	_datetime.setup(loader)
	_gc.setup(loader)
	_itertools.setup(loader)
	_marshal.setup(loader)
	_math.setup(loader)
	_operator.setup(loader)
	_sys.setup(loader)
	_thread.setup(loader)
	_time.setup(loader)
	_zlib.setup(loader)
