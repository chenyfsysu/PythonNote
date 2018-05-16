# -*- coding:utf-8 -*-


from collections import defaultdict
from inline_hook import inline
import functools
import random
import time
import datetime

from common.classutils import CustomMapType, Property, COMPONENT, CustomListType
from common.EntityManager import EntityManager

from txmdecorators import attr_cache
from txmdecorators import attr_inspect_cache
import GlobalData
import const
import utils

from data import buff_data
from data import buff_target_level_data as BTLD
from data import skill_magic_data as SMD
from data import props_name_id_data as PNID

# 同时最多只有一个的buff类型
SINGLE_TYPES = [
	const.BUFF_TYPE_HIT,
	const.BUFF_TYPE_SPECIAL,
	const.BUFF_TYPE_SCH_RESISTANCE,
	const.BUFF_TYPE_SCH_REINFORCE,
	const.BUFF_TYPE_CAMP_CHANGE,
	const.BUFF_TYPE_AFFECT_BUFF,
	const.BUFF_TYPE_TRANSFORM_HARM,
	const.BUFF_TYPE_SPEED_LIMIT,
	const.BUFF_TYPE_BASE_SPEED,
	const.BUFF_TYPE_SHAPESHIFT,
	const.BUFF_TYPE_CD_COOLER,
]

BUFF_DEBUG = 0


