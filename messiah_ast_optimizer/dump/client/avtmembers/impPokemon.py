# -*- coding:utf-8 -*-


class AvatarMember(object, ):
    func = 1
    Property('combatPokemonId', '')
    Property('shadowPokemonId', '')

    def getCombatPokemon(self):
        return EntityManager.getentity(self.combatPokemonId)
