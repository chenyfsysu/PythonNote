# -*- coding:utf-8 -*-

import inspect
import re
import sys
from mobilecommon import COMPONENT, asiocore, is_py_built_in_type

def _addComponent(klass, component):
    for (i, base) in enumerate(klass.__components__):
        if issubclass(component, base):
            klass.__components__[i] = component
            tick = getattr(component, '__tick_component__', None)
            if tick:
                tick = tick.im_func
                basetick = getattr(base, '__tick_component__', None)
                if (basetick in klass.__component_ticks__):
                    klass.__component_ticks__[klass.__component_ticks__.index(basetick)] = tick
                else:
                    klass.__component_ticks__.append(tick)
            break
    else:
        klass.__components__.append(component)
        tick = getattr(component, '__tick_component__', None)
        (tick and klass.__component_ticks__.append(tick.im_func))
    module = getattr(component, '__module__', None)
    if ((not getattr(sys, 'reloading', False)) and module):
        module = sys.modules[module]
        (hasattr(module, klass.__name__) and setattr(module, klass.__name__, klass))
    for (name, func) in inspect.getmembers(component, inspect.ismethod):
        if ((not (name.startswith('__') and name.endswith('__'))) and (name != '_addComponent') and (name != '_delComponent')):
            setattr(klass, name, func.im_func)
    for (name, member) in inspect.getmembers(component, is_py_built_in_type):
        if ((not name.startswith('__')) or ((not name.endswith('__')) and (name != '_addComponent') and (name != '_delComponent'))):
            setattr(klass, name, member)
    _mergeProperties(klass, component)
    return True

def _delComponent(klass, component):
    assert (component in klass.__components__)
    _popProperties(klass, component)
    klass.__components__.remove(component)
    tick = getattr(component, '__tick_component__', None)
    if tick:
        klass.__component_ticks__.remove(tick.im_func)
    for (name, _) in inspect.getmembers(component, is_py_built_in_type):
        if ((not name.startswith('__')) or (not name.endswith('__'))):
            delattr(klass, name)
    for (name, _) in inspect.getmembers(component, inspect.ismethod):
        if (not (name.startswith('__') and name.endswith('__'))):
            delattr(klass, name)
    return True

def _callComponents(self, name, *args, **kwargs):
    funcname = ('__%s_component__' % name)
    for component in self.__components__:
        func = getattr(component, funcname, None)
        (func and func.im_func(self, *args, **kwargs))

def _tickComponents(self, dtime):
    for func in self.__component_ticks__:
        func(self, dtime)

def ComponentHost(klass):
    klass.__components__ = []
    klass.__component_ticks__ = []
    if (not hasattr(klass, '_addComponent')):
        klass._addComponent = classmethod(_addComponent)
        klass._delComponent = classmethod(_delComponent)
        klass._callComponents = _callComponents
        klass._tickComponents = _tickComponents
    for base in klass.__bases__:
        if hasattr(base, '__components__'):
            klass.__components__.extend(base.__components__)
            klass.__component_ticks__.extend(base.__component_ticks__)
    return klass

def Components(*components, **kwargs):

    def _Components(klass):
        membername = (kwargs.get('postfix', '%sMember') % klass.__name__)
        klass = ComponentHost(klass)
        for component in components:
            if inspect.isclass(component):
                klass._addComponent(component)
            elif inspect.ismodule(component):
                for (name, component) in inspect.getmembers(component, inspect.isclass):
                    if (name == membername):
                        klass._addComponent(component)
                        break
            else:
                raise RuntimeError(('Something Strange Slip Into Components: %s (type %s).' % (component, type(component))))
        return klass
    return _Components

def get_defaults(self):
    defaults = {}
    for (name, default) in self.__property_all__.iteritems():
        if isCustomType(default):
            default = default({})
        defaults[name] = default
    return defaults

def _initClassWityProperty(dict_or_class):
    if (type(dict_or_class) == dict):
        if ('__property_all__' not in dict_or_class):
            dict_or_class['__property_all__'] = {}
            dict_or_class['__property_flag__'] = {}
            dict_or_class['__property_delay__'] = {}
    elif (not hasattr(dict_or_class, '__property_all__')):
        dict_or_class.__property_all__ = {}
        dict_or_class.__property_flag__ = {}
        dict_or_class.__property_delay__ = {}