class iBuff(CustomMapType):
	Property("id",        0, Property.ALL_CLIENTS | Property.PERSISTENT)  # noqa
	Property("level",     0, Property.ALL_CLIENTS | Property.PERSISTENT)  # noqa
	Property("cooldown",  0, Property.OWN_CLIENT | Property.PERSISTENT)  # noqa
	Property("casterid", '', Property.OWN_CLIENT | Property.PERSISTENT)  # noqa
	Property('buffForbidSkills', CustomListType, Property.OWN_CLIENT)  # 技能禁掉的skillid list
	Property('powerRatio', 1, Property.ALL_CLIENTS | Property.PERSISTENT)

	def __init__(self, data={}):
		super(iBuff, self).__init__(data)
		self.initData()

	def initData(self):
		self._data = buff_data.data.get((self.id, self.level), {})
		self.dataGetter = self._data.get

	def get_owner(self):
		if hasattr(self, 'temp_owner'):
			return self.temp_owner
		return CustomMapType.get_owner(self)

	@property
	def data(self):
		return self._data

	def onEnter(self):
		owner = self.get_owner()
		if self.dataGetter("transform_harm", 0) > 0:
			owner.trans_harm_count = 0

		for skillid in self.dataGetter("clearSkillCD", ()):
			skill = owner.GetSkill(skillid, restrict=True)
			if not skill.level:
				continue
			if not skill.enable:
				continue
			owner.SetSkillCD(skill.id, time.time(), skill.getCoolDown())

	def onExit(self):
		pass

	def coolDown(self):
		return self.cooldown

	def getType(self):
		return self.dataGetter("Type", 0)

	def getSubType(self):
		return self.dataGetter("SubType", 0)

	def getEffectType(self):
		return self.dataGetter("Effect", 1)

	def getWuXingType(self):
		return self.dataGetter("WuXingType", 0)

	def isPositive(self):
		return self.dataGetter("Effect", 1) == const.BUFF_EFFECT_POSITIVE

	def isNegative(self):
		return self.dataGetter("Effect", 1) == const.BUFF_EFFECT_NEGATIVE

	def showLevel(self):
		return buff_data.data.get((self.id, 2)) is not None

	def isFormation(self):
		return self.dataGetter("Type", 0) == const.BUFF_TYPE_FORMATION

	def isHarmProof(self):
		return self.dataGetter("HarmProof", 0)

	def isHolyGod(self):
		return self.dataGetter("HolyGod", 0)

	@property
	def isImmortal(self):
		return self.dataGetter("immortal", 0)

	@property
	def isImmortalDel(self):
		return self.dataGetter("immortalDel", 0)

	@property
	def immortalRefreshSkill(self):
		return self.dataGetter("immortalRefreshSkill", 0)

	def hasHideFlag(self):
		return self.dataGetter("HideFlag", 0)

	def replaceHead(self):
		return self.dataGetter('ReplaceHead', '')

	def hasSeekFlag(self):
		return self.dataGetter("SeekFlag", 0)

	def isProtectedFromAvts(self):
		return self.dataGetter("avts_no_atk", 0)

	def isAvtsProtectedFrom(self):
		return self.dataGetter("no_atk_avts", 0)

	def wingOnShift(self):
		return self.dataGetter('wingOnShift', 0)

	def disableAllSkillOnModelShift(self):
		return self.dataGetter('disableAllSkillOnModelShift', 0)

	def SchoolShapeShift(self):
		# [DEBUG]
		if getattr(GlobalData, 'buff_shape_shift', 0):
			return 1
		# [DEBUG]
		return self.dataGetter("school_shapeshift", 0)

	def MonsterShapeShift(self):
		return self.dataGetter("monster_shapeshift", 0)

	def ModelShapeShift(self):
		return self.dataGetter("model_shapeshift", 0)

	def ShapeShiftLv(self):
		return self.dataGetter("shapeshift_lv", 0)

	@inline
	def iBuff_ShapeShiftName(self):
		return PNID.dataGetter("shapeshift_name", 0)

	def invisible(self):
		return self.dataGetter("Invisible", 0) > 0

	def kanbujian(self):
		return self.dataGetter("kanbujian", 0) > 0

	def skillDisabled(self):
		return self.dataGetter("Silence", 0) == 1

	def moveDisabled(self):
		return self.dataGetter("DisableMove", 0) > 0

	def dodgeDisabled(self):
		return self.dataGetter("disable_dodge", 0) > 0

	def flyDisabled(self):
		return self.dataGetter("forbidFly", 0) > 0

	def isNoTransmit(self, noType):
		if self.getType() != const.BUFF_LIMIT_TRANSMIT_TYPE:
			return False
		data = self.dataGetter('forbidChangeScene', None)
		if not data:
			return False
		if str(noType) in data:
			return True
		return False

	@inline
	def iBuff_getDisableSkillNums(self):
		return self.dataGetter("iNoSkill", 0)

	def getDisableSkillNos(self):
		return self.dataGetter("disable_skillnos", ())

	def canDisableSkill(self):
		return self.skillDisabled() or self.iBuff_getDisableSkillNums() > 0 or self.getDisableSkillNos()

	def isNoTelport(self):
		return self.isNoTransmit(const.BUFF_NO_TELEPORT_TRANSMIT)

	def isNoNPCTrans(self):
		return self.isNoTransmit(const.BUFF_NO_NPC_TRANSMIT)

	def isNoClineRet(self):
		const = 1
		return self.isNoTransmit(const.SKILL_ID)

	def hasTaunt(self):
		return self.dataGetter("Taunt", 0) > 0

	def hasAntiRemove(self):
		return self.dataGetter("AntiRemove", 0) > 0

	def isFrezzed(self):
		return self.dataGetter("Freezed", 0)

	def isShowModel(self):
		return self.dataGetter("ShowmodelOnLeave", 0)

	def speedRatio(self):
		return self.dataGetter("speed_ratio", 0) * self.powerRatio

	def criHarmRatio(self):
		return self.dataGetter("criHarmRatio", 0) * self.powerRatio

	def pHarmRatio(self):
		return self.dataGetter("pHarmRatio", 0) * self.powerRatio

	def mHarmRatio(self):
		return self.dataGetter("mHarmRatio", 0) * self.powerRatio

	def canStacked(self):
		return self.dataGetter("canStacked", False)

	def forceBaseSpeed(self):
		return self.dataGetter("forceBaseSpeed", None)

	def maxSpeed(self):
		return self.dataGetter("maxSpeed", None)

	def minSpeed(self):
		return self.dataGetter("minSpeed", 0)

	def maxRacingSpeed(self):
		return self.dataGetter("maxRacingSpeed", None)

	def minRacingSpeed(self):
		return self.dataGetter("minRacingSpeed", 0)

	def ignoreSkillMove(self):
		return self.dataGetter("ignoreSkillMove", 0)

	def getHateRate(self):
		return self.dataGetter("hateRate", 1.0) * self.powerRatio

	def getSkillpanel(self):
		return self.dataGetter("skillpanel", 0)

	def getCombatPropsOnly(self):
		return self.dataGetter('combatPropsOnly', 0)

	def getIgnoreCombatPropsOnly(self):
		return self.dataGetter('ignoreCombatPropsOnly', 0)

	def getCanMoveGid(self):
		return self.dataGetter('canMoveGid', 0)

	def getDecHPBySkill(self):
		return self.dataGetter('decHPBySkill', (0, 0))

	def getInVisible(self):
		return self.dataGetter('kanbujian', 0)

	def getDetective(self):
		return self.dataGetter('detective', 0)

	def getKeepInvisibleSkills(self):
		return self.dataGetter('keepInvisibleSkills', ())

	def needCombatprotoScale(self):
		if self.MonsterShapeShift():
			return self.dataGetter("needScale", 0)
		return 0

	def refreshEquipSkill(self):
		return self.dataGetter('refresh_equip_skill', 0)

	def manuallyCancel(self):
		return self.dataGetter('manuallyCancel', False)

	# 所受X次伤害降低Y百分比
	if COMPONENT == 'Server':

		def getCountDamageDecrease(self):
			count_damage_decrease = self.dataGetter("count_damage_decrease", ())
			if count_damage_decrease:
				count, percent = count_damage_decrease
				if not hasattr(self, 'count_damage_decrease_used'):
					self.count_damage_decrease_used = 0
				self.count_damage_decrease_used += 1
				if self.count_damage_decrease_used >= count:
					self.get_parent().remove(self.id)

				return 0 if self.count_damage_decrease_used > count else percent * self.powerRatio
			return 0
	else:
		def getCountDamageDecrease(self):
			count_damage_decrease = self.dataGetter("count_damage_decrease", ())
			if count_damage_decrease:
				count, percent = count_damage_decrease
				if not hasattr(self, 'count_damage_decrease_used'):
					self.count_damage_decrease_used = 0
				self.count_damage_decrease_used += 1

				return 0 if self.count_damage_decrease_used > count else percent * self.powerRatio
			return 0

	def getDamageIncBySkillId(self, skillid):
		damage_inc_by_skill = self.dataGetter("damage_inc_by_skill", ())
		if len(damage_inc_by_skill) != 2:
			return 0.0

		targetSkillid, incPercent = damage_inc_by_skill
		if skillid != targetSkillid:
			return 0.0
		else:
			return incPercent * self.powerRatio / 100.0

	def getGraph(self):
		if self.get_owner() and self.get_owner().IsAvatar:
			return self.dataGetter("AvatarGraph", '')
		else:
			return self.dataGetter("Graph", '')

	@property
	def remainTime(self):
		return -1 if self.cooldown < 0 else max(0, self.cooldown - time.time())

	@property
	def icon(self):
		return self.dataGetter("Icon", "")

	@property
	def description(self):
		return self.dataGetter("Desc", "")

	@property
	def name(self):
		return self.dataGetter("Name", "")

	@property
	def time(self):
		return '永久' if self.cooldown < 0 else utils.getTimeDeltaDesc(max(0, self.cooldown - time.time()))

	@property
	def fadingTime(self):
		return self.dataGetter("FadingTime", 0)

	@property
	def noInvisible(self):
		return self.dataGetter("noInvisible", 0)

	@property
	def gravity(self):
		return self.dataGetter("gravity", 0)

	@property
	def pkViolent(self):
		return self.dataGetter('pkViolent', 0)

	@property
	def immuneTypes(self):
		return self.dataGetter("immune_type", ())

	@property
	def immuneNos(self):
		return self.dataGetter("immune_no", ())

	@property
	def repelDistance(self):
		return self.dataGetter("RepelDist", 0)

	@property
	def skillCooler(self):
		return self.dataGetter('skillCooler', ())

	@property
	def skillCDReducer(self):
		if self.powerRatio == 1:
			return self.dataGetter('reduceOtherCd', ())
		else:
			return tuple(
				(a, b, d * self.powerRatio)
				for a, b, d in self.dataGetter('reduceOtherCd', ())
			)

	@property
	def causeDamage(self):
		return self.dataGetter('causeDamage', 0) * self.powerRatio

	@property
	def causeDeath(self):
		return self.dataGetter('causeDeath', 0)

	@property
	def snowdriftOccupySpeedupOwn(self):
		return self.dataGetter('snowdriftOccupySpeedupOwn', 0)

	@property
	def snowdriftOccupySpeedupCamp(self):
		return self.dataGetter('snowdriftOccupySpeedupCamp', 0)

	@property
	def campSnowballAdd(self):
		return self.dataGetter('campSnowballAdd', 0)

	@property
	def ownSnowballAdd(self):
		return self.dataGetter('ownSnowballAdd', 0)

	@property
	def snowballCollectSpeedup(self):
		return self.dataGetter('snowballCollectSpeedup', 0)

	@property
	def decSnowballCost(self):
		return self.dataGetter('decSnowballCost', 0)

	@property
	def campSnowballRecoverSpeedup(self):
		return self.dataGetter('campSnowballRecoverSpeedup', 0)

	def createMagicFieldOnTimeOut(self):
		create_no = self.dataGetter("post_create_magicfield", 0)
		if create_no == 0:
			return
		if SMD.data.get(create_no, {}).get('center', 1) != const.MAGIC_CTYPE_TARGET:
			return
		if not self.casterid:
			return
		owner = self.get_owner()
		if owner is None or not owner.space:
			return

		caster = owner.space.getEntityByID(self.casterid)
		if caster is None:
			return

		content = {
			'no': create_no,
			'lv': self.level,
			'ownerid': caster.id,
			'position': owner.position,
			'direction': owner.yaw,
			'targetid': owner.id,
			'space': owner.space,
		}
		caster.space.create_entity("MagicField", None, content)

	def createMagicFieldOnInit(self):
		create_no = self.dataGetter("init_create_magicfield", 0)
		if create_no == 0:
			return
		if SMD.data.get(create_no, {}).get('center', 1) != const.MAGIC_CTYPE_SELF:
			return
		owner = self.get_owner()
		if owner is None:
			return

		content = {
			'no': create_no,
			'lv': self.level,
			'ownerid': owner.id,
			'position': owner.position,
			'direction': owner.yaw,
			'targetid': owner.id,
			'space': owner.space,
		}
		owner.add_timer(0, functools.partial(self.createMagicField, content))

	def createMagicField(self, content):
		owner = self.get_owner()
		owner and owner.space and owner.space.create_entity(
			"MagicField", None, content
		)

	def hasBianshenFlag(self):
		return self.dataGetter("bianshenFlag", 0)
	
	def hasYirongFlag(self):
		return self.dataGetter("yirongFlag", 0)

	@property
	def bianshenCarrierNo(self):
		return self.dataGetter("bianshenCarrierNo", 0)

	@property
	def tasteMonsterFlag(self):
		return self.dataGetter("tasteMonsterFlag", 0)

	@property
	def tasteDragonFlag(self):
		return self.dataGetter("tasteDragonFlag", 0)

	@property
	def tasteCarrierNo(self):
		return self.dataGetter("tasteCarrierNo", 0)

	@property
	def divineFlag(self):
		return self.dataGetter("divineFlag", 0)

	@property
	def divineDeadArg(self):
		return self.dataGetter("divineDeadArg", 0)

	@property
	def divineWaterArg(self):
		return self.dataGetter("divineWaterArg", 0)

	@property
	def divineEnhanceArg(self):
		return self.dataGetter("divineEnhanceArg", 0)

	@property
	def divineRedHandArg(self):
		return self.dataGetter("divineEnhanceArg", 0)

	@property
	def divineDiscountArg(self):
		return self.dataGetter("divineDiscountArg", ())

	@property
	def divineBuildArg(self):
		return self.dataGetter("divineBuildArg", 0)

	@property
	def divineExpArg(self):
		return self.dataGetter("divineExpArg", 0)

	@property
	def divineCancelAfterEffect(self):
		return self.dataGetter("divineCancelAfterEffect", False)

	@property
	def divineEffectDurationLimit(self):
		return self.dataGetter("divineEffectDurationLimit", None)

	@property
	def divineInEffectDuration(self):
		if not self.divineEffectDurationLimit:  # 没有这个字段则不受限制
			return True
		(fromHour, fromMinute),(toHour, toMinute) = self.divineEffectDurationLimit
		now = datetime.datetime.now()
		fromTime = datetime.datetime(now.year, now.month, now.day, fromHour, fromMinute, 0)
		toTime = datetime.datetime(now.year, now.month, now.day, toHour, toMinute, 0)
		return fromTime < now < toTime

