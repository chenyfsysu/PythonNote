# -*- coding:utf-8 -*-


class AvatarMember(object, ):
    func = 1
    Property('combatPokemonId', '')
    Property('shadowPokemonId', '')

    def gfggg(self):
        return EntityManager.getentity(self.combatPokemonId)
