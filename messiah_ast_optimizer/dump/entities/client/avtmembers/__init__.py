# -*- coding:utf-8 -*-


def importall():
    return (__import__('impPokemon', globals()), __import__('impCombat', globals()))
