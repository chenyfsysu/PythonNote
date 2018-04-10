# -*- coding:utf-8 -*-

import const
import avtmembers

def Components(*components, **kwargs):
    pass

class iCombatUnit(object, ):

    def useSkill(self):
        print 'iCombatUnit'

    def doAttack(self):
        print 'iCombatUnit'

class cCombatUnit(iCombatUnit, ):
    USE = 'cCombatUnit'

    def useSkill(self):
        print 'cCombatUnit'

class AvatarRoleComponent(cCombatUnit, ):

    def checkBloodbarVisible(self):
        if self.isInCJBattle():
            return True
        return False

    def checkTopNameVisible(self):
        return cRole.checkTopNameVisible.im_func(self)

    def checkSFXVisible(self):
        return True

class AvatarModelComponent(object, ):

    def getModelScale(self):
        if self.monster_shapeshift:
            if self.buffs.needCombatprotoScale():
                return CMD.data.get(self.monster_shapeshift, {}).get('Scale', 1.0)
        elif self.model_shapeshift:
            return self.buffs.ModelShapeShiftScale()
        return school_data.data.get(self.school, {}).get('Scale', 1.0)

@Components(AvatarModelComponent, AvatarRoleComponent, *avtmembers.importall())
class Avatar(ClientAreaEntity, ):
    Property('combatPokemonId', '')
    Property('shadowPokemonId', '')
    USE = 'cCombatUnit'

    def rebuildPokemon(self):
        return True

    def getModelScale(self):
        if self.monster_shapeshift:
            if self.buffs.needCombatprotoScale():
                return CMD.data.get(self.monster_shapeshift, {}).get('Scale', 1.0)
        elif self.model_shapeshift:
            return self.buffs.ModelShapeShiftScale()
        return school_data.data.get(self.school, {}).get('Scale', 1.0)

    def doAttack(self):
        pass

    def checkSFXVisible(self):
        return True

    def checkBloodbarVisible(self):
        if self.isInCJBattle():
            return True
        return False

    def useSkill(self):
        print 'cCombatUnit'

    def getCombatPokemon(self):
        return EntityManager.getentity(self.combatPokemonId)

    def checkTopNameVisible(self):
        return cRole.checkTopNameVisible.im_func(self)
