# -*- coding:utf-8 -*-

from engine import Components




class CombatMember(object, ):

    def func(self):
        pass

class PokemonMember(object, ):
    A = 1

@Components(PokemonMember, CombatMember)
class Avatar(object, ):
    A = 1

    def func(self):
        pass
