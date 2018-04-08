# -*- coding:utf-8 -*-

import sys
from common.EntityManager import EntityManager
from common.IdManager import IdManager
from common.classutils import ComponentHost, PropertyMetaClass
from common.mobilecommon import asiocore, NonexistentSwallower
from mobilelog.LogManager import LogManager
import Timer

class EntityMetaClass(PropertyMetaClass, ):

    def __new__(cls, name, bases, dct):
        entityclass = super(EntityMetaClass, cls).__new__(cls, name, bases, dct)
        entityclass.logger = LogManager.get_logger(entityclass.__name__)
        EntityMetaClass.replaceDestroy(entityclass)
        EntityMetaClass.replaceInitFromDict(entityclass)
        return entityclass

    @staticmethod
    def replaceInitFromDict(entityclass):
        _entity_init_from_dict = entityclass.init_from_dict.im_func
        while hasattr(_entity_init_from_dict, '_entity_init_from_dict'):
            _entity_init_from_dict = _entity_init_from_dict._entity_init_from_dict

        def init_from_dict(self, *args, **kwargs):
            try:
                _entity_init_from_dict(self, *args, **kwargs)
            except:
                ((not self.is_destroyed()) and self.destroy())
                raise 
        init_from_dict._entity_init_from_dict = _entity_init_from_dict
        entityclass.init_from_dict = init_from_dict

    @staticmethod
    def replaceDestroy(entityclass):
        _entity_destroy = entityclass.destroy.im_func
        while hasattr(_entity_destroy, '_entity_destroy'):
            _entity_destroy = _entity_destroy._entity_destroy
        if hasattr(entityclass, '_on_destroy'):

            def destroy(self, *args, **kwargs):
                try:
                    return (self._on_destroy(*args, **kwargs) and _entity_destroy(self, *args, **kwargs))
                except:
                    try:
                        entityclass.logger.error('Failed To Destroy Entity %s(%s)', entityclass.__name__, self.id)
                        sys.excepthook(*sys.exc_info())
                    except:
                        pass
                    ((not self.is_destroyed()) and self.destroyObject())
        else:

            def destroy(self, *args, **kwargs):
                try:
                    return _entity_destroy(self, *args, **kwargs)
                except:
                    try:
                        entityclass.logger.error('Failed To Destroy Entity %s(%s)', entityclass.__name__, self.id)
                        sys.excepthook(*sys.exc_info())
                    except:
                        pass
                    ((not self.is_destroyed()) and self.destroyObject())
        destroy._entity_destroy = _entity_destroy
        entityclass.destroy = destroy

