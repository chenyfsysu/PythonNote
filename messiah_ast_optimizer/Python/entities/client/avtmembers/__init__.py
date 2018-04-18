# -*- coding:utf-8 -*-


def importall():
	return (
		__import__("impCombat", globals()),
		__import__("impPokemon", globals()),
	)
