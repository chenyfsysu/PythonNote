# -*- coding:utf-8 -*-

import sys
import __builtin__


def enum(*sequential, **named):
	enums = dict(zip(sequential, range(len(sequential))), **named)
	enums['__enum__'] = enums.keys()
	return type('Enum', (), enums)


__builtin__.enum = enum

sys.path.append('lib')
