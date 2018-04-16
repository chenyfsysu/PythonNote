# -*- coding:utf-8 -*-

import const
import avatarmembers

class AvatarModelComponent(object, ):

    def getModelScale(self):
        if self.monster_shapeshift:
            if self.buffs.needCombatprotoScale():
                return CMD.data.get(self.monster_shapeshift, {}).get('Scale', 1.0)
        elif self.model_shapeshift:
            return self.buffs.ModelShapeShiftScale()
        return school_data.data.get(self.school, {}).get('Scale', 1.0)

@with_tag('IsAvatar')
class Avatar(ClientAreaEntity, ):
    Property('school')
    USE = 'cCombatUnit'

    def checkSFXVisible(self):
        return True

class PlayerAvatar(object, ):
    pass
