# -*- coding:utf-8 -*-


class AvatarMember(object, ):
    Property('combatPokemonId', '')
    Property('shadowPokemonId', '')

    def getCombatPokemon(self):
        return EntityManager.getentity(self.combatPokemonId)
