# -*- coding: utf-8 -*-

from avatarmembers.impDoubleRide import AvatarMember, PlayerAvatarMember


class CombatPokemonMember(AvatarMember):
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


class AvatarCombatPokemonMember(PlayerAvatarMember):
	def showExtraModel(self, state):
		pass

	def hideExtraModel(self, state):
		pass
