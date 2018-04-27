# -*- coding:utf-8 -*-

import const
import avtmembers
from data import skill_data

class iBuff(object, ):

    @inline
    def getIgnoreCombatPropsOnly(self):
        return self.dataGetter('ignoreCombatPropsOnly', 0)

class iBuffs(object, ):

    def calcConvertProps(self):
        res = set()
        combatPropsOnly = self.getCombatPropsOnly()
        for buff in self.itervalues():
            if (combatPropsOnly and (not buff.dataGetter('ignoreCombatPropsOnly', 0))):
                continue
            data = buff.data
            attrconverts = data.get('attrconverts', ())
            for attrconvert in attrconverts:
                res.add(attrconvert)
        return res

class AvatarModelComponent(object, ):

    def getModelScale(self):
        if self.monster_shapeshift:
            if self.buffs.needCombatprotoScale():
                return CMD.data.get(self.monster_shapeshift, {}).get('Scale', 1.0)
        elif self.model_shapeshift:
            return self.buffs.ModelShapeShiftScale()
        return school_data.data.get(self.school, {}).get('Scale', 1.0)

@with_tag('IsAvatar')
@Components(AvatarModelComponent, *avtmembers.importall())
class Avatar(ClientAreaEntity, ):
    Property('school')
    USE = 'cCombatUnit'

    def checkSFXVisible(self):
        return True

    @inline
    def func(self, a, b, c):
        return skill_data.get(self.id, {}).get(b, c)

    def call(self):
        name = 'coco'
        b = 22
        positive = skill_data.get(buff.id, {}).get(b, name)

@Components(*avtmembers.importall())
class PlayerAvatar(object, ):
    pass
