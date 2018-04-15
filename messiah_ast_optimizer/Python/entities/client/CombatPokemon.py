# -*- coding:utf-8 -*-

from avatarmembers.impDoubleRide import AvatarMember, PlayerAvatarMember
import combatpokemonmembers

@with_tag('IsPokemon')
class CombatPokemon(ClientAreaEntity, ):
    ' \xe5\x8f\xac\xe5\x94\xa4\xe5\x85\xbd\xe7\x9a\x84\xe6\x88\x98\xe6\x96\x97\xe5\x8d\x95\xe4\xbd\x8d\xe5\xbd\xa2\xe6\x80\x81\xef\xbc\x8c\xe6\x98\xaf\xe5\x8f\xac\xe5\x94\xa4\xe5\x85\xbd\xe5\x9c\xa8\xe5\x85\xb6\xe4\xbb\x96\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe7\x9a\x84\xe8\xa1\xa8\xe7\x8e\xb0\n\t'
    Property('pokeid')
    Property('pid')
    Property('no')
    Property('star')
    Property('ownerid')
    Property('ownerName')

    @property
    def owner(self):
        return EntityManager.getentity(self.ownerid)

    @property
    def eqSchool(self):
        return self.school

    @property
    def eqBody(self):
        return self.body

    def showExtraModel(self, state):
        pass

    def hideExtraModel(self, state):
        pass