def _initPropertyWithValueType(self, data):
    for (name, value) in (data.iteritems() if (not hasattr(data, 'normal_iteritems')) else data.normal_iteritems()):
        default = self.__property_all__.get(name, None)
        if (default is not None):
            if isCustomType(default):
                setattr(self, name, default(value))
            else:
                setattr(self, name, value)
        else:
            self[name] = self.VALUE_TYPE(value)

def _initPropertyWithNoneValueType(self, data):
    for (name, value) in (data.iteritems() if (not hasattr(data, 'normal_iteritems')) else data.normal_iteritems()):
        default = self.__property_all__.get(name, None)
        if (default is not None):
            if isCustomType(default):
                setattr(self, name, default(value))
            else:
                setattr(self, name, value)
        else:
            self[name] = value

def _initPropertyWithOutValueType(self, data):
    for (name, value) in (data.iteritems() if (not hasattr(data, 'normal_iteritems')) else data.normal_iteritems()):
        default = self.__property_all__.get(name, None)
        if (default is not None):
            if isCustomType(default):
                setattr(self, name, default(value))
            else:
                setattr(self, name, value)

def _lenWithValueType(self):
    return (super(CustomMapType, self).total_size() - len(self.__property_all__))

def _nonzeroWithOutValueType(self):
    return True

class PropertyMetaClass(type, ):

    def __new__(cls, name, bases, dct):
        _initClassWityProperty(dct)
        is_custom_type = dct.get('IS_CUSTOM_TYPE', False)
        for base in bases:
            if hasattr(base, '__property_all__'):
                dct['__property_all__'].update({k: v for (k, v) in base.__property_all__.iteritems() if (k not in dct['__property_all__'])})
                dct['__property_flag__'].update({k: v for (k, v) in base.__property_flag__.iteritems() if (k not in dct['__property_flag__'])})
                dct['__property_delay__'].update({k: v for (k, v) in base.__property_delay__.iteritems() if (k not in dct['__property_delay__'])})
            if (hasattr(base, 'VALUE_TYPE') and ('VALUE_TYPE' not in dct)):
                dct['VALUE_TYPE'] = getattr(base, 'VALUE_TYPE')
            is_custom_type = (is_custom_type or getattr(base, 'IS_CUSTOM_TYPE', False))
        if is_custom_type:
            if (name == 'CustomMapType'):
                dct['_initProperty'] = _initPropertyWithNoneValueType
                dct['__len__'] = _lenWithValueType
            elif ('VALUE_TYPE' in dct):
                dct['__len__'] = _lenWithValueType
                if dct['VALUE_TYPE']:
                    dct['_initProperty'] = _initPropertyWithValueType
                else:
                    dct['_initProperty'] = _initPropertyWithNoneValueType
            else:
                dct['_initProperty'] = _initPropertyWithOutValueType
                dct['__nonzero__'] = _nonzeroWithOutValueType
        newcls = super(PropertyMetaClass, cls).__new__(cls, name, bases, dct)
        if is_custom_type:
            asiocore.patch_area_map(newcls)
        return newcls
VALID_PROPERTY_NAME = re.compile('^[_A-Za-z][_0-9A-Za-z]*$')

def Property(name, default=0, flag=1, delay=0):
    if (not VALID_PROPERTY_NAME.match(name)):
        raise AttributeError(('Bad Property Name [%r]' % name))
    if (flag == Property.MANUAL):
        return
    classLocals = sys._getframe(1).f_locals
    _initClassWityProperty(classLocals)
    assert isinstance(flag, int)
    assert (name not in classLocals['__property_all__'])
    classLocals['__property_all__'][name] = default
    classLocals['__property_flag__'][name] = flag
    classLocals['__property_delay__'][name] = delay
Property.MANUAL = 0
Property.SERVER_ONLY = 1
Property.OWN_CLIENT = 2
Property.ALL_CLIENTS = 4
Property.PERSISTENT = 8
Property.STRDATA = 32
ComponentWithoutProperty = object
'\n\xe4\xb8\x8d\xe5\xb8\xa6\xe6\x9c\x89\xe5\xb1\x9e\xe6\x80\xa7\xe7\x9a\x84Component\xe7\x9a\x84\xe5\x9f\xba\xe7\xb1\xbb\xe3\x80\x82\n'

class ComponentWithProperty(object, ):
    '\n\t\xe5\xb8\xa6\xe6\x9c\x89\xe5\xb1\x9e\xe6\x80\xa7\xe7\x9a\x84Component\xe7\x9a\x84\xe5\x9f\xba\xe7\xb1\xbb\xef\xbc\x8c\xe4\xbf\xae\xe6\x94\xb9\xe4\xba\x86__metaclass__\xe4\xbb\xa5\xe6\x94\xaf\xe6\x8c\x81\xe5\xb1\x9e\xe6\x80\xa7\xe7\xad\x89\xe5\x8a\x9f\xe8\x83\xbd\xe3\x80\x82\n\t'
    __metaclass__ = PropertyMetaClass

