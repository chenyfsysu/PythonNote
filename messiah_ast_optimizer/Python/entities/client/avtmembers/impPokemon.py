# -*- coding:utf-8 -*-

import const
from Model import Model

class AvatarMember(object, ):
    Property('combatPokemonId', '')
    Property('shadowPokemonId', '')

    def getCombatPokemon(self):
        return EntityManager.getentity(self.combatPokemonId)

    def rebuildPokemon(self):
    	return True
