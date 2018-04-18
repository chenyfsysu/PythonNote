# -*- coding:utf-8 -*-

import const
import const
import avtmembers

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
    Property('ai')
    CombatType = const.COMBATUNIT_TYPE_AVT
    func = 1
    Property('combatPokemonId', '')
    Property('shadowPokemonId', '')

    def getModelScale(self):
        if self.monster_shapeshift:
            if self.buffs.needCombatprotoScale():
                return CMD.data.get(self.monster_shapeshift, {}).get('Scale', 1.0)
        elif self.model_shapeshift:
            return self.buffs.ModelShapeShiftScale()
        return school_data.data.get(self.school, {}).get('Scale', 1.0)

    def updateAllVisible(self):
        ModelSeqLoader().RefreshDismiss()

    def doAttack(self):
        print 'impCombat AvatarMember'

    def getCombatPokemon(self):
        return EntityManager.getentity(self.combatPokemonId)

    @name.setter
    def name(self, name):
        pass

class PlayerAvatar(object, ):
    pass
    Property('ai')
    CombatType = const.COMBATUNIT_TYPE_AVT

    def updateAllVisible(self):
        ModelSeqLoader().RefreshDismiss()

    def doAttack(self):
        print 'impCombat PlayerAvatarMember'
