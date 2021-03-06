# -*- coding:utf-8 -*-

from mobilelog.LogManager import LogManager

class EntityManager(object, ):
    '\n\t\xe7\xae\xa1\xe7\x90\x86\xe6\x89\x80\xe6\x9c\x89\xe7\x9a\x84Entity\xe7\x9a\x84\xe7\xae\xa1\xe7\x90\x86\xe5\x8d\x95\xe4\xbb\xb6\xe7\xb1\xbb\xe3\x80\x82\n\t'
    _logger = LogManager.get_logger('server.EntityManager')
    _entities = {}

    @staticmethod
    def hasentity(entityid):
        '\n\t\t\xe5\x88\xa4\xe5\xae\x9a\xe6\x98\xaf\xe5\x90\xa6\xe5\xad\x98\xe5\x9c\xa8entity\n\n\t\t:param entityid: Entity ID\xe3\x80\x82\n\t\t:type entityid: entityid\n\t\t:returns: \xe8\x8b\xa5ID\xe6\x8c\x87\xe5\xae\x9a\xe7\x9a\x84Enitity\xe5\xad\x98\xe5\x9c\xa8\xef\xbc\x8c\xe5\x88\x99\xe8\xbf\x94\xe5\x9b\x9eTrue\xef\xbc\x9b\xe5\x90\xa6\xe5\x88\x99\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9eFalse\xe3\x80\x82\n\t\t:rtype: bool\n\t\t'
        return (entityid in EntityManager._entities)

    @staticmethod
    def getentity(entityid):
        '\n\t\t\xe8\x8e\xb7\xe5\x8f\x96Entity\xe3\x80\x82\n\n\t\t:param entityid: \xe6\xac\xb2\xe8\x8e\xb7\xe5\x8f\x96\xe7\x9a\x84Entity ID\xe3\x80\x82\n\t\t:type entityid: entityid\n\t\t:returns: \xe8\x8b\xa5ID\xe6\x8c\x87\xe5\xae\x9a\xe7\x9a\x84Enitity\xe5\xad\x98\xe5\x9c\xa8\xef\xbc\x8c\xe5\x88\x99\xe8\xbf\x94\xe5\x9b\x9e\xe8\xaf\xa5Entity\xef\xbc\x9b\xe5\x90\xa6\xe5\x88\x99\xef\xbc\x8c\xe8\xbf\x94\xe5\x9b\x9eNone\xe3\x80\x82\n\t\t:rtype: entity/None\n\t\t'
        return EntityManager._entities.get(entityid, None)

    @staticmethod
    def delentity(entityid):
        '\n\t\t\xe5\x88\xa0\xe9\x99\xa4entity\n\n\t\t:param entityid: \xe5\xbe\x85\xe5\x88\xa0\xe9\x99\xa4\xe7\x9a\x84Entity ID\xe3\x80\x82\n\t\t:type entityid: entityid\n\t\t'
        try:
            del EntityManager._entities[entityid]
        except KeyError:
            EntityManager._logger.warn(" entity id %s didn't exist", entityid)

    @staticmethod
    def addentity(entityid, entity, override=True):
        '\n\t\t\xe6\xb7\xbb\xe5\x8a\xa0\xe6\x96\xb0\xe7\x9a\x84entity\n\n\t\t:param entityid: \xe6\xac\xb2\xe6\xb7\xbb\xe5\x8a\xa0\xe7\x9a\x84\xe7\x9a\x84Entity ID\xe3\x80\x82\n\t\t:type entityid: entityid\n\t\t:param entityid: \xe6\xac\xb2\xe6\xb7\xbb\xe5\x8a\xa0\xe7\x9a\x84\xe7\x9a\x84Entity\xe3\x80\x82\n\t\t:type entity: entity\n\t\t:param override: \xe8\x8b\xa5\xe4\xb8\xbaTrue\xef\xbc\x8c\xe5\x88\x99\xe5\xbd\x93\xe6\xac\xb2\xe6\xb7\xbb\xe5\x8a\xa0\xe7\x9a\x84Entity ID\xe5\xb7\xb2\xe7\xbb\x8f\xe5\xad\x98\xe5\x9c\xa8\xe6\x97\xb6\xef\xbc\x8c\xe5\x88\x99\xe5\xb0\x86\xe8\xa6\x86\xe7\x9b\x96\xe5\x8e\x9f\xe6\x9c\x89\xe7\x9a\x84Entity\xef\xbc\x9b\xe5\x90\xa6\xe5\x88\x99\xef\xbc\x8c\xe4\xb8\x8d\xe6\x89\xa7\xe8\xa1\x8c\xe5\x8a\xa8\xe4\xbd\x9c\xe3\x80\x82\n\t\t:type override: bool\n\t\t'
        if (entityid in EntityManager._entities):
            EntityManager._logger.warn('%s (%s) Already Exist', EntityManager._entities[entityid].__class__.__name__, entityid)
            (override and EntityManager._entities[entityid].destroyObject())
        EntityManager._entities[entityid] = entity
