# -*- coding:utf-8 -*-

'\n:py:func:`rpc_method` \xe4\xb8\xad\xe4\xbd\xbf\xe7\x94\xa8\xe5\x88\xb0\xe7\x9a\x84\xe5\x8f\x82\xe6\x95\xb0\xe3\x80\x82\n\n... seealso:: :py:mod:`engine.common.rpcdecorator`\xe3\x80\x82\n'
from common.IdManager import IdManager

class ConvertError(ValueError, ):
    '\n\tRPC\xe8\xb0\x83\xe7\x94\xa8\xe4\xb8\xad\xe7\x9a\x84\xe5\x8f\x82\xe6\x95\xb0\xe8\xbd\xac\xe6\x8d\xa2\xe5\xbc\x82\xe5\xb8\xb8\xe3\x80\x82\n\t'
    pass

class RpcMethodArg(object, ):
    '\n\tRPC\xe5\x8f\x82\xe6\x95\xb0\xe7\x9a\x84\xe5\x9f\xba\xe7\xb1\xbb\xe3\x80\x82\n\t'

    def __init__(self, name=None):
        '\n\t\t:param name: \xe8\xaf\xa5\xe5\x8f\x82\xe6\x95\xb0\xe7\x9a\x84\xe5\x90\x8d\xe7\xa7\xb0\xef\xbc\x8c\xe7\xbc\xba\xe7\x9c\x81\xe6\x97\xb6\xe4\xbb\xa5\xe8\xaf\xa5\xe5\x8f\x82\xe6\x95\xb0\xe5\x9c\xa8RPC\xe5\x8f\x82\xe6\x95\xb0\xe5\x88\x97\xe8\xa1\xa8\xe4\xb8\xad\xe7\x9a\x84\xe5\xba\x8f\xe5\x8f\xb7\xe4\xb8\xba\xe5\x90\x8d\xe3\x80\x82\n\t\t:type name: str\n\t\t'
        super(RpcMethodArg, self).__init__()
        self.name = name

    def getname(self):
        '\n\t\t\xe8\x8e\xb7\xe5\x8f\x96\xe5\x8f\x82\xe6\x95\xb0\xe5\x90\x8d\xe3\x80\x82\n\n\t\t:returns: \xe5\x8f\x82\xe6\x95\xb0\xe5\x90\x8d\xe3\x80\x82\n\t\t:rtype: str/int\n\t\t'
        return self.name

    def convert(self, data):
        raise ConvertError('Not implemented!')

    def get_type(self):
        raise ConvertError('Not implemented!')

    def genametype(self):
        return ('%s(%s)' % (self.getname(), self.get_type()))

    def default_val(self):
        raise StandardError('Not implemented!')

    def tostr(self, value):
        return str(value)

    def __str__(self):
        return self.genametype()

    def convert_error(self, data):
        return ConvertError(('Cannot Convert Arg %s To Type %s With Data [%r]' % (self.name, self.get_type(), data)))

class NoLimit(object, ):

    def isvalide(self, _data):
        return True

    def __str__(self):
        return ''

class NumeralLimit(object, ):

    def __init__(self, min=None, max=None, range=None):
        super(NumeralLimit, self).__init__()
        self.min = min
        self.max = max
        self.range = range

    def isvalide(self, data):
        if ((self.min is not None) and (data < self.min)):
            return False
        if ((self.max is not None) and (data > self.max)):
            return False
        if ((self.range is not None) and (data not in self.range)):
            return False
        return True

    def __str__(self):
        extra = ''
        if ((self.min is not None) or (self.max is not None)):
            extra = '['
            if (self.min is not None):
                extra += str(self.min)
            extra += '-'
            if (self.max is not None):
                extra += str(self.max)
            extra += ']'
        elif (self.range is not None):
            extra = repr(list(self.range)).replace(' ', '')
        return extra

class NumberArg(RpcMethodArg, ):
    '\xe6\x95\xb0\xe5\x80\xbc\xe7\xb1\xbb\xe5\x8f\x82\xe6\x95\xb0\xe7\x9a\x84\xe5\x9f\xba\xe7\xb1\xbb'

    def __init__(self, min=None, max=None, range=None, name=None):
        '\n\t\t:param min: \xe5\x85\x81\xe8\xae\xb8\xe4\xbc\xa0\xe5\x85\xa5\xe7\x9a\x84\xe6\x9c\x80\xe5\xb0\x8f\xe5\x80\xbc\xe3\x80\x82\n\t\t:param max: \xe5\x85\x81\xe8\xae\xb8\xe4\xbc\xa0\xe5\x85\xa5\xe7\x9a\x84\xe6\x9c\x80\xe5\xa4\xa7\xe5\x80\xbc\xe3\x80\x82\n\t\t:param range: \xe5\x85\x81\xe8\xae\xb8\xe4\xbc\xa0\xe5\x85\xa5\xe7\x9a\x84\xe8\x8c\x83\xe5\x9b\xb4\xe3\x80\x82\n\t\t:param name: \xe5\x8f\x82\xe6\x95\xb0\xe5\x90\x8d\xe7\xa7\xb0\xe3\x80\x82\n\t\t'
        super(NumberArg, self).__init__(name)
        if ((min is not None) or (max is not None) or (range is not None)):
            self.limit = NumeralLimit(min, max, range)

    def convert(self, data):
        try:
            d = self.converter(data)
        except:
            raise ConvertError(('Cannot Covert [%r] To Type %s' % (data, self.get_type())))
        if (hasattr(self, 'limit') and (not self.limit.isvalide(data))):
            raise ConvertError(('[%r] Exceeds Limit Of Type %s' % (data, self.get_type())))
        return d

