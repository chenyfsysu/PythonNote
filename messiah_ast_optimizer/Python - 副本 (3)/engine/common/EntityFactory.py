# -*- coding:utf-8 -*-

import inspect
from IdManager import IdManager
from RpcIndex import PRESET_RPC_INDEXES, register_rpc
from mobilelog.LogManager import LogManager
from rpcdecorator import is_exposed_rpc

class EntityFactory(object, ):
    '\n\t\xe7\xae\xa1\xe7\x90\x86\xe6\x89\x80\xe6\x9c\x89\xe7\x9a\x84Entity\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe5\xb7\xa5\xe5\x8e\x82\xe5\x8d\x95\xe4\xbb\xb6\xe7\xb1\xbb\xe3\x80\x82\n\t'
    _instance = None

    def __init__(self):
        super(EntityFactory, self).__init__()
        self.logger = LogManager.get_logger('server.EntityFactory')
        self.entity_classes = {}

    @classmethod
    def instance(cls):
        if (cls._instance is None):
            cls._instance = EntityFactory()
        return cls._instance

    def register_entity(self, entitytype, entityclass):
        '\n\t\t\xe6\xb3\xa8\xe5\x86\x8centity\xe7\xb1\xbb\xe3\x80\x82\xe5\x9c\xa8\xe6\xad\xa4\xe6\xb3\xa8\xe5\x86\x8c\xe8\xbf\x87\xe7\x9a\x84\xe7\xb1\xbb\xe6\x89\x8d\xe8\x83\xbd\xe8\xbf\x9b\xe8\xa1\x8cRPC\xe8\xb0\x83\xe7\x94\xa8\xe3\x80\x82\n\n\t\t:param entitytype: Entity\xe7\xb1\xbb\xe5\x90\x8d\xe3\x80\x82\n\t\t:type entitytype: str\n\t\t:param entityclass: Entity\xe7\xb1\xbb\xe3\x80\x82\n\t\t:type entityclass: class\n\t\t'
        if (not PRESET_RPC_INDEXES):
            for (name, member) in inspect.getmembers(entityclass, predicate=inspect.ismethod):
                if is_exposed_rpc(member):
                    register_rpc(name)
        self.entity_classes[entitytype] = entityclass
        entityclass.onEntityClassRegistered()

    def get_entity_class(self, entitytype):
        '\n\t\t\xe8\x8e\xb7\xe5\x8f\x96entity\xe7\xb1\xbb\xe3\x80\x82\n\n\t\t:param entitytype: Entity\xe7\xb1\xbb\xe5\x90\x8d\xe3\x80\x82\n\t\t:type entitytype: str\n\t\t:returns: Entity\xe7\xb1\xbb\xe3\x80\x82\n\t\t:rtype: class\n\t\t'
        EntityClass = None
        if isinstance(entitytype, str):
            EntityClass = self.entity_classes.get(entitytype, None)
        elif isinstance(entitytype, type):
            EntityClass = entitytype
        return EntityClass

    def create_entity(self, entitytype, entityid=None):
        '\n\t\t\xe5\x88\x9b\xe5\xbb\xbaEntity\n\n\t\t:param entitytype: \xe5\xbe\x85\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84Entity\xe7\xb1\xbb\xe5\x90\x8d\xe3\x80\x82\n\t\t:type entitytype: str\n\t\t:param entityid: \xe5\xbe\x85\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84Entity ID\xef\xbc\x8c\xe7\xbc\xba\xe7\x9c\x81\xe6\x97\xb6\xe5\xb0\x86\xe4\xbc\x9a\xe7\x94\x9f\xe6\x88\x90\xe6\x96\xb0\xe7\x9a\x84ID\xe3\x80\x82\n\t\t:type entityid: entityid/None\n\t\t:returns: \xe8\x8b\xa5\xe5\x88\x9b\xe5\xbb\xba\xe6\x88\x90\xe5\x8a\x9f\xef\xbc\x8c\xe5\x88\x99\xe8\xbf\x94\xe5\x9b\x9e\xe6\x96\xb0\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe5\xaf\xb9\xe8\xb1\xa1\xef\xbc\x9b\xe5\x90\xa6\xe5\x88\x99\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9eNone\xe3\x80\x82\n\t\t:rtype: entity/None\n\t\t'
        EntityClass = self.get_entity_class(entitytype)
        if (not EntityClass):
            self.logger.error('Cannot Find Entity Type %s ID (%s)', str(entitytype), IdManager.id2str(entityid))
            return None
        return EntityClass(entityid)

    def reregister_rpc(self):
        for entityclass in self.entity_classes.itervalues():
            for (name, member) in inspect.getmembers(entityclass, predicate=inspect.ismethod):
                if is_exposed_rpc(member):
                    register_rpc(name)
