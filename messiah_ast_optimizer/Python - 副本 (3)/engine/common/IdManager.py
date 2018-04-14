# -*- coding:utf-8 -*-

'\nEntityID \xe7\x94\x9f\xe6\x88\x90\xe5\x99\xa8\xe3\x80\x82\n'
from mobilecommon import COMPONENT
if (COMPONENT == 'Client'):
    from base64 import b64encode
    from bson.objectid import ObjectId
else:
    from common.mobilecommon import asiocore
    area_objectid = asiocore.area_objectid

class IdManager(object, ):
    '\n\t\xe4\xba\xa7\xe7\x94\x9f\xe4\xbb\xa5Base64\xe7\xbc\x96\xe7\xa0\x81\xe7\x9a\x84EntityID\xe3\x80\x82\n\tEntityID\xe6\x98\xaf\xe4\xb8\x80\xe4\xb8\xaa\xe9\x95\xbf\xe5\xba\xa6\xe4\xb8\xba16\xe5\xad\x97\xe8\x8a\x82str\xef\xbc\x8c\xe7\xa9\xbaID\xe4\xbb\xa5""\xe8\xa1\xa8\xe7\xa4\xba\xe3\x80\x82\n\t'
    if (COMPONENT == 'Client'):

        @staticmethod
        def genid():
            return b64encode(ObjectId().binary)
    else:

        @staticmethod
        def genid():
            return area_objectid.gen64()

    @staticmethod
    def str2id(string):
        ' .. deprecated:: 18502 '
        return string

    @staticmethod
    def id2str(uid):
        ' .. deprecated:: 18502 '
        return uid

    @staticmethod
    def bytes2id(bytes):
        ' .. deprecated:: 18502 '
        return bytes

    @staticmethod
    def id2bytes(uid):
        ' .. deprecated:: 18502 '
        return uid

    @staticmethod
    def is_valid_id(entityid):
        '\n\t\t\xe5\x88\xa4\xe6\x96\xadID\xe6\x98\xaf\xe5\x90\xa6\xe5\x90\x88\xe6\xb3\x95\xe3\x80\x82\n\n\t\t:param entityid: \xe5\xbe\x85\xe5\x88\xa4\xe6\x96\xad\xe7\x9a\x84ID\xe3\x80\x82\n\t\t:type entityid: EntityID\n\t\t:returns: \xe6\x98\xaf\xe5\x90\xa6\xe5\x90\x88\xe6\xb3\x95\n\t\t:rtype: boot\n\t\t'
        return (isinstance(entityid, str) and ((not entityid) or (len(entityid) == 16)))