class Int(NumberArg, ):
    'int\xe5\x9e\x8b\xe5\x8f\x82\xe6\x95\xb0\xe3\x80\x82'

    def convert(self, data):
        assert isinstance(data, int), self.convert_error(data)
        return int(data)

    def get_type(self):
        return (('Int' + str(self.limit)) if hasattr(self, 'limit') else 'Int')

    def default_val(self):
        return 0

class Long(NumberArg, ):
    'long\xe5\x9e\x8b\xe5\x8f\x82\xe6\x95\xb0\xe3\x80\x82'

    def convert(self, data):
        assert (isinstance(data, long) or isinstance(data, int)), self.convert_error(data)
        return long(data)

    def get_type(self):
        return (('Long' + str(self.limit)) if hasattr(self, 'limit') else 'Long')

    def default_val(self):
        return long(0)

class Float(NumberArg, ):
    'float\xe5\x9e\x8b\xe5\x8f\x82\xe6\x95\xb0\xe3\x80\x82'

    def convert(self, data):
        assert (isinstance(data, float) or isinstance(data, int)), self.convert_error(data)
        return float(data)

    def get_type(self):
        return (('Float' + str(self.limit)) if hasattr(self, 'limit') else 'Float')

    def default_val(self):
        return 0.0

class Str(RpcMethodArg, ):
    'str\xe5\x9e\x8b\xe5\x8f\x82\xe6\x95\xb0\xe3\x80\x82'

    def convert(self, data):
        assert (isinstance(data, str) or isinstance(data, unicode)), self.convert_error(data)
        return str(data)

    def get_type(self):
        return 'Str'

    def default_val(self):
        return ''

class BinData(RpcMethodArg, ):
    '\xe4\xba\x8c\xe8\xbf\x9b\xe5\x88\xb6\xe4\xb8\xb2\xe3\x80\x82'

    def convert(self, data):
        assert isinstance(data, str), self.convert_error(data)
        return data

    def get_type(self):
        return 'BinData'

    def default_val(self):
        return ''

class List(RpcMethodArg, ):
    'list\xe5\x9e\x8b\xe5\x8f\x82\xe6\x95\xb0\xe3\x80\x82'

    def convert(self, data):
        assert isinstance(data, list), self.convert_error(data)
        return data

    def get_type(self):
        return 'List'

    def default_val(self):
        return []

class Tuple(RpcMethodArg, ):
    'tuple\xe5\x9e\x8b\xe5\x8f\x82\xe6\x95\xb0\xe3\x80\x82'

    def convert(self, data):
        if (not isinstance(data, list)):
            self.convert_error(data)
        return tuple(data)

    def get_type(self):
        return 'Tuple'

    def default_val(self):
        return ()

class Dict(RpcMethodArg, ):
    'dict\xe5\x9e\x8b\xe5\x8f\x82\xe6\x95\xb0\xe3\x80\x82'

    def convert(self, data):
        assert isinstance(data, dict), self.convert_error(data)
        return data

    def get_type(self):
        return 'Dict'

    def default_val(self):
        return {}

class Bool(RpcMethodArg, ):
    'bool\xe5\x9e\x8b\xe5\x8f\x82\xe6\x95\xb0\xe3\x80\x82'

    def convert(self, data):
        try:
            return bool(data)
        except:
            raise self.convert_error(data)

    def get_type(self):
        return 'Bool'

    def default_val(self):
        return False

class EntityID(RpcMethodArg, ):
    'EntityID\xe5\x9e\x8b\xe5\x8f\x82\xe6\x95\xb0\xe3\x80\x82'

    def convert(self, data):
        if (data is None):
            return ''
        assert IdManager.is_valid_id(data), self.convert_error(data)
        return data

    def get_type(self):
        return 'EntityID'

    def default_val(self):
        return ''

class Exposed(EntityID, ):

    def get_type(self):
        return 'Exposed'

class CustomType(RpcMethodArg, ):
    'CustomType\xe5\x9e\x8b\xe5\x8f\x82\xe6\x95\xb0\xe3\x80\x82'

    def __init__(self, typ, name=None):
        super(CustomType, self).__init__(name)
        self.typ = typ

    def convert(self, data):
        return self.typ(data)

    def get_type(self):
        return self.typ.__name__

    def default_val(self):
        return self.typ()
from mobilecommon import COMPONENT
if (COMPONENT == 'Server'):
    from mobilecommon import asiocore

    class Proxy(RpcMethodArg, ):
        ':py:class:`engine.server.SeverDummy.EntityProxy` \xe5\xaf\xb9\xe8\xb1\xa1'

        def convert(self, data):
            assert (isinstance(data, asiocore.base_mailbox) or (not data)), self.convert_error(data)
            return (data or '')

        def get_type(self):
            return 'Proxy'

        def default_val(self):
            return None

    class MailBox(RpcMethodArg, ):
        ':py:class:`engine.server.SeverDummy.EntityMailBox` \xe5\xaf\xb9\xe8\xb1\xa1'

        def convert(self, data):
            assert (isinstance(data, asiocore.cell_mailbox) or (not data)), self.convert_error(data)
            return (data or '')

        def get_type(self):
            return 'MailBox'

        def default_val(self):
            return None

    class Delegate(RpcMethodArg, ):
        ':py:class:`engine.server.SeverDummy.EntityMailBox` \xe6\x88\x96 :py:class:`engine.server.SeverDummy.EntityProxy` \xe5\xaf\xb9\xe8\xb1\xa1'

        def convert(self, data):
            assert (isinstance(data, asiocore.base_mailbox) or isinstance(data, asiocore.cell_mailbox) or (not data)), self.convert_error(data)
            return (data or '')

        def get_type(self):
            return 'Delegate'

        def default_val(self):
            return None