class iBuffs(CustomMapType):
	def __init__(self, data={}):
		self.cache = dict()
		self.attr_inspect_cache = dict()
		super(iBuffs, self).__init__(data)

		self.stamps = {}
		self.stamp_counter = 0

	# [DEBUG]
	def debugInfo(self, message):
		if self.get_owner() and BUFF_DEBUG:
			self.get_owner().logger.info('[BUFF DEBUG]: %s', message)
	# [DEBUG]

	def initBuffs(self):
		now = time.time()
		for buff in self.values():
			if buff.cooldown > now:
				buff.onEnter()
				self._initWithDuration(buff.id, buff.cooldown - now)
			elif buff.cooldown > 0 and buff.cooldown < now + 1e-6:
				self.forceRemove(buff.id)
			else:
				buff.onEnter()

	@attr_cache
	def hasFlag(self, name):
		for buff in self.itervalues():
			if buff.data.get(name, 0) > 0:
				return True
		return False

	@attr_cache
	def ShapeShiftLv(self):
		for buff in self.itervalues():
			if buff.ShapeShiftLv():
				return True
		return False

	def _canReplaceSingle(self, id, level, buff):
		buffType = buff_data.data.get((id, level), {}).get('Type', 0)
		if buffType in SINGLE_TYPES and buff.getType() == buffType:
			stype = buff.getSubType()
			if stype == const.BUFF_STYPE_REPLACEABLE:  # subtype 1
				return True
			elif stype == const.BUFF_STYPE_IRREPLACEABLE:  # subtype 2
				return False
			elif buffType == const.BUFF_TYPE_HIT and buff.cooldown > 0 and buff.fadingTime > 0:  # subtype 3
				if time.time() > buff.cooldown - buff.fadingTime:
					return True
		return False

	@staticmethod
	def getActualLevel(targetLevel, buffNo, buffLevel):
		levelRangeList = BTLD.data.get(buffNo, ())
		if levelRangeList:
			for i, (minLevel, maxLevel, actLevel) in enumerate(levelRangeList):
				if targetLevel < minLevel:
					return actLevel if i == 0 else levelRangeList[i - 1][2]
				elif targetLevel <= maxLevel or i == len(levelRangeList) - 1:
					return actLevel
		return buffLevel

	def canAdd(self, id, level, duration, casterid):  # noqa
		buffData = buff_data.data.get((id, level))
		if not buffData:
			# [DEBUG]
			self.debugInfo('状态ID不存在: %d' % id)
			# [DEBUG]
			return False
		dataGetter = buffData.get
		deadExists = dataGetter('existsAfterDead', 0)
		# 死亡不清除的buff在添加的时候，目标死亡也要添加
		if duration == 0 or (not self.get_owner().isAlive() and not deadExists):
			# [DEBUG]
			self.debugInfo('状态时间为0' if duration == 0 else '目标死亡')
			# [DEBUG]
			return False
		owner = self.get_owner()

		buffType = dataGetter('Type', 0)

		# Solo时不接收除自己和自己的召唤兽以外的人加的良性buff
		if owner.IsAvatar and owner.soloState == const.SOLO_STATE_SOLO and casterid != owner.id and \
			(not owner.getCombatPokemon() or casterid != owner.getCombatPokemon().id) and \
			buffType in (const.BUFF_TYPE_BENIGN, const.BUFF_TYPE_TRANSFORM_HARM, const.BUFF_TYPE_SCH_RESISTANCE, const.BUFF_TYPE_SCH_REINFORCE):
			return False

		# Solo时召唤兽也不接受除自己和主人意外的人家的良性buff
		if owner.IsPokemon and owner.owner and owner.owner.soloState == const.SOLO_STATE_SOLO and casterid != owner.id and \
			casterid != owner.owner.id and \
			buffType in (const.BUFF_TYPE_BENIGN, const.BUFF_TYPE_TRANSFORM_HARM, const.BUFF_TYPE_SCH_RESISTANCE, const.BUFF_TYPE_SCH_REINFORCE):
			return False

		if buffType not in (const.BUFF_TYPE_BENIGN, ) and self.get_owner().isDamageProof():
			# [DEBUG]
			self.debugInfo('目标无敌，无法加状态: %d' % id)
			# [DEBUG]
			return False

		onlySpaces = dataGetter('buffOnlySpaces', None)
		if onlySpaces:
			space = getattr(owner, 'space', None)
			if not space or space.spaceno not in onlySpaces:
				return False

		if buffType == const.BUFF_TYPE_FORMATION:
			# 阵型的添加、替换规则交给上层
			return True
		for buff in self.itervalues():
			btype = buff.getType()

			# 4,5,6,7,8类型最多一个（除了可替换的）
			if buffType == btype and btype in SINGLE_TYPES and not self._canReplaceSingle(id, level, buff):
				# [DEBUG]
				self.debugInfo('此状态类型最多只能存在一个并且不能替换: %d' % id)
				# [DEBUG]
				return False

			# 免疫类型
			if buffType in buff.immuneTypes:
				# [DEBUG]
				self.debugInfo('此状态被免疫: %d' % id)
				# [DEBUG]
				return False
			# 免疫编号
			if id in buff.immuneNos:
				# [DEBUG]
				self.debugInfo('此状态被免疫: %d' % id)
				# [DEBUG]
				return False

		buff = self.get(id, None)

		# 无此编号的buff，可以添加
		if buff is None:
			return True

		# [同编号] 5类型不能被同编号的顶替
		# if buffType == const.BUFF_TYPE_SPECIAL:
		# 	return False

		cooldown = -1 if duration < 0 else time.time() + duration
		# [同编号] 低等级忽略；同等级cooldown比原来小忽略
		if level < buff.level or (level == buff.level and cooldown > 0 and cooldown < buff.cooldown):
			# [DEBUG]
			self.debugInfo('此状态已存在且等级较低或者时间较短: %d' % id)
			# [DEBUG]
			return False

		return True

	def resetDuration(self, id, duration):
		if id not in self:
			return

		self.stamps[id] = 0

		self._initWithDuration(id, duration)

	def _initWithDuration(self, id, duration):
		if duration > 0:
			self.stamp_counter += 1
			self.stamps[id] = self.stamp_counter
			self.get_owner().add_timer(duration, functools.partial(self.clearCallback, id, self.stamp_counter))
		if id in self:
			cooldown = -1 if duration < 0 else time.time() + duration
			self[id].cooldown = cooldown

	def _removeOnAdd(self, id, level):
		# 1. 删除同编号的, 在cBuffs.add中已处理
		# self.remove(id)

		# 2. 互斥状态类型、编号
		dataGetter = buff_data.data.get((id, level), {}).get
		remove_buff_type = dataGetter('remove_buff_type', ())
		remove_buff_no = dataGetter('remove_buff_no', ())
		for buff in self.values():
			if buff.getType() in remove_buff_type:
				self.forceRemove(buff.id)
			elif buff.id in remove_buff_no:
				self.forceRemove(buff.id)

		# 3. 处理同类型只能有一个的buff
		buffType = dataGetter('Type', 0)
		if buffType in SINGLE_TYPES:
			for buff in self.values():
				if self._canReplaceSingle(id, level, buff):
					self.forceRemove(buff.id)

	def add(self, id, level, duration, casterid, **kwargs):
		if self.canAdd(id, level, duration, casterid):
			self._removeOnAdd(id, level)
			self._initWithDuration(id, duration)
			return True
		return False

	def clearCallback(self, id, stamp):
		if id in self.stamps and self.stamps[id] == stamp:
			buff = self.get(id, None)
			if buff:
				buff.createMagicFieldOnTimeOut()
			self.clearBuff(id)
			self.stamps[id] = 0

	def clearBuff(self, id):
		if id in self:
			self.stamps[id] = 0
			self.get_owner().onRemoveBuff(id)
			return True

		return False

	def delBuff(self, id):
		if self.canRemove(id):
			self.remove(id)

	def manuallyCancel(self, id):
		id in self and self[id].manuallyCancel() and self.remove(id)

	def forceRemove(self, id):
		self.remove(id)

	def remove(self, id):
		# 不检测canRemove
		return self.clearBuff(id)

	def forceRemoveBuffsFrom(self, casterid, btype):
		bids = list(self.iterkeys())
		for bid in bids:
			if bid not in self:
				continue
			buff = self[bid]
			if buff.casterid == casterid and buff.getType() == btype:
				self.forceRemove(bid)

	def canRemove(self, id):
		buff = self.get(id, None)
		if buff is None:
			return False

		btype = buff.getType()
		# 受击(4), 特殊状态(5)无法被动清除
		if btype == const.BUFF_TYPE_SPECIAL or btype == const.BUFF_TYPE_HIT:
			return False

		# 无法被清除标志
		if buff.hasAntiRemove():
			return False

		return True

	def removeByEffectType(self, typ, num):
		if num <= 0:
			return
		keys = self.keys()
		random.shuffle(keys)
		for no in keys:
			if no not in self:
				continue
			buff = self[no]
			if typ == buff.getEffectType() and self.canRemove(no):
				num -= 1
				self.forceRemove(no)
			if num <= 0:
				break

	def removeByWuxing(self, wuxing, positive, num, prob):
		buffs = [buff.id for buff in self.itervalues() if buff.getWuXingType() == wuxing and buff.isPositive() == positive]
		if len(buffs) > num:
			buffs = random.sample(buffs, num)
		for buffid in buffs:
			if random.random() < prob:
				self.forceRemove(buffid)

	@attr_cache
	def allSkillDisabled(self):
		for buff in self.itervalues():
			if buff.skillDisabled():
				return True
		return False

	@attr_cache
	def ignoreSkillMove(self):
		for buff in self.itervalues():
			if buff.ignoreSkillMove():
				return True
		return False

	@attr_cache
	def ModelShapeShift(self):
		for buff in self.itervalues():
			if buff.ModelShapeShift():
				return True
		return False

	@attr_cache
	def ModelShapeShiftScale(self):
		for buff in self.itervalues():
			scale = buff.data.get('model_shapeshift_scale', 0)
			if scale > 0:
				return scale
		return 1

	@attr_cache
	def disableAllSkillOnModelShift(self):
		for buff in self.itervalues():
			if buff.disableAllSkillOnModelShift():
				return True
		return False

	@attr_cache
	def isHarmProof(self):
		for buff in self.itervalues():
			if buff.isHarmProof() or buff.isHolyGod():
				return True
		return False

	def getDisableSkillNums(self):
		for buff in self.itervalues():
			num = buff.iBuff_getDisableSkillNums()
			if num > 0:
				return num
		return 0

	@attr_cache
	def isHolyGod(self):
		for buff in self.itervalues():
			if buff.isHolyGod():
				return True
		return False

	@attr_cache
	def isProtectedFromAvts(self):
		for buff in self.itervalues():
			if buff.isProtectedFromAvts():
				return True
		return False

	@attr_cache
	def isAvtsProtectedFrom(self):
		for buff in self.itervalues():
			if buff.isAvtsProtectedFrom():
				return True
		return False

	@attr_cache
	def speedRatio(self):
		return self.sumAttr('speed_ratio')

	@attr_cache
	def forceBaseSpeed(self):
		for buff in self.itervalues():
			if buff.forceBaseSpeed():
				return buff.forceBaseSpeed()
		return None

	@attr_cache
	def maxSpeed(self):
		for buff in self.itervalues():
			if buff.maxSpeed():
				return buff.maxSpeed()
		return None

	@attr_cache
	def minSpeed(self):
		for buff in self.itervalues():
			if buff.minSpeed() > 0:
				return buff.minSpeed()
		return 0

	@attr_cache
	def maxRacingSpeed(self):
		for buff in self.itervalues():
			if buff.maxRacingSpeed():
				return buff.maxRacingSpeed()
		return None

	@attr_cache
	def minRacingSpeed(self):
		for buff in self.itervalues():
			if buff.minRacingSpeed() > 0:
				return buff.minRacingSpeed()
		return 0

	@attr_cache
	def pHarmRatio(self):
		ro = 0
		harmProtectRatios = self.getHarmRatioProtect()
		for buff in self.itervalues():
			ro += buff.pHarmRatio() * harmProtectRatios.get(buff.id, 1.0)
		if ro > 1:
			ro == 1
		if ro < -1:
			ro == -1
		return ro

	@attr_cache
	def noInvisible(self):
		# 不能隐身
		for buff in self.itervalues():
			if buff.noInvisible:
				return True
		return False

	@attr_cache
	def mHarmRatio(self):
		ro = 0
		harmProtectRatios = self.getHarmRatioProtect()
		for buff in self.itervalues():
			ro += buff.mHarmRatio() * harmProtectRatios.get(buff.id, 1.0)
		if ro > 1:
			ro == 1
		if ro < -1:
			ro == -1
		return ro

	@attr_cache
	def sumAttr(self, attrName):
		return sum(x.data.get(attrName, 0) * x.powerRatio for x in self.itervalues())

	@attr_cache
	def maxAttr(self, attrName, default=0):
		try:
			return max(x.data.get(attrName, 0) for x in self.itervalues())
		except ValueError:  # for an empty sequence
			return default

	@attr_cache
	def moveDisabled(self):
		for buff in self.itervalues():
			if buff.moveDisabled():
				return True
		return False

	@attr_cache
	def flyDisabled(self):
		for buff in self.itervalues():
			if buff.flyDisabled():
				return True
		return False

	@attr_cache
	def getHateRate(self):
		rate = 1.0
		for buff in self.itervalues():
			rate *= buff.getHateRate()
		return rate

	@attr_cache
	def getSkillpanel(self):
		for buff in self.itervalues():
			if buff.getSkillpanel():
				return True
		return False

	@attr_cache
	def getCombatPropsOnly(self):
		for buff in self.itervalues():
			if buff.getCombatPropsOnly():
				return True
		return False

	@attr_cache
	def getCanMoveGid(self):
		for buff in self.itervalues():
			if buff.getCanMoveGid():
				return True
		return False

	@attr_cache
	def getDecHPBySkill(self):
		for buff in self.itervalues():
			x, y = buff.getDecHPBySkill()
			if x and y:
				return x, y
		return (0, 0)

	@attr_cache
	def needCombatprotoScale(self):
		for buff in self.itervalues():
			if buff.needCombatprotoScale():
				return True
		return False

	def getTauntTarget(self):
		for buff in self.itervalues():
			if buff.hasTaunt() and buff.casterid:
				target = EntityManager.getentity(buff.casterid)
				if target and target.isAlive():
					return target
		return None

	@attr_cache
	def isNoTelport(self):
		for buff in self.itervalues():
			if buff.isNoTelport():
				return True
		return False

	@attr_cache
	def hasHideFlag(self):
		for buff in self.itervalues():
			if buff.hasHideFlag():
				return True
		return False

	@attr_cache
	def replaceHead(self):
		for buff in self.itervalues():
			if buff.replaceHead():
				return buff.replaceHead()
		return ''

	@attr_cache
	def hasSeekFlag(self):
		for buff in self.itervalues():
			if buff.hasSeekFlag():
				return True
		return False

	@attr_cache
	def isNoNPCTrans(self):
		for buff in self.itervalues():
			if buff.isNoNPCTrans():
				return True
		return False

	@attr_cache
	def isNoClineRet(self):
		for buff in self.itervalues():
			if buff.isNoClineRet():
				return True
		return False

	@attr_cache
	def getBuffForbidSkills(self):
		for buff in self.itervalues():
			if len(buff.buffForbidSkills) > 0:
				return list(buff.buffForbidSkills)
		return []

	@attr_cache
	def getSkillEnforceRate(self, skillid):
		increase_damage_rate = 0
		for buff in self.itervalues():
			skillEnforces = buff.data.get('skill_enforce', ())
			for enforce in skillEnforces:
				if enforce[0] == skillid:
					increase_damage_rate += enforce[1]
		return increase_damage_rate

	@attr_cache
	def getSchoolAttackReinforce(self, school):
		a1, b1 = 0, 0
		for buff in self.itervalues():
			reinforce = buff.data.get('school_attack_reinforce', {})
			if reinforce and school in reinforce:
				a1, b1 = reinforce[school]

		return a1, b1

	@attr_cache
	def getSchoolDamageResistance(self, school):
		a2, b2 = 0, 0
		for buff in self.itervalues():
			resistance = buff.data.get('school_damage_resistance', {})
			if resistance and school in resistance:
				a2, b2 = resistance[school]

		return a2, b2

	@attr_cache
	def isNoTransmit(self, noType):
		for buff in self.itervalues():
			if buff.isNoTransmit(noType):
				return True
		return False

	@attr_cache
	def hasSpecialSubType(self, subType):
		for buff in self.itervalues():
			if buff.getType() == const.BUFF_TYPE_SPECIAL and buff.getSubType() == subType:
				return True
		return False

	def getHarmRatioProtect(self):
		ratios = {}
		for buff in self.itervalues():
			harmRatioProtect = buff.data.get("harmRatioProtect", ())
			for bid, add in harmRatioProtect:
				if bid not in ratios:
					ratios[bid] = add
				else:
					ratios[bid] *= add

		return ratios

	def _pokemonPropPerLevel(self, props, addProps, pokemon_lv_prop, casterid):
		if not casterid or not pokemon_lv_prop or len(pokemon_lv_prop) != 2:
			return
		if self.get_owner() is None or self.get_owner().space is None:
			return
		pokemon = self.get_owner().space.getEntityByID(casterid)
		if pokemon is None:
			return
		if not pokemon.IsPokemon:
			return
		pname = PNID.data.get(pokemon_lv_prop[0], {}).get('key', '')
		if not pname:
			return
		pvalue = pokemon_lv_prop[1] * pokemon.lv
		if pname in props:
			addProps.setdefault(pname, list()).append((0, pvalue))

	def calcConvertProps(self):
		res = set()

		combatPropsOnly = self.getCombatPropsOnly()

		for buff in self.itervalues():
			if combatPropsOnly and not buff.getIgnoreCombatPropsOnly():
				continue
			data = buff.data
			attrconverts = data.get('attrconverts', ())
			# self.get_owner().logger.info('calcMiscProps: attrconvert %s', attrconvert)
			for attrconvert in attrconverts:
				res.add(attrconvert)
		return res

	def calcAddProps(self, props, addProps=None, ingnorePmPskill=False):
		addProps = addProps or defaultdict(list)

		combatPropsOnly = self.getCombatPropsOnly()

		for buff in self.itervalues():
			if combatPropsOnly and not buff.getIgnoreCombatPropsOnly():
				continue
			powerRatio = buff.powerRatio
			data = buff.data
			for name, ratio, value in data.get('add_props', tuple()):
				effectPercent = data.get('pokemonEffectPercent', 1) if self.get_owner().IsPokemon else 1
				effectPercent *= powerRatio
				name in props and addProps[name].append((ratio * effectPercent, value * effectPercent))

			for name, ratio, value, base, extra in data.get('extra_props', tuple()):
				if name not in props:
					continue

				value += props.get(base, 0) * extra * powerRatio
				addProps[name].append((ratio * powerRatio, value))

			if not ingnorePmPskill:
				pokemon_lv_prop = data.get('pokemon_lv_prop', ())
				pokemon_lv_prop and self._pokemonPropPerLevel(props, addProps, pokemon_lv_prop, buff.casterid)

		return addProps

	def calcPokemonPskillProps(self):
		"""召唤兽被动技能增加属性单独作为基础属性"""
		props = {}
		for buff in self.itervalues():
			pokemon_lv_prop = buff.data.get('pokemon_lv_prop', ())
			if not pokemon_lv_prop:
				continue

			addProp = self.getPokemonPropPerLevel(pokemon_lv_prop, buff.casterid)
			if not addProp:
				continue

			pname, pvalue = addProp
			props[pname] = props.get(pname, 0) + pvalue

		return props

	def getPokemonPropPerLevel(self, pokemon_lv_prop, casterid):
		if not casterid or not pokemon_lv_prop or len(pokemon_lv_prop) != 2:
			return
		if self.get_owner() is None or self.get_owner().space is None:
			return
		pokemon = self.get_owner().space.getEntityByID(casterid)
		if pokemon is None:
			return
		if not pokemon.IsPokemon:
			return
		pname = PNID.data.get(pokemon_lv_prop[0], {}).get('key', '')
		if not pname:
			return
		pvalue = pokemon_lv_prop[1] * pokemon.lv
		return pname, pvalue

	def calcMiscProps(self, props):
		combatPropsOnly = self.getCombatPropsOnly()
		for buff in self.itervalues():
			if combatPropsOnly and not buff.getIgnoreCombatPropsOnly():
				continue
			if buff.wingOnShift():
				props['wingOnShift'] = 1

		return props

	def clear(self):
		self.cache.clear()
		self.attr_inspect_cache.clear()
		for id in self.keys():
			self.forceRemove(id)

	def getRemainTime(self, id):
		if id in self:
			buff = self[id]
			return -1 if buff.cooldown < 0 else max(0, buff.cooldown - time.time())
		return 0

	def isFaint(self):
		# HARDCODE
		return 31 in self

	def triggerEvent(self, id, level):
		event = buff_data.data.get((id, level), {}).get("SpaceEvent", 0)
		if event > 0 and self.get_owner():
			self.get_owner().space.triggerEvent(self.get_owner(), event)

	def hasHolyShield(self):
		return const.BUFF_ID_HOLY_SHIELD in self

	def hasID(self, id):
		return id in self

	def updateSpacecamp(self):
		if not self.get_owner():
			return
		for buff in self.itervalues():
			spacecamp = buff.data.get('SpacecampChange', -1)
			if spacecamp >= 0:
				self.get_owner().changeSpacecamp(spacecamp)
				return

	@attr_cache
	def getHarmTransformArgs(self):
		for buff in self.itervalues():
			th = buff.data.get('transform_harm', 0)
			if th > 0:
				return th, buff.data.get('transform_harm_limit', 0)
		return (0, 0)

	def isImmortal(self):
		return self.hasFlag('immortal')

	if COMPONENT == 'Server':
		@attr_inspect_cache('count_damage_decrease')
		def getCountDamageDecrease(self, triggers):
			# 不能用itervalues，可能会被删除
			buffs = [self[buffid] for buffid in triggers if buffid in self]
			return sum(map(self.VALUE_TYPE.getCountDamageDecrease, buffs)) if buffs else 0
	else:
		@attr_cache
		def getCountDamageDecrease(self):
			return sum(map(self.VALUE_TYPE.getCountDamageDecrease, self.itervalues()))

	def getDamageIncBySkillId(self, skillId):
		return sum(x.getDamageIncBySkillId(skillId) for x in self.itervalues())

	def hasAntiLock(self):
		return self.hasFlag('anti_lock_target')

	def onDelCondition(self, cond, exclude=0):
		pass

	@attr_cache
	def getSkillRangeAdd(self, skillid):
		res = 0
		for buff in self.itervalues():
			skill_range_add = buff.data.get('skill_range_add', ())
			if skill_range_add and skillid in skill_range_add[1]:
				res += skill_range_add[0][0]
		return res

	@attr_cache
	def getAffectRangeAdd(self, skillid):
		res = 0
		for buff in self.itervalues():
			affect_range_add = buff.data.get('affect_range_add', ())
			if affect_range_add and skillid in affect_range_add[1]:
				res += affect_range_add[0][0]
		return res

	def isDisorder(self):
		return self.hasFlag('disorder')

	def comradeReflectDmg(self):
		return self.hasFlag('comrade_reflect_dmg')

	def __setitem__(self, name, value):
		self.cache.clear()
		self.attr_inspect_cache.clear()
		super(iBuffs, self).__setitem__(name, value)

	def __delitem__(self, name):
		self.cache.clear()
		self.attr_inspect_cache.clear()
		super(iBuffs, self).__delitem__(name)
		
	@attr_cache
	def hasBianshenFlag(self):
		for buff in self.itervalues():
			if buff.hasBianshenFlag():
				return True
		return False

	@attr_cache
	def hasYirongFlag(self):
		for buff in self.itervalues():
			if buff.hasYirongFlag():
				return True
		return False

	@attr_cache
	def bianshenCarrierNo(self):
		for buff in self.itervalues():
			no = buff.bianshenCarrierNo
			if no:
				return no
		return 0

	@attr_cache
	def tasteMonsterFlag(self):
		for buff in self.itervalues():
			if buff.tasteMonsterFlag:
				return buff.tasteMonsterFlag
		return 0

	@attr_cache
	def tasteDragonFlag(self):
		for buff in self.itervalues():
			if buff.tasteDragonFlag:
				return buff.tasteDragonFlag
		return 0

	@attr_cache
	def tasteCarrierNo(self):
		for buff in self.itervalues():
			if buff.tasteCarrierNo:
				return buff.tasteCarrierNo
		return 0

	@attr_cache
	def divineDeadArg(self):
		for buff in self.itervalues():
			if buff.divineDeadArg:
				return buff.divineDeadArg
		return 0

	@attr_cache
	def divineWaterArg(self):
		for buff in self.itervalues():
			if buff.divineWaterArg:
				return buff.divineWaterArg
		return 0

	@attr_cache
	def divineEnhanceArg(self):
		for buff in self.itervalues():
			if buff.divineEnhanceArg:
				return buff.divineEnhanceArg
		return 0

	@attr_cache
	def divineRedHandArg(self):
		for buff in self.itervalues():
			if buff.divineRedHandArg:
				return buff.divineRedHandArg
		return 0

	@attr_cache
	def divineDiscountArg(self):
		for buff in self.itervalues():
			if buff.divineDiscountArg:
				return buff.divineDiscountArg
		return -1, 1

	@attr_cache
	def divineBuildArg(self):
		for buff in self.itervalues():
			if buff.divineBuildArg:
				return buff.divineBuildArg
		return 0

	@attr_cache
	def divineExpArg(self):
		for buff in self.itervalues():
			if buff.divineExpArg:
				return buff.divineExpArg
		return 0