@ComponentHost
class Entity(getattr(asiocore, 'entity', object), ):
    '\n\t\xe6\xb8\xb8\xe6\x88\x8f\xe4\xb8\xad\xe6\x89\x80\xe6\x9c\x89\xe5\xae\x9e\xe4\xbd\x93\xe5\xaf\xb9\xe8\xb1\xa1\xe7\x9a\x84\xe9\x80\x9a\xe7\x94\xa8\xe5\x9f\xba\xe7\xb1\xbb\xe3\x80\x82\n\n\t\xe8\xaf\xa5\xe7\xb1\xbb\xe5\x85\x81\xe8\xae\xb8\xe4\xbd\xbf\xe7\x94\xa8\xe5\x85\xb6\xe5\xae\x83\xe7\xb1\xbb\xe4\xbd\x9c\xe4\xb8\xba\xe8\xaf\xa5\xe7\xb1\xbb\xe7\x9a\x84\xe7\xbb\x84\xe4\xbb\xb6\xef\xbc\x8c\xe7\xbb\x84\xe4\xbb\xb6\xe7\xb1\xbb\xe7\x9a\x84\xe5\x90\x84\xe6\x96\xb9\xe6\xb3\x95\xe5\x8f\x8a\xe7\xb1\xbb\xe5\x8f\x98\xe9\x87\x8f\xe5\xb0\x86\xe8\xa2\xab\xe5\xa4\x8d\xe5\x88\xb6\xe8\x87\xb3\xe8\xaf\xa5\xe7\xb1\xbb\xef\xbc\x8c\xe7\x94\xb1\xe6\xad\xa4\xe7\xbb\x84\xe5\x90\x88\xe4\xb8\xba\xe4\xb8\x80\xe4\xb8\xaa\xe5\xae\x8c\xe6\x95\xb4\xe7\x9a\x84\xe7\xb1\xbb\xe3\x80\x82\n\t\xe7\xbb\x84\xe4\xbb\xb6\xe7\xb1\xbb\xe9\x80\x9a\xe8\xbf\x87 :func:`Components` \xe4\xbf\xae\xe9\xa5\xb0\xe7\xac\xa6\xe5\xa3\xb0\xe6\x98\x8e\xe3\x80\x82\n\n\t\xe8\xaf\xa5\xe7\xb1\xbb\xe6\x94\xaf\xe6\x8c\x81\xe7\x94\xb1 :func:`Property` \xe5\xa3\xb0\xe6\x98\x8e\xe7\x9a\x84\xe5\xb1\x9e\xe6\x80\xa7\xef\xbc\x8c\xe6\xad\xa4\xe7\xb1\xbb\xe5\xb1\x9e\xe6\x80\xa7\xe5\xb0\x86\xe5\x9c\xa8 :func:`init_from_dict` \xe4\xb8\xad\xe8\x87\xaa\xe5\x8a\xa8\xe5\x88\x9d\xe5\xa7\x8b\xe5\x8c\x96\xe3\x80\x82\n\n\t.. note:: \xe8\xaf\xa5\xe7\xb1\xbb\xe7\x9a\x84\xe5\x85\x83\xe7\xb1\xbb\xe4\xb8\xba :class:`PropertyMetaClass` \xe3\x80\x82\n\t'
    __metaclass__ = EntityMetaClass

    @classmethod
    def onEntityClassRegistered(klass):
        '\n\t\t\xe8\xaf\xa5\xe7\xb1\xbb\xe8\xa2\xab\xe6\xb3\xa8\xe5\x86\x8c\xe8\x87\xb3 :class:`EntityManager` \xe6\x97\xb6\xe7\x9a\x84\xe5\x9b\x9e\xe8\xb0\x83\xe3\x80\x82\n\t\t'
        pass

    def __init__(self, entityid=''):
        '\n\t\t\xe8\xaf\xa5\xe5\x87\xbd\xe6\x95\xb0\xe5\xb0\x86\xe5\x88\x9d\xe5\xa7\x8b\xe5\x8c\x96\xe8\xaf\xa5\xe5\xae\x9e\xe4\xbe\x8b\xef\xbc\x8c\xe5\xb0\x86\xe5\xae\x9e\xe4\xbe\x8b\xe6\xb3\xa8\xe5\x86\x8c\xe8\x87\xb3 :class:`EntityManager`\n\n\t\t:param entityid: \xe6\xaf\x8f\xe4\xb8\xaaEntity\xe5\x94\xaf\xe4\xb8\x80\xe7\x8b\xac\xe6\x9c\x89\xe7\x9a\x84\xe6\xa0\x87\xe8\xaf\x86\xe7\xac\xa6\xe3\x80\x82\xe8\xaf\xa5\xe5\x8f\x82\xe6\x95\xb0\xe4\xb8\xbaNone\xe6\x88\x96\xe7\xbc\xba\xe7\x9c\x81\xe6\x97\xb6\xef\xbc\x8c\xe5\xb0\x86\xe7\x94\xb1 :func:`IdManager.genid` \xe7\x94\x9f\xe6\x88\x90\xe6\x96\xb0ID\xe3\x80\x82\n\t\t:type entityid: entityid/None\n\t\t'
        super(Entity, self).__init__()
        self._is_deactive = False
        self._is_destroyed = False
        self.id = (entityid or IdManager.genid())
        EntityManager.addentity(self.id, self, False)
        self._timers = {}
        self._tick_timer = 0

    def init_from_dict(self, bdict):
        '\n\t\t\xe4\xbb\xa5\xe5\xa4\x96\xe9\x83\xa8\xe6\x95\xb0\xe6\x8d\xae\xe5\xad\x97\xe5\x85\xb8\xe5\xaf\xb9\xe8\xaf\xa5\xe7\xb1\xbb\xe8\xbf\x9b\xe8\xa1\x8c\xe7\x9a\x84\xe5\x88\x9d\xe5\xa7\x8b\xe5\x8c\x96\xe3\x80\x82\n\n\t\t\xe8\xaf\xa5\xe5\x87\xbd\xe6\x95\xb0\xe5\x9c\xa8\xe7\x88\xb6\xe7\xb1\xbb\xe7\x9a\x84\xe5\x88\x9d\xe5\xa7\x8b\xe5\x8c\x96\xe5\xae\x8c\xe6\x88\x90\xe5\x90\x8e\xef\xbc\x8c\xe5\xb0\x86\xe4\xbe\x9d\xe6\xac\xa1\xe6\x89\xa7\xe8\xa1\x8c\xe4\xb8\x8b\xe5\x88\x97\xe5\x8a\xa8\xe4\xbd\x9c\xef\xbc\x9a\n\t\t1. \xe8\xb0\x83\xe7\x94\xa8\xe5\x90\x84\xe7\xbb\x84\xe4\xbb\xb6\xe7\x9a\x84 :func:`__init_component__` \xe5\x87\xbd\xe6\x95\xb0\xef\xbc\x9b\n\t\t2. \xe5\x88\x9d\xe5\xa7\x8b\xe5\x8c\x96\xe7\x94\xb1 :func:`Property` \xe5\xa3\xb0\xe6\x98\x8e\xe7\x9a\x84\xe5\x90\x84\xe5\xb1\x9e\xe6\x80\xa7\xef\xbc\x9b\n\t\t3. \xe8\xb0\x83\xe7\x94\xa8\xe5\x90\x84\xe7\xbb\x84\xe4\xbb\xb6\xe7\x9a\x84 :func:`__post_component__` \xe5\x87\xbd\xe6\x95\xb0\xe3\x80\x82\n\n\t\t:param bdict: \xe5\x88\x9d\xe5\xa7\x8b\xe5\x8c\x96\xe6\x95\xb0\xe6\x8d\xae\xe5\xad\x97\xe5\x85\xb8\xef\xbc\x8c\xe7\x94\xb1\xe6\x9c\xac\xe5\x9c\xb0API\xe6\x88\x96RPC\xe4\xbc\xa0\xe6\x9d\xa5\xe3\x80\x82\n\t\t:type bdict: dict\n\t\t'
        self._callComponents('init', bdict)
        self.area.prop()._initProperty(bdict)
        self._callComponents('post', bdict)

    def setdefault(self, key, dft):
        pass

    def destroy(self):
        '\n\t\t\xe9\x94\x80\xe6\xaf\x81\xe8\xaf\xa5\xe5\xae\x9e\xe4\xbe\x8b\xe3\x80\x82\n\n\t\t\xe8\xaf\xa5\xe5\x87\xbd\xe6\x95\xb0\xe5\xb0\x86\xe8\xb0\x83\xe7\x94\xa8\xe5\x90\x84\xe7\xbb\x84\xe4\xbb\xb6\xe7\x9a\x84 :func:`__fini_component__` \xe5\x87\xbd\xe6\x95\xb0\xe3\x80\x82\n\n\t\t.. note:: \xe5\x87\xbd\xe6\x95\xb0\xe4\xbc\x9a\xe5\xb0\x86 self.__dict__ \xe6\xb8\x85\xe7\xa9\xba\xef\xbc\x8c\xe4\xbb\xa5\xe4\xbf\x9d\xe8\xaf\x81\xe5\xbd\xa2\xe5\xa6\x82 self.xx.owner = self \xe7\x9a\x84\xe5\xbe\xaa\xe7\x8e\xaf\xe5\xbc\x95\xe7\x94\xa8\xe5\x8f\xaf\xe4\xbb\xa5\xe6\xad\xa3\xe7\xa1\xae\xe5\x9b\x9e\xe6\x94\xb6\xe3\x80\x82\n\t\t'
        self._callComponents('fini')
        self.destroyObject()

    def deactive(self):
        self._is_deactive = True
        self.set_tick(None)
        for timerid in self._timers:
            Timer.cancel_timer(timerid)
        self._timers = {}
        self.add_timer = self.add_repeat_timer = self._on_timer = NonexistentSwallower()

    def is_deactived(self):
        return self._is_deactive

    def destroyObject(self):
        '\n\t\t\xe9\x94\x80\xe6\xaf\x81\xe8\xaf\xa5\xe5\xaf\xb9\xe8\xb1\xa1\xe3\x80\x82\n\n\t\t\xe4\xbb\x85\xe9\x94\x80\xe6\xaf\x81\xe8\xaf\xa5\xe5\xaf\xb9\xe8\xb1\xa1\xe5\x8f\x8a\xe5\x85\xb6\xe5\x9c\xa8 :class:`EntityManager` \xe5\x8f\x8atimer\xe4\xb8\xad\xe7\x9a\x84\xe5\xbc\x95\xe7\x94\xa8\xe7\xad\x89\xef\xbc\x8c\xe4\xb8\x8d\xe4\xbc\x9a\xe8\xb0\x83\xe7\x94\xa8\xe5\x90\x84\xe7\xbb\x84\xe4\xbb\xb6\xe7\x9a\x84 :func:`__fini_component__` \xe5\x87\xbd\xe6\x95\xb0\xe3\x80\x82\n\n\t\t.. note:: \xe5\x87\xbd\xe6\x95\xb0\xe4\xbc\x9a\xe5\xb0\x86 self.__dict__ \xe6\xb8\x85\xe7\xa9\xba\xef\xbc\x8c\xe4\xbb\xa5\xe4\xbf\x9d\xe8\xaf\x81\xe5\xbd\xa2\xe5\xa6\x82 self.xx.owner = self \xe7\x9a\x84\xe5\xbe\xaa\xe7\x8e\xaf\xe5\xbc\x95\xe7\x94\xa8\xe5\x8f\xaf\xe4\xbb\xa5\xe6\xad\xa3\xe7\xa1\xae\xe5\x9b\x9e\xe6\x94\xb6\xe3\x80\x82\n\t\t'
        self.deactive()
        entityid = self.id
        EntityManager.delentity(entityid)
        self.area = None
        self.__dict__.clear()
        self.id = entityid
        self._is_deactive = True
        self._is_destroyed = True

    def is_destroyed(self):
        '\n\t\t\xe8\xbf\x94\xe5\x9b\x9e\xe8\xaf\xa5\xe5\xae\x9e\xe4\xbe\x8b\xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe7\xbb\x8f\xe5\xa4\x84\xe4\xba\x8e\xe8\xa2\xab\xe9\x94\x80\xe6\xaf\x81\xef\xbc\x88\xe4\xbd\x86Python\xe5\xb0\x9a\xe6\x9c\xaa\xe5\x9b\x9e\xe6\x94\xb6\xef\xbc\x89\xe7\x8a\xb6\xe6\x80\x81\xe3\x80\x82\n\n\t\t:returns: \xe8\x8b\xa5\xe5\xb7\xb2\xe5\xa4\x84\xe4\xba\x8e\xe8\xa2\xab\xe9\x94\x80\xe6\xaf\x81\xe7\x8a\xb6\xe6\x80\x81\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9eTrue\xef\xbc\x8c\xe5\x90\xa6\xe5\x88\x99\xe8\xbf\x94\xe5\x9b\x9eFalse\xe3\x80\x82\n\t\t:rtype: bool\n\t\t'
        return self._is_destroyed

    def set_tick(self, period):
        '\n\t\t\xe8\xae\xbe\xe7\xbd\xaeTick\xe5\x91\xa8\xe6\x9c\x9f\xe3\x80\x82\n\n\t\t:param period: Tick\xe5\x91\xa8\xe6\x9c\x9f\xef\xbc\x8c\xe5\x8d\x95\xe4\xbd\x8d\xe4\xb8\xba\xe7\xa7\x92\xe3\x80\x82\n\t\t:type period: float\n\t\t'
        if self._tick_timer:
            self.cancel_timer(self._tick_timer)
        if period:
            self._tick_timer = self.add_repeat_timer(period, (lambda : self.tick(period)))

    def tick(self, dtime):
        '\n\t\tTick\xe5\x9b\x9e\xe8\xb0\x83\xef\xbc\x8c\xe5\x91\xa8\xe6\x9c\x9f\xe7\x94\xb1 :func:`set_tick` \xe8\xae\xbe\xe5\xae\x9a\xe3\x80\x82\n\n\t\t\xe8\xaf\xa5\xe5\x87\xbd\xe6\x95\xb0\xe5\xb0\x86\xe8\xb0\x83\xe7\x94\xa8\xe5\x90\x84\xe7\xbb\x84\xe4\xbb\xb6\xe7\x9a\x84 :func:`__tick_component__` \xe5\x87\xbd\xe6\x95\xb0\xe3\x80\x82\n\n\t\t:param dtime: \xe5\xbd\x93\xe5\x89\x8dTick\xe5\x91\xa8\xe6\x9c\x9f\xe3\x80\x82\n\t\t:type dtime: float\n\t\t'
        self._tickComponents(dtime)

    def add_timer(self, delay, func):
        '\n\t\t\xe6\xb7\xbb\xe5\x8a\xa0\xe4\xb8\x80\xe6\xac\xa1\xe6\x80\xa7\xe5\xae\x9a\xe6\x97\xb6\xe5\x99\xa8\xe3\x80\x82\n\n\t\t:param delay: \xe8\xa7\xa6\xe5\x8f\x91\xe5\x91\xa8\xe6\x9c\x9f\xef\xbc\x8c\xe5\x8d\x95\xe4\xbd\x8d\xe4\xb8\xba\xe7\xa7\x92\xe3\x80\x82\n\t\t:type delay: float\n\t\t:param func: \xe8\xa7\xa6\xe5\x8f\x91\xe6\x97\xb6\xe9\x9c\x80\xe8\xa6\x81\xe5\x9b\x9e\xe8\xb0\x83\xe7\x9a\x84\xe5\x87\xbd\xe6\x95\xb0\xe3\x80\x82\n\t\t:type func: callable object\n\t\t:returns: \xe5\xae\x9a\xe6\x97\xb6\xe5\x99\xa8ID\xef\xbc\x8c\xe5\x8f\xaf\xe7\x94\xa8\xe4\xba\x8e\xe5\x8f\x96\xe6\xb6\x88\xe8\xaf\xa5\xe5\xae\x9a\xe6\x97\xb6\xe5\x99\xa8\xef\xbc\x8c\xe4\xb8\x80\xe6\xac\xa1\xe6\x80\xa7\xe5\xae\x9a\xe6\x97\xb6\xe5\x99\xa8\xe7\x9a\x84ID\xe5\xbf\x85\xe5\xae\x9a\xe4\xb8\xba\xe6\xad\xa3\xe5\x80\xbc\xe3\x80\x82\n\t\t:rtype: int/long\n\t\t'
        timerid = Timer.add_callback(delay, False, self._on_timer)
        self._timers[timerid] = func
        return timerid

    def add_repeat_timer(self, delay, func):
        '\n\t\t\xe6\xb7\xbb\xe5\x8a\xa0\xe5\x91\xa8\xe6\x9c\x9f\xe6\x80\xa7\xe5\xae\x9a\xe6\x97\xb6\xe5\x99\xa8\xe3\x80\x82\n\n\t\t:param delay: \xe6\xaf\x8f\xe6\xac\xa1\xe8\xa7\xa6\xe5\x8f\x91\xe5\x91\xa8\xe6\x9c\x9f\xef\xbc\x8c\xe5\x8d\x95\xe4\xbd\x8d\xe4\xb8\xba\xe7\xa7\x92\xe3\x80\x82\n\t\t:type delay: float\n\t\t:param func: \xe6\xaf\x8f\xe6\xac\xa1\xe8\xa7\xa6\xe5\x8f\x91\xe6\x97\xb6\xe9\x9c\x80\xe8\xa6\x81\xe5\x9b\x9e\xe8\xb0\x83\xe7\x9a\x84\xe5\x87\xbd\xe6\x95\xb0\xe3\x80\x82\n\t\t:type func: callable object\n\t\t:returns: \xe5\xae\x9a\xe6\x97\xb6\xe5\x99\xa8ID\xef\xbc\x8c\xe5\x8f\xaf\xe7\x94\xa8\xe4\xba\x8e\xe5\x8f\x96\xe6\xb6\x88\xe8\xaf\xa5\xe5\xae\x9a\xe6\x97\xb6\xe5\x99\xa8\xef\xbc\x8c\xe5\x91\xa8\xe6\x9c\x9f\xe6\x80\xa7\xe5\xae\x9a\xe6\x97\xb6\xe5\x99\xa8\xe7\x9a\x84ID\xe5\xbf\x85\xe5\xae\x9a\xe4\xb8\xba\xe8\xb4\x9f\xe5\x80\xbc\xe3\x80\x82\n\t\t:rtype: int/long\n\t\t'
        timerid = Timer.add_callback(delay, True, self._on_timer)
        self._timers[timerid] = func
        return timerid

    def _on_timer(self, timerid):
        '\n\t\t\xe5\xae\x9a\xe6\x97\xb6\xe5\x99\xa8\xe5\xbc\x95\xe6\x93\x8e\xe5\x9b\x9e\xe8\xb0\x83\xe3\x80\x82\n\t\t\xe8\xaf\xa5\xe5\x87\xbd\xe6\x95\xb0\xe7\x94\xb1 :func:`TimerProxy.tick()` \xe8\xa7\xa6\xe5\x8f\x91\xef\xbc\x8c\xe5\xb0\x86\xe5\x9c\xa8\xe6\xb8\x85\xe9\x99\xa4\xe7\x9b\xb8\xe5\xba\x94\xe5\xae\x9a\xe6\x97\xb6\xe5\x99\xa8\xe8\xae\xb0\xe5\xbd\x95\xe5\x90\x8e\xe8\xb0\x83\xe7\x94\xa8\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x97\xb6\xe4\xbc\xa0\xe5\x85\xa5\xe7\x9a\x84\xe5\x8e\x9f\xe5\xae\x9a\xe6\x97\xb6\xe5\x99\xa8\xe5\x9b\x9e\xe8\xb0\x83\xe3\x80\x82\n\n\t\t:param timerid: \xe5\xae\x9a\xe6\x97\xb6\xe5\x99\xa8ID\xe3\x80\x82\n\t\t:type timerid: int/long\n\t\t'
        if Timer.is_repeat_timer(timerid):
            self._timers[timerid]()
        else:
            self._timers.pop(timerid)()

    def cancel_timer(self, timerid):
        '\n\t\t\xe5\x8f\x96\xe6\xb6\x88\xe5\xae\x9a\xe6\x97\xb6\xe5\x99\xa8\xe3\x80\x82\n\n\t\t:param timerid: \xe5\xae\x9a\xe6\x97\xb6\xe5\x99\xa8ID\xe3\x80\x82\n\t\t:type timerid: int/long\n\n\t\t.. warning:: \xe5\x88\x87\xe5\x8b\xbf\xe4\xba\x8e\xe8\xa7\xa6\xe5\x8f\x91\xe7\x9a\x84\xe5\xae\x9a\xe6\x97\xb6\xe5\x99\xa8\xe5\x9b\x9e\xe8\xb0\x83\xe5\x87\xbd\xe6\x95\xb0\xe4\xb8\xad\xe8\xb0\x83\xe7\x94\xa8\xe6\xad\xa4\xe5\x87\xbd\xe6\x95\xb0\xe5\x8f\x96\xe6\xb6\x88\xe6\xad\xa3\xe5\x9c\xa8\xe8\xa2\xab\xe8\xa7\xa6\xe5\x8f\x91\xe7\x9a\x84\xe5\xae\x9a\xe6\x97\xb6\xe5\x99\xa8\xe3\x80\x82\n\t\t'
        self._timers.pop(timerid)
        Timer.cancel_timer(timerid)

    def __str__(self):
        if self._is_destroyed:
            return ('%s(%s)(D)' % (self.__class__.__name__, self.id))
        else:
            return ('%s(%s)' % (self.__class__.__name__, self.id))

    def __repr__(self):
        return ('<%s>' % self)
