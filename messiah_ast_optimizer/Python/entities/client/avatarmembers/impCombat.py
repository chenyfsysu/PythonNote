# -*- coding:utf-8 -*-

import const

class AvatarMember(object):
	Property("ai")
	CombatType = const.COMBATUNIT_TYPE_AVT

	def updateAllVisible(self):
		ModelSeqLoader().RefreshDismiss()

	def doAttack(self):
		print 'impCombat AvatarMember'


class PlayerAvatarMember(AvatarMember):
	def doAttack(self):
		print 'impCombat PlayerAvatarMember'
