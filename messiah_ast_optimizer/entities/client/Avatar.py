# -*- coding:utf-8 -*-

from avtmembers.impPokemon import AvatarMember
import const


class iCombatUnit(object):
    def useSkill(self):
        print 'iCombatUnit'

    def doAttack(self):
        print 'iCombatUnit'



class cCombatUnit(iCombatUnit):
    USE  = 'cCombatUnit'
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

@with_tag('IsAvatar')
@Components(AvatarModelComponent, AvatarRoleComponent, AvatarMember)
class Avatar(ClientAreaEntity, ):
    Property('school')
    Property('uid')
    Property('hates', AvatarHates)
    Property('xw')
    Property('origin_account', '')
    Property('body')

    def onClick(self):
        p = GlobalData.p
        if p.isInSurvivalBattle():
            return
        if (self.id != p.id):
            if (not p.canLockTarget(self)):
                p.popNotificationMsg(1001)
            else:
                p.lockTarget(self)
            if (TasteQuery.tasteInActDuration and self.buffs.tasteCarrierNo()):
                HomePartnerDialogue().show(self.id, 5)
