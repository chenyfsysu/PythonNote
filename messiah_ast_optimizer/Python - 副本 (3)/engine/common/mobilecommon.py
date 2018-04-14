# -*- coding:utf-8 -*-

import cPickle
import os
import sys
import zlib
import imp

def import_asiocore(name):
    import common
    if (name in sys.modules):
        return sys.modules[name]
    dirname = os.path.dirname(os.path.realpath(__file__))
    if common.USE_STABLE_SO:
        path = os.path.abspath(('%s/../Lib/%s_stable.so' % (dirname, name)))
    else:
        path = os.path.abspath(('%s/../Lib/%s.so' % (dirname, name)))
    with open(path) as file:
        return imp.load_module(name, file, path, ('.so', 'rb', imp.C_EXTENSION))
if (sys.maxsize > (2 << 31)):
    if (os.environ.get('CLIENT_ASYNC') == 'True'):
        import asiocore_client_64 as asiocore
    else:
        asiocore = import_asiocore('asiocore_64')
elif (os.environ.get('CLIENT_ASYNC') == 'True'):
    import asiocore_client as asiocore
else:
    asiocore = import_asiocore('asiocore')
assert asiocore
COMPONENT = ('Client' if getattr(asiocore, 'IS_CLIENT_ONLY', False) else 'Server')
PY_BUILT_TYPES = {int, long, list, dict, tuple, float, set, frozenset, property, bool, str, unicode}
EMPTY_DICT = {}

def is_py_built_in_type(obj):
    '\n\t\xe5\x88\xa4\xe6\x96\xad\xe5\xaf\xb9\xe8\xb1\xa1\xe6\x98\xaf\xe5\x90\xa6\xe6\x98\xafPython\xe5\x86\x85\xe7\xbd\xae\xe7\xb1\xbb\xe3\x80\x82\n\n\t:param obj: \xe5\xbe\x85\xe5\x88\xa4\xe6\x96\xad\xe5\xaf\xb9\xe8\xb1\xa1\xe3\x80\x82\n\t:type obj: object\n\t:returns:  \xe5\xaf\xb9\xe8\xb1\xa1\xe6\x98\xaf\xe5\x90\xa6\xe6\x98\xafPython\xe5\x86\x85\xe7\xbd\xae\xe7\xb1\xbb\xe3\x80\x82\n\t:rtype: bool\n\t'
    return (type(obj) in PY_BUILT_TYPES)

def compress(obj):
    return zlib.compress(cPickle.dumps(obj, (-1)))

def decompress(val):
    return cPickle.loads(zlib.decompress(val))

class Swallower(object, ):

    def __init__(self, *args, **kwargs):
        pass

    def __getattr__(self, name):
        return self

    def __call__(self, *args, **kwargs):
        return self

    def __add__(self, other):
        return 0

    def __sub__(self, other):
        return self

    def __mul__(self, other):
        return 1

    def __div__(self, other):
        return 1

    def __getitem__(self, index):
        return self

    def __neg__(self):
        return (-1)

    def __iter__(self):
        return self

    def next(self):
        raise StopIteration()

class NonexistentSwallower(Swallower, ):

    def __nonzero__(self):
        return False

def DO_NOTHING(*arg, **kwargs):
    pass
