# -*- coding:utf-8 -*-

class cBuffs(object):
	def __init__(self):
		self.data = dict({'CommonEffectArgs': 'EffectCom/buff_shutup_jh:biped Head:-1:110000:p0,-0.1,-0.5:s1.2,1.1,1.1', 'Desc': '沉默，无法释放部分技能。', 'Effect': 2, 'Icon': 'UI_bufficon_cm.png', 'Name': '沉默', 'NegType': 1, 'SubType': 1, 'Type': 2, 'iNoSkill': 2})

	def getGeneralIcon(self):
		return self.data.get('general_icon', '')

	def func1(self):
		if self.getGeneralIcon():
			pass

	def func2(self):
		if self.data.get('general_icon', ''):
			pass


buff = cBuffs()
a = buff.func1
b = buff.func2

import timeit
print timeit.Timer('a()', 'from __main__ import a').timeit()
print timeit.Timer('b()', 'from __main__ import b').timeit()