def _mergeProperties(dst, src):
    if hasattr(src, '__property_all__'):
        _initClassWityProperty(dst)
        dst.__property_all__.update(src.__property_all__)
        dst.__property_flag__.update(src.__property_flag__)
        dst.__property_delay__.update(src.__property_delay__)

def _popProperties(dst, src):
    if hasattr(src, '__property_all__'):
        for prop in src.__property_all__:
            dst.__property_all__.pop(prop, None)
        for prop in src.__property_flag__:
            dst.__property_flag__.pop(prop, None)
        for prop in src.__property_delay__:
            dst.__property_delay__.pop(prop, None)

class CustomMapTypeMetaClass(PropertyMetaClass, type(asiocore.area_map), ):
    pass

class CustomMapType(asiocore.area_map, ):
    __metaclass__ = CustomMapTypeMetaClass
    IS_CUSTOM_TYPE = True

    def __init__(self, data={}):
        super(CustomMapType, self).__init__(data)
        ((data or isinstance(data, CustomMapType)) and self._initProperty(data))

    def __str__(self):
        return ('{%s}' % ', '.join((('%s: %s' % item) for item in self.iteritems())))

    def __repr__(self):
        return ('%s({%s})' % (self.__class__.__name__, ', '.join((('%r: %r' % item) for item in self.iteritems()))))
    if (COMPONENT == 'Client'):

        def on_init(self, parent):
            pass

        def on_setattr(self, key, old, new):
            pass

        def on_clear(self):
            pass

        def on_update(self, value):
            pass

        def on_assign(self):
            pass

    def keys(self):
        return list(self.iterkeys())

    def values(self):
        return list(self.itervalues())

    def items(self):
        return list(self.iteritems())

    def __contains__(self, item):
        return (self.get(item, None) is not None)

class CustomListType(asiocore.area_list, ):
    IS_CUSTOM_TYPE = True

    def __init__(self, data=[]):
        super(CustomListType, self).__init__()
        if data:
            self.clear()
            if hasattr(self, 'VALUE_TYPE'):
                data = (self.VALUE_TYPE(item) for item in data)
            self.extend(list(data))

    def __str__(self):
        return ('[%s]' % ', '.join((repr(item) for item in self)))

    def __repr__(self):
        return str(self)

    def remove(self, x):
        for (i, value) in enumerate(self):
            if (value == x):
                del self[i]
                return
        else:
            raise ValueError(('%s not in list' % x))
    if (COMPONENT == 'Client'):

        def on_init(self, parent):
            pass

        def on_insert(self, inx):
            pass

        def on_append(self):
            pass

        def on_clear(self):
            pass

        def on_update(self, inx, old):
            pass

        def on_pop(self, inx, old):
            pass

        def on_extend(self, inx):
            pass

        def on_assign(self):
            pass

def isCustomType(klass):
    return getattr(klass, 'IS_CUSTOM_TYPE', False)

def isCustomTypeObj(obj):
    return (isinstance(obj, CustomMapType) or isinstance(obj, CustomListType))

def get_props_stype(klass):
    desc = {}
    stype = getattr(klass, 'VALUE_TYPE', None)
    if stype:
        desc['type'] = klass
        desc['stype'] = get_props_stype(stype)
    props = get_props_desc(klass)
    if (len(props) > 0):
        desc['type'] = klass
        desc['props'] = props
    if (len(desc) > 0):
        return desc
    return klass

def get_props_desc(klass):
    desc = {}
    for (name, default) in getattr(klass, '__property_all__', {}).iteritems():
        customtype = None
        if isCustomType(default):
            customtype = default
        sub_customtype = getattr(customtype, 'VALUE_TYPE', None)
        if sub_customtype:
            sub_customtype = get_props_stype(sub_customtype)
        if (inspect.isclass(default) and issubclass(default, CustomMapType)):
            custom_props = get_props_desc(default)
        else:
            custom_props = {}
        delay = klass.__property_delay__.get(name, 0)
        desc[name] = {'flag': klass.__property_flag__[name], 'delay': delay, 'type': customtype, 'stype': sub_customtype, 'props': custom_props}
    return desc
