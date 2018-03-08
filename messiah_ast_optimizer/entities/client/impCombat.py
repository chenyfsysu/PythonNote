# -*- coding:utf-8 -*-

import txm
import MEngine
import MRender
import MObject
import MPlatform
import MConfig
import MType
import MHelper
import math
import random
import time
import functools
import EngineVersionCheck
from common.IdManager import IdManager
from common.EntityManager import EntityManager
from common.RpcMethodArgs import Dict, Int, Tuple, Float, Str, Bool, EntityID, List
from common.classutils import Property
from common.rpcdecorator import rpc_method, CLIENT_STUB
from mobilelog.LogManager import LogManager
from GUI.AwakePanel import AwakeSkillResult
from iAwake import AwakeConst
from GUI.playermain.PlayerMain import PlayerMain
from GUI.playermain.GSkillButton import ChooseMode
from GUI.RelivePopup import ReliveBase
from GUI.SkillPanel import SkillPanel
from GUI.SchoolTransfer import SchoolTransfer
from GUI.gameitems.ResourceTips import ResourceTips
from GUI.cjbattle.CJRightCorner import CJRightCorner
from Space import Space
from GameItem import GameItem
from cCombatUnit import cCombatUnit
from iCombatUnit import iCombatUnit, SkillCooler
from commontypes.PanelSkills import PanelSkills
from commontypes.SyncableRandomer import SyncableRandomer
import GlobalData
import cconst
import const
import config
import formula
import utils
import DataHelper
from MagicField import MagicField
from SimpleAI import PlayerTaskSimpleAI
from iCombatUnit import getSchoolLevelSkills
from iCombatUnit import getSchoolLevelPSkills
from iDress import DressColor
from data import combatunit_data as CD
from data import combatproto_data as CPD
from data import school_data
from data import skill_data
from data import space_data
from data import state_instruction_constrain_data as SICD
from data import auto_skills_ref_data as ASRD
from data import school_skill_data as SSD
from data import school_special_data as SSPD
from data import school_init_skill_data as SISD
from data import hardcode_resource_data as HRD
from data import school_skill_relation_data as SSRD
from data import school_skill_learn_data as SSLD
from data import school_special_skill_item_data as SSSID
from data import space_taskai_data as STAD
from data import survival_combatmodel_random_data as SCRD
from GUI.SkillChargeBar import SkillChargeBar
from GUI.AutoSkillPanel import AutoSkillBar
from GUI.TxmMessageBox import MessageBox
from GUI.NoticeMessage import NavigationMessage
from GUI.gameitems.ExtraAssignCredit import ExtraAssignCredit
from impHideAndSeek import HsConst
from iRelation import decide
from iCombatUnit import CombatHelper
from GUI.ScreenPopmsg import PopmsgPool
from ModelSeqLoader import ModelSeqLoader
from iSurvivalBattle import SurvivalBattleConst

class SkillManager(object, ):

    class Slot(object, ):

        def __init__(self, skillid, slotid, ownerid):
            self.skillid = skillid
            self.time = 0
            self.slotid = slotid
            self.ownerid = ownerid
            self.skillid_cache = (-1)

        def ResetSkillidCacheS(self):
            self.skillid_cache = (-1)

        def used(self):
            pass

        def canUse(self, skillid):
            return True

        def chargeStart(self):
            self.time = time.time()

        def chargeEnd(self):
            delta = max(0, (time.time() - self.time))
            self.time = 0
            return delta

        def updateSkillState(self, skillid, state):
            p = GlobalData.p
            skill = p.GetSkill(skillid)
            if skill:
                PlayerMain().updateSlotSkillState(self.slotid, skillid, state)

        def checkAutoSwitch(self):
            return 0

    class ComboSlot(Slot, ):

        def __init__(self, skillid, level, slotid, ownerid):
            self.skillids = [skillid]
            self.skillids.extend(SSRD.data.get(skillid, ()))
            self.combo = 0
            self.slotid = slotid
            self.ownerid = ownerid
            self.time = 0
            self.skillid_cache = (-1)

        @property
        def cur_skillid(self):
            owner = EntityManager.getentity(self.ownerid)
            if (owner is None):
                return 0
            (skillid, state) = owner.skillstate.skillRunning
            if (skillid in self.skillids):
                return skillid
            old = ASRD.data.get('n2o', {}).get(skillid, 0)
            if (old in self.skillids):
                return skillid
            return 0

        def getDefaultSkill(self):
            skillid = self.skillids[0]
            buffReplaceSkill = self.checkBuffReplaceSkill()
            if buffReplaceSkill:
                skillid = buffReplaceSkill
            return skillid

        @property
        def skillid(self):
            if (self.skillid_cache != (-1)):
                return self.skillid_cache
            player = EntityManager.getentity(self.ownerid)
            if (not player):
                return 0
            default_skill = self.getDefaultSkill()
            skillid = default_skill
            if self.cur_skillid:
                skillid = self.cur_skillid
                skill = player.GetSkill(self.cur_skillid)
                succ = skill.comboSucc
                if succ:
                    if (succ == self.cur_skillid):
                        skillid = default_skill
                    else:
                        skillid = succ
                else:
                    skillid = default_skill
            elif (self.slotid == (5 + 4)):
                x = player.isDodgeOrQinggong()[0]
                skillid = (x if x else skillid)
            else:
                auto_skillid = self.checkAutoSwitch()
                if auto_skillid:
                    skillid = auto_skillid
                else:
                    skillid = default_skill
            self.skillid_cache = int(skillid)
            return self.skillid_cache

        def checkAutoSwitch(self):
            owner = EntityManager.getentity(self.ownerid)
            if ((owner is None) or (not owner.skillmgr.comboAllowed)):
                return 0
            skillid = self.skillids[0]
            (sskillid, sstate) = owner.skillstate.skillRunning
            sskill = owner.GetSkill(sskillid)
            if sskill:
                ass = sskill.GetAutoSwitchSkills()
                for (skilla, skillb) in ass:
                    if (skillid == skilla):
                        return skillb
            return 0

        def checkBuffReplaceSkill(self):
            owner = EntityManager.getentity(self.ownerid)
            if (owner is None):
                return 0
            skillid = self.skillids[0]
            replace_skill = owner.buffs.getReplacedSkill(skillid)
            if replace_skill:
                return replace_skill
            return 0

        def used(self):
            self.combo += 1
            self.combo %= len(self.skillids)

        def reset(self):
            self.combo = 0

        def canUse(self, skillid):
            if (self.cur_skillid == 0):
                return True
            owner = EntityManager.getentity(self.ownerid)
            if (owner is None):
                return False
            cskill = owner.GetSkill(self.cur_skillid)
            if (cskill is None):
                return False
            if (cskill.comboSucc == skillid):
                return owner.skillmgr.comboAllowed
            return True

        def onSkillUsedS(self, skillid):
            pass

        def onSkillStartS(self, skillid):
            PlayerMain().onSkillStart(self.slotid)

        def onSkillEndS(self, skillid):
            pass

    def __init__(self, ownerid):
        super(SkillManager, self).__init__()
        self.ownerid = ownerid
        self.updateSkills()
        self.skillRunning = (0, 5)
        self.skillHolding = 0
        self.logger = LogManager.get_logger(('SkillManager.' + self.__class__.__name__))

    def ResetSkillidCacheM(self):
        for s in self.slots:
            s.ResetSkillidCacheS()

    @property
    def comboAllowed(self):
        return getattr(self, '_combo', False)

    @comboAllowed.setter
    def comboAllowed(self, value):
        self._combo = value
        self.ResetSkillidCacheM()

    @property
    def skillRunning(self):
        owner = EntityManager.getentity(self.ownerid)
        return owner.skillstate.skillRunning

    @skillRunning.setter
    def skillRunning(self, value):
        self.ResetSkillidCacheM()
        owner = EntityManager.getentity(self.ownerid)
        owner.skillstate.skillRunning = value

    @property
    def skillNext(self):
        owner = EntityManager.getentity(self.ownerid)
        return owner.skillstate.skillNext

    @skillNext.setter
    def skillNext(self, value):
        owner = EntityManager.getentity(self.ownerid)
        owner.skillstate.skillNext = value

    def _get_ordinary_skills_school_shapeshift(self):
        skills = []
        owner = EntityManager.getentity(self.ownerid)
        data = SISD.data.get(owner.school_shapeshift, {})
        general = SSD.data.get(data.get('general', 0), {}).get('Skillid', 0)
        currentPanelSkills = owner.getCurrentPanelSkills()
        skills.append(general)
        tskills = [SSD.data.get(skill_idx, {}).get('Skillid', 0) for skill_idx in data.get('skills', ())]
        tskills = [skillid for skillid in tskills if (skillid in owner.skills)]
        tskills.sort()
        for i in xrange(2):
            switch = ((owner.skillSwitch + i) % 2)
            if (switch < len(currentPanelSkills)):
                for idx in xrange(4):
                    if (idx < len(currentPanelSkills[switch])):
                        skills.append(currentPanelSkills[switch][idx])
                    else:
                        skills.append(0)
            else:
                for idx in xrange(4):
                    skills.append(0)
        data = owner.getCombatSkillsData()
        skills.append(data.get('dodge', 0))
        if owner.selectESkills:
            for i in xrange(2):
                if (i < len(owner.selectESkills[0])):
                    es = owner.selectESkills[0][i]
                    eskill = owner.EquipSkills.get(es, None)
                    if (eskill is None):
                        skills.append(0)
                        continue
                    skill = eskill.GetSkill()
                    if ((skill is None) or (not skill.enable)):
                        skills.append(0)
                        continue
                    skills.append(skill.id)
                else:
                    skills.append(0)
        else:
            for i in xrange(2):
                skills.append(0)
        for _ in xrange(2):
            skills.append(0)
        skills.append(owner.getChildISkillId())
        return skills

    def _get_ordinary_skills_monster_shapeshift(self):
        skills = []
        owner = EntityManager.getentity(self.ownerid)
        combatSkillsData = owner.getCombatSkillsData()
        currentPanelSkills = owner.getCurrentPanelSkills()
        general = combatSkillsData.get('GeneralAttack', 0)
        if (owner.isInSurvivalBattle() and (owner.monster_shapeshift in SCRD.data.iterkeys())):
            general = SCRD.data[owner.monster_shapeshift]
        skills.append(general)
        for i in xrange(2):
            switch = ((owner.skillSwitch + i) % 2)
            if (switch < len(currentPanelSkills)):
                for idx in xrange(4):
                    if (idx < len(currentPanelSkills[switch])):
                        skills.append(currentPanelSkills[switch][idx])
                    else:
                        skills.append(0)
            else:
                for idx in xrange(4):
                    skills.append(0)
        dodge = combatSkillsData.get('dodge', 0)
        skills.append(dodge)
        if owner.isInSurvivalBattle():
            if owner.selectESkills:
                for i in xrange(2):
                    if (i < len(owner.selectESkills[0])):
                        es = owner.selectESkills[0][i]
                        eskill = owner.EquipSkills.get(es, None)
                        if (eskill is None):
                            skills.append(0)
                            continue
                        skill = eskill.GetSkill()
                        if ((skill is None) or (not skill.enable)):
                            skills.append(0)
                            continue
                        skills.append(skill.id)
                    else:
                        skills.append(0)
            else:
                for i in xrange(2):
                    skills.append(0)
        for _ in xrange(3):
            skills.append(0)
        return skills

    def _get_ordinary_skills(self):
        skills = []
        owner = EntityManager.getentity(self.ownerid)
        general = SSD.data.get(SISD.data.get(owner.school, {}).get('general', 0), {}).get('Skillid', 0)
        currentPanelSkills = owner.getCurrentPanelSkills()
        skills.append(general)
        switch = max(0, min(len(currentPanelSkills), owner.skillSwitch))
        for i in xrange(2):
            switch = ((owner.skillSwitch + i) % 2)
            if (switch < len(currentPanelSkills)):
                for idx in xrange(4):
                    if (idx < len(currentPanelSkills[switch])):
                        skills.append(currentPanelSkills[switch][idx])
                    else:
                        skills.append(0)
            else:
                for idx in xrange(4):
                    skills.append(0)
        data = owner.getCombatSkillsData()
        skills.append(data.get('dodge', 0))
        if owner.selectESkills:
            for i in xrange(2):
                if (i < len(owner.selectESkills[0])):
                    es = owner.selectESkills[0][i]
                    eskill = owner.EquipSkills.get(es, None)
                    if (eskill is None):
                        skills.append(0)
                        continue
                    skill = eskill.GetSkill()
                    if ((skill is None) or (not skill.enable)):
                        skills.append(0)
                        continue
                    skills.append(skill.id)
                else:
                    skills.append(0)
        else:
            for i in xrange(2):
                skills.append(0)
        skills.extend(owner.spaceItems.getSkills())
        skills.append(owner.getChildISkillId())
        skills.append(owner.getAwakeISkillId())
        return skills

    @rpc_method(CLIENT_STUB, Dict())
    def onPokemonAttackResult(self, result):
        pokemon = self.getCombatPokemon()
        if (not pokemon):
            pokemon.onAttackResult(result)

    def getAvlSkills(self):
        owner = EntityManager.getentity(self.ownerid)
        if owner.school_shapeshift:
            return self._get_ordinary_skills_school_shapeshift()
        elif owner.monster_shapeshift:
            return self._get_ordinary_skills_monster_shapeshift()
        elif owner.model_shapeshift:
            return self._get_ordinary_skills()
        return self._get_ordinary_skills()

    def updateSkills(self, reset=True):
        (reset and GlobalData.playerMain and GlobalData.playerMain.InitRotateSkill())
        owner = EntityManager.getentity(self.ownerid)
        self.slots = []
        skills = self.getAvlSkills()
        for (slotid, skillid) in enumerate(skills):
            if (slotid in (10, 11)):
                skill = owner.skills_hub.get(const.SKILL_SRC_EQUIP, {}).get(skillid, None)
            elif (slotid in (12, 13)):
                skill = owner.skills_hub.get(const.SKILL_SRC_SPACE_ITEM, {}).get(skillid, None)
            elif (slotid == 14):
                skill = owner.skills_hub.get(const.SKILL_SRC_CHILD, {}).get(skillid, None)
            elif (slotid == 15):
                skill = owner.skills_hub.get(const.SKILL_SRC_AWAKE, {}).get(skillid, None)
            else:
                skill = owner.skills.get(skillid, None)
            if (skill is None):
                self.slots.append(SkillManager.Slot(0, slotid, self.ownerid))
            else:
                self.slots.append(SkillManager.ComboSlot(skill.id, skill.level, slotid, self.ownerid))
        self.UpdateSkillUI()

    def UpdateSkillUI(self):
        owner = EntityManager.getentity(self.ownerid)
        if (not hasattr(owner, 'model')):
            return
        if (not hasattr(self, 'uistamp')):
            self.uistamp = 0
        self.uistamp += 1
        GlobalData.p.add_timer(0, utils.Functor(self._UpdateSkillUI, self.uistamp))

    def _UpdateSkillUI(self, stamp):
        if (getattr(self, 'uistamp', 0) != stamp):
            return
        PlayerMain().onSetSkillSlots()
        PlayerMain().onSetSelectESkills()
        PlayerMain().onSetSpaceItemSkills()
        PlayerMain().onSetChildSkill()
        PlayerMain().onSetAwakeSkill()

    def showSkillResult(self, skillid, skilllevel, attacker, resultmap):
        owner = EntityManager.getentity(self.ownerid)
        owner.sActionM.showSkillResult(skillid, skilllevel, attacker, resultmap)

    def SkillUsedM(self, skillid):
        s = self.getSlotBySkillid(skillid)
        if s:
            s.onSkillUsedS(skillid)
        self.skillNext = (skillid, 0)
        owner = EntityManager.getentity(self.ownerid)
        slot = self.getSlotBySkillid(skillid)
        if slot:
            slot.updateSkillState(skillid, self.skillNext[1])
        skill = owner.GetSkill(skillid)
        if skill.JoystickYaw():
            (sskillid, sstate) = self.skillRunning
            if (sstate <= 1):
                slot = self.getSlotBySkillid(sskillid)
                if slot:
                    slot.updateSkillState(sskillid, (-1))

    def SkillStartM(self, skillid):
        self.comboAllowed = False
        s = self.getSlotBySkillid(skillid)
        if s:
            s.onSkillStartS(skillid)
        if (self.skillNext[0] == skillid):
            self.skillRunning = (skillid, 1)
            slot = self.getSlotBySkillid(skillid)
            if slot:
                slot.updateSkillState(skillid, self.skillRunning[1])
        self.skillNext = (0, 5)
        owner = EntityManager.getentity(self.ownerid)
        if AwakeConst.canPopAwakeDamageText(skillid, owner):
            owner.add_timer(0.1, (lambda : AwakeSkillResult()))

    def SkillCalcM(self, skillid):
        if (self.skillRunning[0] == skillid):
            self.skillRunning = (skillid, 2)
            slot = self.getSlotBySkillid(skillid)
            if slot:
                slot.updateSkillState(skillid, self.skillRunning[1])

    def SkillPostM(self, skillid):
        if (self.skillRunning[0] == skillid):
            self.skillRunning = (skillid, 3)
            slot = self.getSlotBySkillid(skillid)
            if slot:
                slot.updateSkillState(skillid, self.skillRunning[1])

    def SkillProgressM(self, skillid):
        if (self.skillRunning[0] == skillid):
            self.skillRunning = (skillid, 2)

    def SkillMovePostM(self, skillid):
        if (self.skillRunning[0] == skillid):
            self.skillRunning = (skillid, 4)
            slot = self.getSlotBySkillid(skillid)
            if slot:
                slot.updateSkillState(skillid, self.skillRunning[1])

    def SkillEndM(self, skillid):
        self.comboAllowed = False
        self.SkillPostM(skillid)
        slot = self.getSlotBySkillid(skillid)
        if slot:
            slot.onSkillEndS(skillid)
        if (self.skillRunning[0] == skillid):
            self.skillRunning = (0, 5)
            if slot:
                slot.updateSkillState(skillid, self.skillRunning[1])

    def blockBySlot(self, skillid):
        s = self.getSlotBySkillid(skillid)
        if (s and (not s.canUse(skillid))):
            return True
        return False

    def blockByRunningSkill(self, skillid):
        owner = EntityManager.getentity(self.ownerid)
        skill = owner.GetSkill(skillid, restrict=1)
        if (not skill.level):
            return True
        res = False
        (sskillid, sstate) = self.skillRunning
        sskill = owner.GetSkill(sskillid, restrict=1)
        if (skill.JoystickYaw() and ((sskill is None) or (not sskill.JoystickYaw()))):
            return sskill.isChildSkill()
        if skill.isEquipSkill():
            return False
        if (skill.isChildSkill() and (not sskill.isChildSkill())):
            return False
        if sskill.level:
            if sskill.isEquipSkill():
                res = True
            elif sskill.isChildSkill():
                res = True
            elif sskill.isComboSucceed(skillid):
                res = (not owner.skillmgr.comboAllowed)
            elif (sstate in (0, 1)):
                res = (sskill.priority >= skill.priority)
            elif (sstate >= 3):
                res = False
            else:
                res = True
        if res:
            return True
        (nskillid, nstate) = self.skillNext
        nskill = owner.GetSkill(nskillid, restrict=1)
        if nskill.level:
            if nskill.isEquipSkill():
                res = True
            elif nskill.isChildSkill():
                res = True
            elif (nstate in (0, 1)):
                res = (nskill.priority >= skill.priority)
            elif (nstate >= 3):
                res = False
            else:
                res = True
        return res

    def getCurrentSkillid(self, slotid):
        if (slotid >= len(self.slots)):
            return 0
        return self.slots[slotid].skillid

    def getSlotSkills(self, slotid):
        if (slotid >= len(self.slots)):
            return []
        return self.slots[slotid].skillids

    def getSlotBySkillid(self, skillid):
        for s in self.slots:
            s_skillid = s.skillid
            if ((not s_skillid) or ((skillid not in s.skillids) and (s_skillid != skillid))):
                continue
            return s
        return None

    def ComboAllowedM(self, skillid):
        self.comboAllowed = True
        PlayerMain().OnComboAllowed(skillid)

    def ComboBanedM(self, skillid):
        self.comboAllowed = False
        PlayerMain().OnComboBaned(skillid)

    def ComboFailedM(self, skillid):
        self.comboAllowed = False
        s = self.getSlotBySkillid(skillid)
        if s:
            s.reset()

    def onCurrentUsed(self, slotid):
        if (slotid >= len(self.slots)):
            return
        self.slots[slotid].used()

    def reset(self, slotid):
        if (slotid >= len(self.slots)):
            return
        self.slots[slotid].reset()

    def canUseSkill(self, skillid):
        for slot in self.slots:
            if (slot.skillid == skillid):
                return True
        return False

    def hasSlot(self, slotid):
        if (slotid >= len(self.slots)):
            return False
        return (self.slots[slotid].skillid != 0)

    def canUseGeneralAttack(self):
        owner = EntityManager.getentity(self.ownerid)
        return self.canUseSkill(owner.getCombatSkillsData().get('GeneralAttack', 0))

    def startHolding(self, slotid):
        if (slotid >= len(self.slots)):
            return
        self.skillHolding = self.slots[slotid].skillid

    def isHolding(self):
        return (self.skillHolding > 0)

    def stopHolding(self):
        self.skillHolding = 0

    def onReleaseHold(self, position):
        if self.isHolding():
            owner = EntityManager.getentity(self.ownerid)
            (owner and owner.onReleaseHold(self.skillHolding, position))
            self.stopHolding()

    def onChargeStart(self, slotid):
        if (slotid >= len(self.slots)):
            return False
        self.slots[slotid].chargeStart()

    def onChargeEnd(self, slotid):
        if (slotid >= len(self.slots)):
            return False
        return self.slots[slotid].chargeEnd()

class SkillSyncState(object, ):

    def __init__(self, owner):
        self.ownerid = owner.id
        self.skillUsing = 0

    def skillStart(self):
        self.skillUsing += 1
        owner = EntityManager.getentity(self.ownerid)
        if getattr(self, 'checkSkillUseTimer', None):
            owner.cancel_timer(self.checkSkillUseTimer)
        self.checkSkillUseTimer = owner.add_timer(10.0, self._checkSkillEndSuccess)

    def skillEnd(self):
        self.skillUsing -= 1

    def _checkSkillEndSuccess(self):
        self.checkSkillUseTimer = None
        owner = EntityManager.getentity(self.ownerid)
        if self.skillUsing:
            owner.syncPosOn()
            self.skillUsing = 0

class AvatarMember(cCombatUnit, ):
    Property('ai')
    CombatType = 1

    def __post_component__(self, bdict):
        cCombatUnit.__post_component__.im_func(self, bdict)

    def __tick_component__(self, dtime):
        (getattr(self, 'isPosReady', False) and self.AITick(dtime))
        fight_target = getattr(self, 'target', None)
        if callable(getattr(fight_target, 'updateFocusLogo', None)):
            fight_target.updateFocusLogo()

    def updateAllVisible(self):
        ModelSeqLoader().RefreshDismiss()

    def updateVisibleEntity(self, targetId):
        ModelSeqLoader().RefreshDismissEntity(targetId)

    def _on_set_invisible(self, old):
        self.updateVisibleEntity(self.id)
        if (self.invisible and (self.id == getattr(GlobalData.p.target, 'id', 0))):
            GlobalData.p.lockTarget(None)

    def _on_set_hp(self, old, attacker=None):
        cCombatUnit._on_set_hp.im_func(self, old, attacker)
        pokemon = self.getCombatPokemon()
        (pokemon and pokemon.updatePokemonSacrificeEffect())

    def BelongTo(self, entity):
        return (self.id == getattr(entity, 'id', None))

    def getSpeedUpperLimit(self):
        return 7.15

    def getVisiability(self):
        if GlobalData.hideAllAvatar:
            return False
        player = GlobalData.p
        if (self.hsRole == HsConst.ROLE_HIDE):
            return True
        if (self.isPlayOffWatcher and (player is not self)):
            return False
        if (player.d_ride_info and (player.d_ride_info[0] == self.id)):
            return True
        if self.isInWedding():
            return True
        isPhotoing = getattr(GlobalData, 'isPhotoing', False)
        if isPhotoing:
            flag = True
            value = config.LocalConfig.PhotoSettings.get(cconst.PHOTO_KEY_VISIBILITY, cconst.PHOTO_VSB_VALUE_ALL)
            if (value == cconst.PHOTO_VSB_VALUE_ALL):
                flag = True
            elif (value == cconst.PHOTO_VSB_VALUE_TEAM):
                flag = ((player is self) or (self.id in (getattr(player, 'team', None) or list())))
            elif (value == cconst.PHOTO_VSB_VALUE_SELF):
                flag = (player is self)
            if (not flag):
                return False
        if ((player is self) and getattr(self, 'isNpcSpecialScreen', False)):
            return False
        if (getattr(GlobalData, 'F11_flag', 0) and (not isPhotoing)):
            if (player.relation(self) == 3):
                return False
        return cCombatUnit.getVisiability.im_func(self)

    def replaceInvisibleModels(self, model_data):
        if (self.model.isValid() and (not txm.canUseTrans()) and self.invisible and (not getattr(self, 'attack_show_model', 0))):
            model_data['Models'] = model_data.get('InvisibleModels', ())

    def getCombatProtoID(self):
        if self.isFaking:
            if self.replacement_no:
                return self.replacement_no
            if self.school_shapeshift:
                return school_data.data.get(self.school_shapeshift, {}).get('BodyCombatproto', {}).get(0, 0)
            elif self.monster_shapeshift:
                return CD.data.get(self.monster_shapeshift, {}).get('combatproto', 0)
            else:
                fakeData = self.fakeData
                return school_data.data.get(fakeData.school, {}).get('BodyCombatproto', {}).get(fakeData.body, 0)
        return cCombatUnit.getCombatProtoID.im_func(self)

    def getModelData(self):
        if self.isInSurvivalBattle():
            return self.getSurvivalModelData()
        model_data = dict(cCombatUnit.getModelData.im_func(self))
        flag = False
        if hasattr(GlobalData, 'EditorModelData'):
            model_data = GlobalData.EditorModelData
            flag = True
        if hasattr(GlobalData, 'EditorWorkdGraph'):
            model_data['BasicGraph'] = GlobalData.EditorWorkdGraph
            flag = True
        if flag:
            return model_data
        if self.hasShapeShift:
            self.replaceInvisibleModels(model_data)
            return model_data
        if self.isFaking:
            fakeData = self.fakeData
            model_data = DataHelper.GetSchoolModelData(fakeData.school, fakeData.equips, model_data, fakeData.dressing, body=fakeData.body, dresscolor=fakeData.dressingColor)
        else:
            rubbingGetter = self.rubbing.get
            equipmentsGetter = self.gameItems.equipments.get
            equips = [x for x in [(rubbingGetter(part, 0) or equipmentsGetter(part, dict()).get('id', 0)) for part in const.EQU_BODYPARTS] if x]
            dressingColor = DressColor.copy()
            if hasattr(self, 'wardrobe'):
                for (key, value) in self.dressing.iteritems():
                    if ((value in self.wardrobe.keys()) and (self.wardrobe[value].usedColor != (-1))):
                        dressingColor[key] = self.wardrobe[value].usedColor
            elif hasattr(self, 'colorEquiped'):
                dressingColor = self.colorEquiped
            if hasattr(self, 'dressingColor'):
                dressingColor = self.dressingColor
            cloakModelChoose = 0
            if hasattr(self, 'cloakModelChoose'):
                cloakModelChoose = self.cloakModelChoose
            model_data = DataHelper.GetSchoolModelData(self.school, equips, model_data, (self.tryDressing if getattr(self, 'isTryingDress', False) else self.dressing), body=self.body, dresscolor=(self.tryDressingColor if getattr(self, 'isTryingDress', False) else dressingColor), cloakModelChoose=cloakModelChoose)
        model_data = self.tryReplaceLowModel(model_data)
        self.replaceInvisibleModels(model_data)
        return model_data

    def getSurvivalModelData(self):
        model_data = dict(cCombatUnit.getModelData.im_func(self))
        if self.model_shapeshift:
            model_data = dict(CPD.data.get(self.model_shapeshift, {}))
            return model_data
        if getattr(self, 'survivalSpecialHideBuff', None):
            model_data = self.getSurvivalSpecialHideModelData()
            return model_data
        from iSurvivalBattle import SurvivalBattleConst
        if (self.survivalProtoNo not in SurvivalBattleConst.SHAPE_SHIFT_NOS):
            self.replaceInvisibleModels(model_data)
            return model_data
        equipmentsGetter = self.survivalGameItems.equipments.get
        equips = [x for x in [equipmentsGetter(part, dict()).get('id', 0) for part in const.EQU_BODYPARTS] if x]
        dressingColor = DressColor.copy()
        dresscolor = getattr(self, 'view_dressing_color', dressingColor)
        model_data = DataHelper.GetSchoolModelData(self.survivalSchool, equips, model_data, None, dresscolor=dresscolor)
        model_data = self.tryReplaceSurvivalLowModel(model_data)
        self.replaceInvisibleModels(model_data)
        return model_data

    def hideExtraModel(self, state):
        if ((self is GlobalData.p) and any((buff.kanbujian() for buff in getattr(self, 'buffs', dict()).itervalues()))):
            self.server.removeAllInvisibleBuffs()

    def showExtraModel(self, state):
        pass

    def updateExtraModel(self):
        pass

    def tryReplaceLowModel(self, model_data):
        if (space_data.data.get(self.spaceno, {}).get('useUglyModel', 0) == 1):
            model_data = dict(cCombatUnit.getModelData.im_func(self))
            model_data['Models'] = school_data.data.get(self.school, {}).get('BodyuglyModel', {}).get(self.body, model_data)
        return model_data

    def tryReplaceSurvivalLowModel(self, model_data):
        if (space_data.data.get(self.spaceno, {}).get('useUglyModel', 0) == 1):
            model_data = dict(cCombatUnit.getModelData.im_func(self))
            model_data['Models'] = school_data.data.get(self.survivalSchool, {}).get('BodyuglyModel', {}).get(self.body, model_data)
        return model_data

    def getUIModelData(self):
        model_data = dict(CPD.data.get(school_data.data.get(self.school, {}).get('BodyCombatproto', {}).get(self.body, 0), {}))
        rubbingGetter = self.rubbing.get
        equipmentsGetter = self.gameItems.equipments.get
        equips = [x for x in [(rubbingGetter(part, 0) or equipmentsGetter(part, dict()).get('id', 0)) for part in const.EQU_BODYPARTS] if x]
        dressingColor = DressColor.copy()
        for (key, value) in self.dressing.iteritems():
            if ((value in self.wardrobe.keys()) and (self.wardrobe[value].usedColor != (-1))):
                dressingColor[key] = self.wardrobe[value].usedColor
        dresscolor = getattr(self, 'view_dressing_color', dressingColor)
        cloakModelChoose = getattr(self, 'cloakModelChoose', 0)
        model_data = DataHelper.GetSchoolModelData(self.school, equips, model_data, getattr(self, 'view_dressing', self.dressing), body=self.body, dresscolor=dresscolor, cloakModelChoose=cloakModelChoose)
        return model_data

    def getSurvivalUIModelData(self, protoNo):
        model_data = dict(CPD.data.get(protoNo, {}))
        equipmentsGetter = self.survivalGameItems.equipments.get
        equips = [x for x in [equipmentsGetter(part, dict()).get('id', 0) for part in const.EQU_BODYPARTS] if x]
        dressingColor = DressColor.copy()
        dresscolor = getattr(self, 'view_dressing_color', dressingColor)
        model_data = DataHelper.GetSchoolModelData(self.survivalSchool, equips, model_data, None, dresscolor=dresscolor)
        return model_data

    def _on_set_pvp_mode(self, old):
        if (old == self.pvp_mode):
            return
        if getattr(self, 'model', None):
            self.model.SetVariableF(0, 'PVP_MODE', self.pvp_mode)

    def isProtectedFromAvts(self):
        if (self.pkRole == 1):
            return False
        return cCombatUnit.isProtectedFromAvts.im_func(self)

    def isAvtsProtectedFrom(self):
        if (self.pkRole == 1):
            return False
        return cCombatUnit.isAvtsProtectedFrom.im_func(self)

    def getCombatSkillsData(self):
        if self.school_shapeshift:
            return school_data.data.get(self.school_shapeshift, {})
        elif self.monster_shapeshift:
            return CD.data.get(self.monster_shapeshift, {})
        elif self.model_shapeshift:
            return school_data.data.get(self.school, {})
        return school_data.data.get(self.school, {})

    def setNavigationFlag(self, val):
        if ((not self._navigationflag) and val):
            (GlobalData.camera and GlobalData.camera.enterNavigateMode())
        elif (self._navigationflag and (not val)):
            (GlobalData.camera and GlobalData.camera.exitNavigateMode())
        cCombatUnit.setNavigationFlag.im_func(self, val)

    def onDead(self, killer=0, skillid=0, skilllevel=0):
        if self.isQinggong():
            self.stopQinggong()
        cCombatUnit.onDead.im_func(self, killer, skillid, skilllevel)
        if hasattr(self, 'OnJoyStickSelectEnd'):
            self.OnJoyStickSelectEnd()
        p = GlobalData.p
        if ((self is p) or (p.team and (p.teamid == self.teamid))):
            p.checkAceMark(exclude=(self.id,))
        (GlobalData.camera and GlobalData.camera.onAvatarGone(self))
        if hasattr(self, 'clearArenaKillTimes'):
            self.clearArenaKillTimes()

    def onRelive(self):
        cCombatUnit.onRelive.im_func(self)
        self.model.ProcessModelSfxs()
        self.model.refreshAttachmentSFXs()

    @rpc_method(CLIENT_STUB, Int())
    def ClearSkillCD(self, skillid=(-1)):
        cCombatUnit.ClearSkillCD.im_func(self, skillid)
        PlayerMain().onSetSkillSlots()

    @rpc_method(CLIENT_STUB)
    def OnJoyStickSelectActBegin(self):
        self.model.gotoLocomotion(0.03)
        self.model.SetSendActivatedSignal(0, 'joystick_cycle', True)
        self.model.FireEvent(0, '@joystick_shake')

    @rpc_method(CLIENT_STUB)
    def OnJoyStickSelectActEnd(self):
        self.model.FireEvent(0, '@joystick_end')

    def onBeDamaged(self, skillid, skilllevel, damage, attacker, atktype, atkindex=0):
        cCombatUnit.onBeDamaged.im_func(self, skillid, skilllevel, damage, attacker, atktype, atktype)
        realDmg = CombatHelper.getDamageFromResult(damage)
        ((realDmg > 0) and self.model.FireEvent(0, '@onHit'))

    @rpc_method(CLIENT_STUB, Tuple(), Float())
    def attractedToPos(self, pos, time):
        if (not self.model.isValid()):
            return
        if self.buffs.ignoreSkillMove():
            return
        print 'jjj attract to pos', time, self
        time = 0.2
        diff = formula.substract3D(pos, self.position)
        direction = formula.vectorToYaw(diff)
        dist = float(formula.distance(pos, self.position))
        _motion = self.model.applyMotion(False)
        _gravity = self.model.applyGravity(False)
        _obstacle = self.model.navigator.EnableObstacle
        self.model.setNavigatorProp('EnableObstacle', False)
        self.model.gotoLocomotion(0)
        self.resetSkillState()
        speed = (dist / time)
        self.model.moveTo(pos, None, speed, True)
        self._is_attracting = True
        self.add_timer(time, (lambda : self.attractedEnd(direction, _motion, _gravity, _obstacle)))

    @rpc_method(CLIENT_STUB, Int(), Tuple())
    def OnCheckChangeConditions(self, stamp, res):
        print 'OnCheckChangeConditions >>>>>>>>>>>>>>>>>>', stamp, res
        if SchoolTransfer.isHide():
            return
        SchoolTransfer()._LayoutPage0(stamp, res)

    @rpc_method(CLIENT_STUB, Int(), Int())
    def OnCheckSpecialSkills(self, stamp, total):
        print 'OnCheckSpecialSkills >>>>>>>>>>>>>>>>>>', stamp, total
        if SchoolTransfer.isHide():
            return
        SchoolTransfer()._LayoutPage3(stamp, total)

    def attractedEnd(self, direction, motion, gravity, obstacle):
        print 'attractedEnd ===='
        self.yaw = direction
        self.model.cancelNavigator()
        self.model.applyMotion(motion)
        self.model.applyGravity(gravity)
        self.model.setNavigatorProp('EnableObstacle', obstacle)
        self._is_attracting = False
        self.server.attractedEnd()

    @rpc_method(CLIENT_STUB, Str(), Int(), Int(), Int(), Bool(), Int())
    def triggerEnterStory(self, graph, endEvent, showSelf, showOthers, canSkip, interactive=0, spaceEnd=0):
        if interactive:
            eid = IdManager.genid()
            doll = GlobalData.p.space.create_entity('Doll', eid, {'type': 5, 'stype': 5, 'invisible': True})
            model = getattr(doll, 'model', None)
            if ((doll is None) or (model is None)):
                utils.CallUntil(func=(lambda : self.doTriggerEnterStory(eid, graph, endEvent, showSelf, showOthers, canSkip, interactive)), condition=(lambda : ((self.space.getEntityByID(eid) is not None) and getattr(self.space.getEntityByID(eid), 'model', None))), delay=1.0).start()
            else:
                doll.model.enterStory(graph, endEvent=endEvent, showSelf=showSelf, showOthers=showOthers, canSkip=canSkip, spaceEnd=spaceEnd)
        elif getattr(GlobalData.p, 'model', None):
            if (not self.stateIM.applyInstruction(SICD.STORY)):
                return
            GlobalData.p.model.enterStory(graph, endEvent=endEvent, showSelf=showSelf, showOthers=showOthers, canSkip=canSkip, spaceEnd=spaceEnd)

    def doTriggerEnterStory(self, eid, graph, endEvent, showSelf, showOthers, canSkip, interactive):
        doll = self.space.getEntityByID(eid)
        (doll and doll.model.enterStory(graph, endEvent=endEvent, showSelf=showSelf, showOthers=showOthers, canSkip=canSkip))

    def _on_set_relationStamp(self, old):
        cCombatUnit._on_set_relationStamp.im_func(self, old)
        pokemon = self.getCombatPokemon()
        if pokemon:
            pokemon._on_set_relationStamp(0)

    @rpc_method(CLIENT_STUB, Int(), List(), Dict(), Tuple())
    def onSkillActionPlay(self, skillid, targetinfo, choose_pos, location_info):
        self.showAttachmentsInCloak()
        cCombatUnit.onSkillActionPlay.im_func(self, skillid, targetinfo, choose_pos, location_info)
        self.tryNotifySkillToShadowPokemon(skillid)

    def tryNotifySkillToShadowPokemon(self, skillid):
        if self.shadowPokemonId:
            shadowPokemon = self.getShadowPokemon()
            (shadowPokemon and shadowPokemon.onAvatarUseSkill(skillid))
PlayerAvatar = None

class PlayerAvatarMember(AvatarMember, ):
    Property('panelSkills', PanelSkills)
    Property('panelSkills2', PanelSkills)
    Property('selectESkills', PanelSkills)
    Property('_navigationflag', False)
    Property('teamTarget', None)
    Property('chargeStamp', 0)
    Property('skillSwitch', 0)
    Property('lastAttackTarget', '')
    Property('newbieRelive')
    Property('warRelive', 3)
    Property('reliveTime')
    Property('lastSkillSprt', 0)
    Property('cur_special', 0)
    Property('lastSpecialSwitch', 0)

    def _on_set_invisible(self, old):
        self.updateVisibleEntity(self.id)
        self.onCheckSummonPokemon()
        self.attack_show_model = 0
        self.wait_show_model_info = None
        if self.model.isModelValid():
            self.model.setIsCastDynamicShadow((not self.invisible), cconst.CDS_INVISIBLE)

    def _on_set_detective(self, old):
        self.updateAllVisible()

    def ResetSkillidCache(self):
        self.skillmgr.ResetSkillidCacheM()

    def ClearSkillCache(self):
        cCombatUnit.ClearSkillCache.im_func(self)
        self.ResetSkillidCache()

    def onBuffChanged(self):
        self.updateRideBtn()
        self.ResetSkillidCache()

    def navigateToPos(self, position, callback=None):
        walk_entity = self.getWalkEntity()
        if walk_entity:
            walk_entity.model.moveTo(position, callback)

    def getGeneralSkills(self):
        res = []
        ga = school_data.data.get(self.school, {}).get('GeneralAttack', 0)
        if (ga == 0):
            return res
        res.append(ga)
        skill = self.GetSkill(ga)
        skillcombo = skill.comboSucc
        while (skill and skillcombo and (skillcombo != skill.id) and (skillcombo not in res)):
            res.append(skillcombo)
            skill = self.GetSkill(skillcombo)
            skillcombo = skill.comboSucc
        return res

    def _checkTargetForSkill(self, target, skill):
        if ((skill.getType() != 3) and target and target.IsAvatar):
            if (target.isProtectedFromAvts() or self.isAvtsProtectedFrom()):
                return False
        return cCombatUnit._checkTargetForSkill.im_func(self, target, skill)

    def __init_component__(self, bdict):
        AvatarMember.__init_component__.im_func(self, bdict)
        self.server_first = False
        self.syncCombatRandomer = SyncableRandomer()

    def __post_component__(self, bdict):
        cCombatUnit.__post_component__.im_func(self, bdict)
        self.initSkillManager()
        self.initStateIM()
        self.initChangeSceneRule()
        self._curBtreeid = ''
        self.aceMark = False
        self.lastAttack = 0
        self.autoFightTimer = None
        self.npcTarget = None
        self.persistentStates = dict()
        self.skillCooler = SkillCooler()
        self.skillCDReducer = {}
        self.skillSyncState = SkillSyncState(self)

    def _on_set_cur_special(self, old):
        if (self.cur_special != old):
            self.OnSpecialSkillChange(old)

    def _on_set_isCombating(self, old):
        cCombatUnit._on_set_isCombating.im_func(self, old)
        combatPokemon = self.getCombatPokemon()
        (combatPokemon and combatPokemon._updateGraphStatus())
        self.ResetSkillidCache()
        if ((not self.isCombating) and self.navigationflag and (not self.isRiding)):
            self.hold()
            self.think()

    def _on_set_relationStamp(self, old):
        self.updateOthersTopLogo()
        self.delayRelationStampRefresh()
        self.update_space_level_shield()
        pokemon = self.getCombatPokemon()
        if pokemon:
            pokemon._on_set_relationStamp(0)

    def _on_set_is_dead(self, old):
        cCombatUnit._on_set_is_dead.im_func(self, old)
        if GlobalData.camera:
            GlobalData.camera.exitPkModeImmediately()
            if ((not self.isInCJBattle()) and (not self.isInDHYW2Space())):
                GlobalData.camera.resetCameraImmediately()
        self.UpdateHP()

    def _delayRelationStampRefresh(self):
        self.updateAllVisible()

    def calcAttackResult(self, targets, skillid, skilllevel, misc):
        for target in targets:
            if getattr(target, 'atk_flag', 0):
                continue
            target.atk_flag = True
            self.update_entity_level_shield(target.id)
        if self.server_first:
            skill = self.GetSkill(skillid, skilllevel)
            results = []
            if skill:
                for target in targets:
                    skillType = skill.getType()
                    if ((skillType != 4) and (len(targets) >= skill.getMinAffectNum())):
                        if (skillType != 3):
                            atktype = 0
                        else:
                            atktype = 4
                        damage = [[0, 0], [0, 0], [0, 0]]
                        bld = 0
                        results.append([target.id, damage, atktype, bld])
            finalResult = {'s': skillid, 'l': skilllevel, 'a': self.id, 'r': results}
            (misc.get('combo', False) and finalResult.update({'c': True}))
            print 'calcAttackResult >>>>>>>> finalResult', finalResult
            return finalResult
        return cCombatUnit.calcAttackResult.im_func(self, targets, skillid, skilllevel, misc)

    def switchSpecialSkill(self, skillid, com=None):
        skill = GlobalData.p.GetSkill(skillid, restrict=True)
        if (skill.level == 0):
            PopmsgPool().AddMsg(('\xe4\xba\xba\xe7\x89\xa9\xe7\xad\x89\xe7\xba\xa7\xe5\xb0\x9a\xe6\x9c\xaa\xe8\xbe\xbe\xe5\x88\xb0%s\xe8\xa7\xa3\xe9\x94\x81\xe7\xad\x89\xe7\xba\xa7' % skill.name))
            return
        if (skill.enable == 0):
            PopmsgPool().AddMsg(('%s\xe5\xb0\x9a\xe6\x9c\xaa\xe4\xb9\xa0\xe5\xbe\x97\xef\xbc\x8c\xe6\x97\xa0\xe6\xb3\x95\xe6\xbf\x80\xe6\xb4\xbb\xe4\xbd\xbf\xe7\x94\xa8' % skill.name))
            if com:
                itemid = SSSID.data.get(skillid, {}).get('id', 0)
                if itemid:
                    ResourceTips().showBrief(GameItem({'id': itemid}), com.getWorldPosition(), com.getContentSize(), 1, None)
            return
        print 'setSkillsSwitch A', skillid
        if (self.cur_special == skillid):
            return
        print 'setSkillsSwitch B', skillid
        if (skillid not in SSPD.data.get(self.school, {}).get('skills', ())):
            return
        print 'setSkillsSwitch C', skillid
        self.server.switchSpecialSkill(skillid)

    def setSkillEnable(self, skillid, enable):
        if (not self.GetSkill(skillid).level):
            return
        self.server.setSkillEnable(skillid, enable)

    def getCanLvUpSkills(self):
        if (self.getSkillSourceid() != 0):
            return {}
        hide_pskills = SSLD.data.get(self.school, {}).get(0, {}).get('hide_pskills', ())
        dodge = school_data.data.get(self.school, {}).get('dodge', 0)
        new_skills = getSchoolLevelSkills(self.school, self.lv)
        new_pskills = getSchoolLevelPSkills(self.school, self.lv)
        basic_skills_limit = self.lv
        res = {}
        for skill_idx in SISD.data.get(self.school, {}).get('basic_skills', ()):
            skillid = SSD.data.get(skill_idx, {}).get('Skillid', 0)
            if (not skillid):
                continue
            pskill = self.GetPSkill(skillid)
            if (pskill.level < basic_skills_limit):
                basic_skills_limit = pskill.level
            if (pskill.level < self.lv):
                res.setdefault('pskills', set()).add(skillid)
                res.setdefault('basic_skills', set()).add(skillid)
        for skillid in new_skills:
            skill = self.GetSkill(skillid)
            if (skill.level and (skill.level < basic_skills_limit)):
                res.setdefault('iskills', set()).add(skillid)
        for skillid in new_pskills:
            skill = self.GetPSkill(skillid)
            if (skill.level and (skill.level < basic_skills_limit)):
                res.setdefault('pskills', set()).add(skillid)
        if ('pskills' in res):
            res['pskills'] = res.get('pskills', set()).difference(hide_pskills)
        res.get('iskills', set()).discard(dodge)
        if (not res.get('pskills', None)):
            res.pop('pskills', None)
        if (not res.get('iskills', None)):
            res.pop('iskills', None)
        return res

    def getSkillLvUpLmt(self, skill_idx):
        basic_skills = SISD.data.get(self.school, {}).get('basic_skills', ())
        min_lv = self.lv
        if (skill_idx not in basic_skills):
            for idx in basic_skills:
                skillid = SSD.data.get(idx, {}).get('Skillid', 0)
                if (not skillid):
                    continue
                skill_type = SSD.data.get(idx, {}).get('Type', 0)
                if (skill_type == 1):
                    tskill = self.GetPSkill(skillid)
                else:
                    tskill = self.GetSkill(skillid)
                if (min_lv > tskill.level):
                    min_lv = tskill.level
        return min_lv

    def levelUpSkill(self, skill_idx):
        skillid = SSD.data.get(skill_idx, {}).get('Skillid', 0)
        skill_type = SSD.data.get(skill_idx, {}).get('Type', 0)
        if (skill_type == 1):
            if (skillid not in self.pskills):
                PopmsgPool().AddMsg('\xe6\x8a\x80\xe8\x83\xbd\xe6\x9c\xaa\xe4\xb9\xa0\xe5\xbe\x97')
                return
        elif (skillid not in self.skills):
            PopmsgPool().AddMsg('\xe6\x8a\x80\xe8\x83\xbd\xe6\x9c\xaa\xe4\xb9\xa0\xe5\xbe\x97')
            return
        self.server.levelUpSkill(skill_idx)

    def levelUpSkillMax(self, skill_idx):
        skillid = SSD.data.get(skill_idx, {}).get('Skillid', 0)
        skill_type = SSD.data.get(skill_idx, {}).get('Type', 0)
        if (skill_type == 1):
            if (skillid not in self.pskills):
                return
        elif (skillid not in self.skills):
            return
        self.server.levelUpSkillMax(skill_idx)

    def levelUpInitiateSkillsMax(self):
        self.server.levelUpInitiateSkillsMax()

    def levelUpPassiveSkillsMax(self):
        self.server.levelUpPassiveSkillsMax()

    def getAutoTargetRange(self):
        return school_data.data.get(self.school, {}).get('AutoTargetRange', 0)

    def getCombatSpeed(self):
        if self.d_ride_info:
            return school_data.data.get(self.school, {}).get('BodyDRideSpeed', {}).get(self.body, 0)
        if self.school_shapeshift:
            return school_data.data.get(self.school, {}).get('speed', 0)
        return self.getCombatSkillsData().get('speed', 0)

    @utils.crosserver_forbidden
    def confirmAssignCredit(self, credits):
        if self.monster_shapeshift:
            return
        t = [x for x in credits if x]
        if (not t):
            return False
        self.server.confirmAssignCredit(credits)
        return True

    @rpc_method(CLIENT_STUB, Tuple())
    def initSyncableRandomer(self, state):
        self.syncCombatRandomer.state = state

    def _on_set_school(self, old):
        cCombatUnit._on_set_school.im_func(self, old)
        if (__debug__ and hasattr(GlobalData, 'EditorWorkdGraph')):
            self.panelSkills = self.getDefaultPanelSkills()
        self.skillmgr.updateSkills()
        if GlobalData.playerMain:
            GlobalData.playerMain.onPlayerShapeshift()

    def _on_set_school_shapeshift(self, old):
        cCombatUnit._on_set_school_shapeshift.im_func(self, old)
        if (__debug__ and hasattr(GlobalData, 'EditorWorkdGraph')):
            self.panelSkills = self.getDefaultPanelSkills()
        self.skillSwitch = 0
        self.skillmgr.updateSkills()
        if GlobalData.playerMain:
            GlobalData.playerMain.onPlayerShapeshift()
        self.ResetSkillidCache()
        (self.hideExtraModel(cconst.HIDE_ATTCH_TYPE_SHAPE) if self.school_shapeshift else self.showExtraModel(cconst.HIDE_ATTCH_TYPE_SHAPE))
        if self.shadowPokemonId:
            self.adjustShadowPokemonScale(self.school_shapeshift, old)

    def _on_set_monster_shapeshift(self, old):
        cCombatUnit._on_set_monster_shapeshift.im_func(self, old)
        if (__debug__ and hasattr(GlobalData, 'EditorWorkdGraph')):
            self.panelSkills = self.getDefaultPanelSkills()
        if self.inOfflineSpace():
            if (self.school_shapeshift or self.monster_shapeshift):
                self.panelSkills2 = self.getDefaultPanelSkills()
        self.skillSwitch = 0
        self.skillmgr.updateSkills()
        if (not SkillPanel.isHide()):
            SkillPanel().hide(True)
        if GlobalData.playerMain:
            GlobalData.playerMain.onPlayerShapeshift()
        self.ResetSkillidCache()
        (self.hideExtraModel(cconst.HIDE_ATTCH_TYPE_SHAPE) if self.monster_shapeshift else self.showExtraModel(cconst.HIDE_ATTCH_TYPE_SHAPE))

    def _on_set_model_shapeshift(self, old):
        cCombatUnit._on_set_model_shapeshift.im_func(self, old)
        if GlobalData.playerMain:
            GlobalData.playerMain.onPlayerShapeshift()
        self.ResetSkillidCache()
        (self.hideExtraModel(cconst.HIDE_ATTCH_TYPE_SHAPE) if self.model_shapeshift else self.showExtraModel(cconst.HIDE_ATTCH_TYPE_SHAPE))

    def _on_set_replacement_no(self, old):
        cCombatUnit._on_set_replacement_no.im_func(self, old)
        (self.hideExtraModel(cconst.HIDE_ATTCH_TYPE_SHAPE) if self.replacement_no else self.showExtraModel(cconst.HIDE_ATTCH_TYPE_SHAPE))

    def _settarget(self, en):
        if (GlobalData.p == self):
            (GlobalData.camera and GlobalData.camera.onTargetSet(en))

    def transToSkillActionCallback(self, skillid):
        self.SkillStart(skillid)
        self.setSkillActionPosition(skillid)

    def transToSkillAction(self, skillid, targetinfo, choose_pos, location_info=()):
        if getattr(const, 'GRAPH_NODE_DELAY', 0):
            if getattr(self, 'skill_action_timer', None):
                self.cancel_timer(self.skill_action_timer)
            self.skill_action_timer = self.add_timer(const.GRAPH_NODE_DELAY, utils.Functor(self._transToSkillAction, skillid, targetinfo, choose_pos, location_info))
        else:
            if getattr(self, 'skill_action_timer', None):
                self.cancel_timer(self.skill_action_timer)
            self._transToSkillAction(skillid, targetinfo, choose_pos, location_info)

    def _transToSkillAction(self, skillid, targetinfo, choose_pos, location_info):
        self.skill_action_timer = None
        (sskillid, sstate) = self.skillstate.skillRunning
        sskill = self.GetSkill(sskillid, 1)
        skill = self.GetSkill(skillid, 1)
        if (skill is None):
            return False
        target_gid = 0
        skill_proto = skill.getSkillProto()
        if self.SkillDisable(skillid):
            return False
        if skill_proto:
            if ((sstate <= 2) and (sskill is not None) and sskill.isComboSucceed(skillid)):
                res = self.model.FireEvent(target_gid, ('@use_skill_%d' % skill_proto))
                self.setEndActionArgs((skillid, targetinfo, choose_pos, location_info))
                return res
            if hasattr(self, 'interruptSkill'):
                self.interruptSkill(skillid)
            res = self.model.JumpToState(target_gid, ('skill_%d' % skill_proto), 0.0)
            skill_mode = skill.getSkillMode()
            self.model.SetVariableI(target_gid, 'MODE', skill_mode)
            (EngineVersionCheck.engineLargerThan400278() and self.startCheckEngineSignalInterrupt(skillid))
        else:
            self.model.gotoLocomotion(0, True)
            MHelper.AddCallback(0, utils.Functor(self.transToSkillActionCallback, skillid))
            res = True
        if res:
            targetinfo = self.processSkillTargetInfo(skillid, targetinfo)
            skill_pos = self.calcSkillPosition(skillid, targetinfo, choose_pos, location_info)
            if (skill.getInstantMove() >= 0):
                self.enterInstantMove(skill.getInstantMove(), skill_pos)
            else:
                self.model.SetVariableV3(target_gid, 'G_MOTION_DEST_POS', MType.Vector3(*skill_pos))
            self.setStartActionArgs((skillid, targetinfo, skill_pos))
            self.setEndActionArgs(None)
        return res

    @property
    def isClientAhead(self):
        return True

    def isRunningFightAI(self):
        res = self.AIIsRunning()
        return res

    def AIIsRunning(self):
        return (not (not self._curBtreeid))

    def saveAI(self):
        self._activeTaskIdSaved = self.activeTaskId
        self.aiTypeSaved = self.getAIType()
        self.stopAutoFight()

    @rpc_method(CLIENT_STUB, Tuple())
    def restoreAI(self, position=None):
        if (getattr(self, 'aiTypeSaved', cconst.PLAYER_AI_TYPE_NONE) != cconst.PLAYER_AI_TYPE_NONE):
            if (not self.space.IsPersistent):
                self.position = (position or self.position)
            aiType = self.aiTypeSaved
            del self.aiTypeSaved
            if (self.isInArena() or self.isInBattle()):
                return
            self.activeTaskId = self._activeTaskIdSaved
            if (aiType == cconst.PLAYER_AI_TYPE_TASK):
                self.switchTaskAutoFight()
            elif (aiType == cconst.PLAYER_AI_TYPE_BT):
                self.switchAutoFight()
        elif getattr(self, 'isInAIRunning', False):
            self.switchAutoFight()
            delattr(self, 'isInAIRunning')

    def clearAI(self):
        if (getattr(self, 'aiTypeSaved', cconst.PLAYER_AI_TYPE_NONE) != cconst.PLAYER_AI_TYPE_NONE):
            del self.aiTypeSaved
            self._activeTaskIdSaved = 0

    @rpc_method(CLIENT_STUB)
    def recordAIState(self):
        self.isInAIRunning = self.isInAIRunningCurrent

    def getAIType(self):
        if (not self._curBtreeid):
            return cconst.PLAYER_AI_TYPE_NONE
        elif (self._curBtreeid == 'bttask'):
            return cconst.PLAYER_AI_TYPE_TASK
        else:
            return cconst.PLAYER_AI_TYPE_BT

    def resetFightStatus(self):
        pass

    def checkAceMark(self, exclude):
        self.aceMark = True
        for eid in (self.team or list()):
            avatar = getattr(self.space, 'avatars', dict()).get(eid)
            if ((not avatar) or (eid in exclude)):
                continue
            if avatar.isAlive():
                self.aceMark = False
                break

    def clearAceMark(self):
        self.aceMark = False

    def waitAutoFight(self):
        (self.autoFightTimer and self.cancel_timer(self.autoFightTimer))
        self.autoFightTimer = None
        delay = (space_data.data.get(self.spaceno, {}).get('AutoCombatDelayLeader', 0) if self.isTeamLeader() else space_data.data.get(self.spaceno, {}).get('AutoCombatDelay', 0))
        if (not delay):
            return
        self.autoFightTimer = self.add_timer(delay, self.startAutoFight)

    def startAutoFight(self):
        self.autoFightTimer = None
        if ((not self.isAlive()) or self.aceMark or self.AIIsRunning()):
            return
        now = time.time()
        delay = (space_data.data.get(self.spaceno, {}).get('AutoCombatDelayLeader', 0) if self.isTeamLeader() else space_data.data.get(self.spaceno, {}).get('AutoCombatDelay', 0))
        last = max(self.lastMove, self.lastAttack)
        if ((now - last) > delay):
            if self.isTeamLeader():
                MessageBox().show('\xe7\xa1\xae\xe8\xae\xa4\xe8\xbf\x9b\xe5\x85\xa5\xe8\x87\xaa\xe5\x8a\xa8\xe6\x8c\x82\xe6\x9c\xba\xe7\x8a\xb6\xe6\x80\x81\xef\xbc\x9f', {'callback': (lambda : setattr(self, 'autoFightTimer', self.add_timer(delay, self.startAutoFight)))}, {'callback': self.triggerAutoFight, 'countdown': 5})
            else:
                self.triggerAutoFight()
        else:
            self.autoFightTimer = self.add_timer((((last + delay) - now) + 1), self.startAutoFight)

    def triggerAutoFight(self):
        if self.isAutoRunningTask:
            self.runTask(self.activeTaskId)
        else:
            self.switchAutoFight()

    def stopMoveAttackTarget(self):
        if hasattr(GlobalData, 'moveAttackTargetId'):
            self.AIStop()
            del GlobalData.moveAttackTargetId

    @rpc_method(CLIENT_STUB)
    def stopAutoFight(self):
        if getattr(self, 'showTaskDebugInfo', False):
            if self._curBtreeid:
                msg = ('\xe5\x81\x9c\xe6\xad\xa2%s' % ('\xe4\xbb\xbb\xe5\x8a\xa1AI' if (self._curBtreeid == 'bttask') else '\xe8\xa1\x8c\xe4\xb8\xba\xe6\xa0\x91AI'))
                self.popWarningMsg(msg)
                self.logger.debug(msg)
        ((self._curBtreeid == 'bttask') and self.stopAutoRunTask())
        self.stopMoveAttackTarget()
        cCombatUnit.stopAutoFight.im_func(self)
        self._curBtreeid = ''
        ((not self.autoFightTimer) and self.waitAutoFight())
        PlayerMain().updateAutoFight()
        self.isInAIRunningCurrent = False

    def _getBehaviorTree(self):
        BehaviorTree = school_data.data.get(self.school, {}).get('BehaviorTree', ())
        BehaviorTree = ((BehaviorTree and BehaviorTree[4]) or '')
        DungeonBT = school_data.data.get(self.school, {}).get('DungeonBehaviorTree', {})
        if (self.space and (self.space.spaceno in DungeonBT)):
            BehaviorTree = DungeonBT[self.space.spaceno]
        return BehaviorTree

    @rpc_method(CLIENT_STUB)
    def switchAutoFight(self, team=True, overrideAI=''):
        if ((self.spaceno, self.school) in STAD.data):
            taskids = STAD.data[(self.spaceno, self.school)].get('tasks', ())
            currentTasks = set(self.getCurrentTaskList())
            for taskid in taskids:
                if (taskid in currentTasks):
                    self.tryStartAutoRunTask(taskid)
                    return
        self.stopMoveAttackTarget()
        if (self._curBtreeid != (overrideAI or self._getBehaviorTree())):
            self.stopAutoFight()
        if getattr(self, 'aiTypeSaved', None):
            del self.aiTypeSaved
        if (team and self.isInTeam()):
            self.teamRunAI()
            if (self.isTeamMember() and (not self.acceptTeamControl)):
                self.wantFollowLeader()
        else:
            BehaviorTree = (overrideAI or self._getBehaviorTree())
            print 'BehaviorTree ', BehaviorTree
            if BehaviorTree:
                self.AIRun(('bt%s' % BehaviorTree))
            PlayerMain().updateAutoFight()

    def switchTaskAutoFight(self):
        if getattr(self, 'aiTypeSaved', None):
            del self.aiTypeSaved
        if (self._curBtreeid != 'bttask'):
            if (self.isTeamMember() and self.acceptTeamControl):
                self.changeTeamStatus(1)
                self.stopAutoFight()
                self.popNotificationMsg('\xe4\xbd\xa0\xe5\xb7\xb2\xe5\x8f\x96\xe6\xb6\x88\xe8\xb7\x9f\xe9\x9a\x8f\xe9\x98\x9f\xe9\x95\xbf\xe7\x8a\xb6\xe6\x80\x81')
        self.AIRun('bttask')
        PlayerMain().updateAutoFight()

    def AIRun(self, btreeid):
        self.isInAIRunningCurrent = True
        self._curBtreeid = btreeid
        if (btreeid == 'bttask'):
            if getattr(self, 'showTaskDebugInfo', False):
                msg = '\xe6\x89\xa7\xe8\xa1\x8c\xe4\xbb\xbb\xe5\x8a\xa1AI'
                self.popWarningMsg(msg)
                self.logger.debug(msg)
            if (not getattr(self, 'ai', None)):
                self.ai = PlayerTaskSimpleAI(self)
            self.ai.state = self.ai.S_IDLE
            self.aiStopFlag = False
            self.think()
        else:
            if getattr(self, 'showTaskDebugInfo', False):
                msg = '\xe6\x89\xa7\xe8\xa1\x8c\xe8\xa1\x8c\xe4\xb8\xba\xe6\xa0\x91AI'
                self.popWarningMsg(msg)
                self.logger.debug(msg)
            cCombatUnit.AIRun.im_func(self, btreeid)
            for (name, value) in self.persistentStates.iteritems():
                self.AIWriteBlackBoard(name, value)

    def think(self):
        if ((self._curBtreeid == 'bttask') and getattr(self, 'ai', None)):
            if (getattr(self, 'shakeInfo', None) is not None):
                self.stopAutoFight()
            else:
                self.ai.think()
        else:
            cCombatUnit.think.im_func(self)

    def onAddCombo(self, cnt):
        cCombatUnit.onAddCombo.im_func(self, cnt)

    def initSkillManager(self):
        self.skillmgr = SkillManager(self.id)
        self.GeneralAttackSkills = []
        skillid = self.getCombatSkillsData().get('GeneralAttack', 0)
        while skillid:
            if (skillid in self.GeneralAttackSkills):
                break
            self.GeneralAttackSkills.append(skillid)
            skill = self.GetSkill(skillid)
            if (skill is None):
                break
            skillid = skill.comboSucc

    def relive(self, hp=None, mp=None):
        if self.server:
            self.server.reliveClick()
        else:
            self.onRelive()

    def onDead(self, killer=0, skillid=0, skilllevel=0):
        if self.isQinggong():
            self.stopQinggong()
        AvatarMember.onDead.im_func(self, killer, skillid, skilllevel)
        if ((not (self.isInCJBattle() and self.cjNearRelivePos())) and (not self.isInSurvivalBattle()) and (not self.isInHatKingBattle())):
            self.add_timer(3.0, ReliveBase.show)
        PlayerMain().onPlayerDead()
        (self.isInCJBattle() and (not CJRightCorner.isHide()) and CJRightCorner().onPlayerDead())
        MRender.GrayToPercent(1, 1)
        self.endQte(0)
        self.saveAI()
        if ((not GlobalData.gameActive) and (MConfig.Platform == 'windows') and hasattr(MPlatform, 'Vibrate')):
            MHelper.Vibrate()
        self.onExitOperationIdle()
        self.stateIM.applyInstruction(SICD.DEAD)

    def onRelive(self):
        AvatarMember.onRelive.im_func(self)
        ReliveBase.release()
        PlayerMain().onPlayerRelive()
        (self.isInCJBattle() and (not CJRightCorner.isHide()) and CJRightCorner().onPlayerRelive())
        MRender.GrayToPercent(0, 1)
        self.updatePlayerStatus()
        (self.stopAutoFight() if self.aceMark else self.waitAutoFight())
        self.model.leaveSpace()
        self.model.enterSpace()
        self.refreshEquipHalo()
        self.restoreAI(self.position)

    def _on_set_reliveTime(self, _):
        ReliveBase.updateReliveTime()

    def _on_set_skills_hub(self, old):
        print '[SKILL DEBUG] _on_set_skills_hub', self.skills_hub.keys(), old.keys()
        if hasattr(self, 'OnJoyStickSelectEnd'):
            self.OnJoyStickSelectEnd()
        self.OnSkillsChange()

    def obtainMonsterKilledAward(self, monster):
        if (not self.model.isValid()):
            return
        if (not self.stateIM.applyInstruction(SICD.COLLECT)):
            return
        if (getattr(self, 'collectTimer', None) in self._timers):
            self.cancel_timer(self.collectTimer)
        graph = (HRD.data.get(25, {}).get('path', '') if (self.school == 2) else HRD.data.get(24, {}).get('path', ''))
        self._collectGraphId = self.model.PushGraph(graph, 0.1, 0)
        monster.isCollected = True
        GlobalData.p.server.obtainMonsterKilledAward(monster.id)
        self.collectTimer = self.add_timer(1.5, self.stateIM.cancel_collecting)

    def onBeDamaged(self, skillid, skilllevel, damage, attacker, atktype, atkindex=0):
        cCombatUnit.onBeDamaged.im_func(self, skillid, skilllevel, damage, attacker, atktype, atktype)
        realDmg = CombatHelper.getDamageFromResult(damage)
        if (realDmg > 0):
            self.stateIM.applyInstruction(SICD.ONHIT)
            self.think()
        shotSkillTarget = skill_data.data.get((skillid, skilllevel), {}).get('shotSkillTarget', 0)
        if ((atktype not in (4, 5)) and (not self.target) and (not shotSkillTarget)):
            self.lockTarget(attacker)
        if getattr(self, 'delay_move_info', None):
            (x, y, z, flag) = self.delay_move_info
            if (flag == 1):
                self.position = (x, y, z)
                self.delay_move_info = None
        pokemon = self.getCombatPokemon()
        (pokemon and pokemon.onOwnerBeDamaged(skillid, attacker))
        ((realDmg > 0) and self.model.FireEvent(0, '@onHit'))
        if self.inOfflineSpace():
            iCombatUnit.onBeDamaged.im_func(self, skillid, skilllevel, damage, attacker, atktype)
            if (self.hp < (self.maxhp * 0.3)):
                self.startOfflineRecover(10)
        if attacker:
            attacker.atk_flag = True
            GlobalData.p.update_entity_level_shield(attacker.id)

    def startOfflineRecover(self, time):
        if (getattr(self, 'recoverCount', 0) > 0):
            return
        self.recoverCount = 5
        self.doOfflineRecover()

    def doOfflineRecover(self):
        self.recoverCount -= 1
        self.hp += (self.maxhp * 0.2)
        self.onStatusUpdate()
        self.model.attachEffect(HRD.data.get(41, {}).get('path', ''), 'root')
        if (self.recoverCount > 0):
            self.add_timer(1.5, self.doOfflineRecover)
        else:
            self.recoverCount = 0

    def calcSkillPosition(self, *args, **kwargs):
        if getattr(self, 'delay_move_info', None):
            (x, y, z, flag) = self.delay_move_info
            if (flag == 2):
                self.delay_move_info = None
                return (x, y, z)
        return cCombatUnit.calcSkillPosition.im_func(self, *args, **kwargs)

    def lockTeamTarget(self, target):
        self.teamTarget = target

    def lockTarget(self, target):
        if (target and target.IsMonster and (not target.isAlive())):
            return
        if (getattr(target, 'shield_flag', 0) >= 2):
            return
        if ((not self.detective) and (getattr(target, 'invisible', 0) and (self.relation(target) != 2))):
            return
        if (target and (target.IsNPC or target.IsChest or target.IsTreasure)):
            self.npcTarget = target
            target = None
        else:
            self.npcTarget = None
        originTarget = (self.target if getattr(self.target, 'model', None) else None)
        if (self.target and (self.target is target)):
            self.target = target
            self.hsCheckOnEntityClicked()
            return
        if (self.target and self.target.model and (not self.target.IsMagicField)):
            self.target.model.hideFocusEffect()
            self.target.model.SetEnvFlags(self.target.model.ENV_ID_SEL, False)
        if self.approach_target:
            self.approachTarget(None)
        cCombatUnit.lockTarget.im_func(self, target)
        if getattr(originTarget, 'updateBloodBar', None):
            originTarget.updateBloodBar()
        if getattr(self.target, 'updateBloodBar', None):
            self.target.updateBloodBar()
        self.updateTargetIndicator(target)
        if isinstance(self.target, MagicField):
            return
        if (self.target and (not self.isRunningFightAI())):
            self.target.model.showFocusEffect(self.relation(self.target))
            self.target.model.SetEnvFlags(self.target.model.ENV_ID_SEL, True)
        team = getattr(self, 'team', None)
        if (team and target):
            needReport = True
            for o in team:
                if (o == target.id):
                    needReport = False
                    break
            if needReport:
                self.reportAttackTarget(target.id)
        self.updateTargetStatus()
        PlayerMain().updateMemberHighlightUI(target)
        self.UpdateEntitySoundVol(originTarget)
        self.UpdateEntitySoundVol(target)
        self.hsCheckOnEntityClicked()
        self.updateCancelTargetButton()

    def showAutoPosChooser(self, skill):
        if skill.showAutoPosChooser():
            args = skill.getSpecialEffectArgs()
            (dist, speed, effectid) = args
            content = {'effectid': effectid, 'ownerid': self.id, 'speed': float(speed), 'position': formula.horizontalCoordinate(self.position, self.yaw, float(dist), 0), 'direction': self.yaw}
            self.autoPosChooser = Space().create_entity('Indicator', None, content)
            direction = formula.yawToVector(self.yaw)
            self.autoPosChooser.towards(direction[0], direction[(-1)])

    def hideAutoPosChooser(self):
        if getattr(self, 'autoPosChooser', None):
            self.autoPosChooser.destroy()
            self.autoPosChooser = None

    def setPVPMode(self, v):
        self.server.setPVPMode(v)

    def setChargeDirection(self, cancel=False, reset=False):
        if (not self.model.isValid()):
            return
        effectid = (cconst.CHARGE_DIRECTION_CANCEL if cancel else cconst.CHARGE_DIRECTION)
        needDettach = (getattr(self, 'charge_effectid', None) and ((getattr(self, 'charge_effectid_type', False) != cancel) or reset))
        if needDettach:
            self.model.detachEffect(self.charge_effectid, True)
            self.charge_effectid = None
        if reset:
            return
        if (getattr(self, 'charge_effectid', None) is None):
            self.charge_effectid = self.model.attachEffect(effectid, 'Scene Root')
        self.charge_effectid_type = cancel

    def OnStartCharing(self, slotid):
        self.chargeStamp += 1
        skillid = self.skillmgr.getCurrentSkillid(slotid)
        skill = self.GetSkill(skillid)
        self.updateShowSkillRange(skill)
        res = self.isSkillReady(skill)
        if (res != 1):
            return res
        res = self.doConfirmTarget(skill, seltgts=None, restricttgts=None)
        if (res != 1):
            return res
        if self.target:
            self.faceTo(self.target.position)
        if (skill.isChargeSkill() and self.stateIM.applyInstruction(SICD.CHARGE)):
            if self.invisible:
                self.wait_charge_slot = slotid
                self.skillmgr.onChargeStart(slotid)
                self.server.removeAllInvisibleBuffs()
                return 39
            PlayerMain().UpdateButtonBySlotid(slotid)
            self.skillmgr.onChargeStart(slotid)
            chargeTime = skill.maxChargeTime()
            chargeEndTime = (utils.getNow() + chargeTime)
            charge_style = skill_data.data.get((skill.id, max(1, skill.level)), {}).get('charge_style', 0)
            if (charge_style == 1):
                self.add_timer(chargeTime, utils.Functor(self.OnChargeFinish, slotid, self.chargeStamp))
            self.server.onChargeSkill(skillid, chargeEndTime)
            self.onChargeStart(skillid)
            PlayerMain().showChargeProgress(skill, chargeTime)
            self.showAutoPosChooser(skill)
            sp = skill_data.data.get((skill.id, skill.level), {}).get('charge_turning_speed', 0)
            if (sp > 0):
                self.charge_turning_speed = sp
                self.setChargeDirection()
            self.server.onBeforeSkill()
            return 1
        return 0

    def SetSkillCD(self, skillid, value, totaltime):
        cCombatUnit.SetSkillCD.im_func(self, skillid, value, totaltime)
        PlayerMain().UpdateAllSkillCD()

    def cancelCharge(self, slotid):
        if (not self.isCharging()):
            return
        skillBtn = PlayerMain().getSkillButton(slotid)
        PlayerMain().hideChargeProgress()
        self.stopCharging()
        skillBtn.StopCharging()
        self.setChargeDirection(reset=True)
        self.skillmgr.onChargeEnd(slotid)
        self.server.onCancelCharge()

    def OnChargeFinish(self, slotid, stamp=None):
        if ((stamp is not None) and (self.chargeStamp != stamp)):
            return
        if (not self.isCharging()):
            return
        skillBtn = PlayerMain().getSkillButton(slotid)
        skillid = self.skillmgr.getCurrentSkillid(slotid)
        skill = self.GetSkill(skillid)
        PlayerMain().hideChargeProgress()
        self.setChargeDirection(reset=True)
        charge_remove_delay = skill_data.data.get((skill.id, max(1, skill.level)), {}).get('charge_remove_delay', 0)
        self.stopCharging(delay=charge_remove_delay)
        self.server.onCancelCharge()
        choose_pos = None
        self.charge_turning_speed = 0
        if skill.showAutoPosChooser():
            choose_pos = [self.autoPosChooser.position]
            self.hideAutoPosChooser()
        chargeTime = self.skillmgr.onChargeEnd(slotid)
        charge_min_time_cd = skill_data.data.get((skill.id, max(1, skill.level)), {}).get('charge_min_time_cd', ())
        if charge_min_time_cd:
            charge_min_time = charge_min_time_cd[0]
            cd = (0 if (len(charge_min_time_cd) == 1) else charge_min_time_cd[1])
            if ((charge_min_time > 0) and (chargeTime < charge_min_time)):
                PlayerMain()._showSkillMessage(27)
                self.SetSkillCD(skillid, (cd + time.time()), cd)
                skillBtn.StopCharging()
                skillBtn.UpdateCD()
                self.server.onCancelCharge()
                self.stopCharging()
                return
        newskillid = skill.getChargeSkill(chargeTime)
        res = self.doConfirmTarget(skill, seltgts=([self.target.id] if self.target else None), restricttgts=None)
        if (res != 1):
            text = const.SKILL_ERR_MSG.get(res, '')
            (text and PopmsgPool().AddMsg(text))
            return
        self.doAttack(newskillid, choose_pos=choose_pos)
        PlayerMain().UpdateButtonBySlotid(slotid)

    def interruptCharging(self):
        self.stopCharging()
        PlayerMain().StopAllSkillCharging()
        self.charge_turning_speed = 0
        if (self.id == GlobalData.p.id):
            ((not getattr(self, 'screenEffectBlack', False)) and MRender.SetScreenColor(0, 0, 0, 0, 0.1))

    def interruptSkill(self, skillid):
        (curSkillid, curSkillState) = self.skillstate.skillRunning
        if (curSkillState > 3):
            return
        if (self.id != GlobalData.p.id):
            return
        if GlobalData.camera.motorBlender:
            GlobalData.camera.stopCurrSkillMove()
        ((not getattr(self, 'screenEffectBlack', False)) and MRender.SetScreenColor(0, 0, 0, 0, 0))
        MRender.MotionBlurToPercent(0, 0, 0.5, 0.5)

    def isDodgeOrQinggong(self):
        if ((not self.isCombating) and self.isInFly):
            return (0, False)
        dodge = self.getCombatSkillsData().get('dodge', 0)
        return (dodge, True)

    def dodgeBtnDisabled(self):
        return self.canDodge()

    def OnJoyStickSelectBegin(self, slotid):
        skillid = self.skillmgr.getCurrentSkillid(slotid)
        if (getattr(self, 'jsSelSkillid', 0) == skillid):
            pos = self.skillPosIndicator.position
            self.onReleaseHold(skillid, pos)
            self.OnJoyStickSelectEnd()
            return 1
        self.OnJoyStickSelectEnd()
        skill = self.GetSkill(skillid)
        res = self.isSkillReady(skill)
        if (res != 1):
            return res
        if (not Space.is_loaded()):
            return 0
        effects = skill.JoyStickSelEffect()
        effect1 = effects[0:1]
        effect2 = effects[1:2]
        content = {'effectid': (effect1[0][0] if effect1 else ''), 'effectradius': (effect1[0][1] if effect1 else 1.0), 'ownerid': self.id, 'speed': skill.JoyStickSelEffectSpeed(), 'warn_effectid': (effect2[0][0] if effect2 else ''), 'warn_effectradius': (effect2[0][1] if effect2 else 1.0)}
        self.skillPosIndicator = Space().create_entity('Indicator', None, content)
        self.jsSelSkillid = skillid
        PlayerMain().SkillCasting(skillid, True)
        self.OnJoyStickSelectActBegin()
        self.model.showSkillRange(skill.getRange(), isInRange=True)
        return 1

    def OnJoyStickSelectEnd(self):
        if (getattr(self, 'skillPosIndicator', None) is None):
            return
        self.skillPosIndicator.destroy()

    def OnIndictorDestroy(self, indcator):
        if (self.skillPosIndicator == indcator):
            PlayerMain().SkillCasting(self.jsSelSkillid, False)
            self.skillPosIndicator = None
            self.jsSelSkillid = 0
            self.model.FireEvent(0, '@joystick_end')

    def OnShowChooseModeEffect(self, skill, btn):
        if (not skill):
            return
        tgtlock = self.GetSkillTargetInRange(skill)
        if skill.chooseRangeEffect:
            self.chooseRangeEffect = self.model.play_effect_inner(skill.chooseRangeEffect, maxlife=(-1))
            (tgtlock and self.updateChooseModeEffectPos(tgtlock.position))
        if skill.chooseInnerEffect:
            self.chooseInnerEffect = self.model.play_effect_inner(skill.chooseInnerEffect, maxlife=(-1))
            if (skill.chooseMode == ChooseMode.Direction):
                if (tgtlock and (tgtlock.position != self.position)):
                    targetpos = tgtlock.position
                    yaw = (math.atan2((self.position[0] - targetpos[0]), (self.position[(-1)] - targetpos[(-1)])) + math.pi)
                else:
                    yaw = self.yaw
                self.updateChooseModeEffectDir(yaw)
            else:
                (tgtlock and btn.updateOffsetByPosition(tgtlock.position))

    def updateChooseModeEffectDir(self, yaw):
        if getattr(self, 'chooseInnerEffect', None):
            effect = self.model.getCueTypeEffect(self.chooseInnerEffect)
            if (not effect):
                return
            effect = effect[0]
            m = effect.Tach.Transform
            m.yaw = yaw
            effect.Tach.Transform = m

    def updateChooseModeEffectPos(self, pos):
        if getattr(self, 'chooseInnerEffect', None):
            effect = self.model.getCueTypeEffect(self.chooseInnerEffect)
            if (not effect):
                return
            effect = effect[0]
            m = effect.Tach.Transform
            m.translation = MType.Vector3(*pos)
            effect.Tach.Transform = m

    def OnDestroyChooseModeEffect(self):
        if getattr(self, 'chooseRangeEffect', None):
            self.model.detach_cue_type_effect(self.chooseRangeEffect, True)
            self.chooseRangeEffect = None
        if getattr(self, 'chooseInnerEffect', None):
            self.model.detach_cue_type_effect(self.chooseInnerEffect, True)
            self.chooseInnerEffect = None

    @rpc_method(CLIENT_STUB)
    def OnJoyStickSelectActBegin(self):
        AvatarMember.OnJoyStickSelectActBegin.im_func(self)
        self.server.OnJoyStickSelectActBegin()

    @rpc_method(CLIENT_STUB)
    def OnJoyStickSelectActEnd(self):
        AvatarMember.OnJoyStickSelectActEnd.im_func(self)
        self.server.OnJoyStickSelectActEnd()

    def OnSlotCancel(self, slotid, cancel=False):
        if cancel:
            self.cancelCharge(slotid)
        else:
            self.OnStopCharging(slotid)

    def OnSlotEnd(self, slotid):
        self.OnStopCharging(slotid)
        if getattr(self, 'comboholding', None):
            self.comboholding = False
            SkillChargeBar().comboStop()
            self.skillmgr.reset(slotid)
            PlayerMain().UpdateAllSkillIcon()
        else:
            PlayerMain().UpdateSkillEnable()

    def ComboReset(self, skillid=(-1)):
        ((not AutoSkillBar.isHide()) and AutoSkillBar().stop())
        self.removeAutoSkillEffect()
        camera = GlobalData.camera
        if camera.motorBlender:
            camera.stopCurrSkillMove()
        if (skillid == (-1)):
            skillid = self.skillstate.skillRunning[0]
        slot = self.skillmgr.getSlotBySkillid(skillid)
        if (not slot):
            return
        slotid = slot.slotid
        self.skillmgr.reset(slotid)
        PlayerMain().UpdateAllSkillIcon()

    def breakAutoCombo(self):
        (skillid, state) = self.skillstate.skillRunning
        self.SkillEnd(skillid)
        self.ComboReset()
        self.model.gotoLocomotion(0.5)
        self.resetSkillState()

    def OnStopCharging(self, slotid):
        if self.isCharging():
            self.chargeStamp += 1
            self.OnChargeFinish(slotid)
        self.skillmgr.onChargeEnd(slotid)

    def isChargeSucceed(self, chargeid):
        skill = self.GetSkill(chargeid)
        if (not skill):
            return False
        (t, targets) = self.verifySkillTargets(skill, skill.getRange())
        return (t == 1)

    def SetGeneralAtkHolding(self, v):
        self.gernal_attack_holding = v

    def OnComboHolding(self, slotid):
        res = self.OnSlotUsed(slotid)
        if (res != 1):
            return
        self.comboholding = True
        skillid = self.skillmgr.getCurrentSkillid(slotid)
        skill = self.GetSkill(skillid)
        holdTime = skill.getHoldingComboTime()
        SkillChargeBar().comboProgressShow(holdTime)

    def OnSlotUsed(self, slotid):
        if self.skillmgr.isHolding():
            self.skillmgr.stopHolding()
            return 0
        if getattr(self, 'comboholding', False):
            return 0
        skillid = self.skillmgr.getCurrentSkillid(slotid)
        if (not skillid):
            return 0
        skill = self.GetSkill(skillid)
        if (not skill):
            return 0
        if (self.isQinggong() and self.isGeneralSkill(skillid)):
            self.stopQinggong()
            return
        if (self.is3DNavigating() and self.isGeneralSkill(skillid)):
            self.stop3DNavigate()
            return
        if (getattr(self, 'wait_skill_break', None) and self._isSkillCDReady(skill)):
            self.breakAutoCombo()
        ready = self.isSkillReady(skill)
        if (ready != 1):
            return ready
        if skill.needChoosePosition():
            if ((not self.isRunningFightAI()) and (not skill.chooseMode)):
                needHold = True
                comboSuccChoosePos = getattr(self, 'comboSuccChoosePos', None)
                if comboSuccChoosePos:
                    (tskillid, tchoose_pos) = comboSuccChoosePos
                    if (tskillid == skillid):
                        needHold = False
                if needHold:
                    self.skillmgr.startHolding(slotid)
                    return 0
        if skill.chooseMode:
            effect = None
            if getattr(self, 'chooseInnerEffect', None):
                effect = self.model.getCueTypeEffect(self.chooseInnerEffect)
            if (not effect):
                return 40
            effect = effect[0]
            if (skill.chooseMode == ChooseMode.Direction):
                self.yaw = effect.Tach.Transform.yaw
                res = self.doAttack(skillid)
            elif (skill.chooseMode == ChooseMode.Position):
                offset = effect.Tach.Transform.translation
                pos = ((self.position[0] + offset.x), (self.position[1] + offset.y), (self.position[2] + offset.z))
                res = self.doAttack(skillid, choose_pos=[pos])
            else:
                res = 0
        else:
            res = self.doAttack(skillid)
        return res

    def GetSlotCDPercent(self, skillid):
        skill = self.GetSkill(skillid)
        if (skill is None):
            return 1.0
        (cur_cd, totaltime) = self.GetSkillCD(skillid)
        if (cur_cd >= self.GetSkillCCD()[1]):
            if (skill.getCoolDown() == 0.0):
                return 0.0
            return max(0.0, ((cur_cd - time.time()) / totaltime))
        else:
            if (self.GetSkillCCD()[2] == 0.0):
                return 0.0
            ccd = self.GetSkillCCD()
            return max(0.0, ((ccd[1] - time.time()) / ccd[2]))

    def onReleaseHold(self, skillid, choose_pos):
        choose_pos = [choose_pos]
        if choose_pos:
            if (len(choose_pos) == 1):
                self.faceTo(choose_pos[0])
            self.doAttack(skillid, choose_pos=choose_pos)

    def attackAngle(self, targetpos):
        if getattr(self, 'tendDirection', False):
            p1 = self.position
            p2 = targetpos
            v = MType.Vector3(*self.getModelFaceVector())
            p1 = MType.Vector3(p1[0], 0, p1[2])
            p2 = MType.Vector3(p2[0], 0, p2[2])
            vx = (p2 - p1)
            v.length = 1
            vx.length = 1
            cosv = min(1, max((-1), vx.dot(v)))
            return (math.acos(cosv) < cconst.TARGET_ANGLE)
        return True

    def shouldUseTeamTarget(self, skill, targets):
        if (not skill):
            return False
        skillType = skill.getType()
        return ((skillType == 3) and (not targets) and self.isInTeam() and self.teamTarget)

    def useSkill(self, *args, **kwargs):
        if (not self.stateIM.applyInstruction(SICD.USESKILL)):
            return 0
        self.showAttachmentsInCloak()
        cCombatUnit.useSkill.im_func(self, *args, **kwargs)
        return 1

    def getSkillDirection(self, skillid):
        if ((skillid in getattr(self, 'GeneralAttackSkills', ())) and (not self.target)):
            if getattr(self, 'shakeYaw', None):
                return self.shakeYaw
        skill = self.GetSkill(skillid)
        if (skill and skill.JoystickYaw()):
            if getattr(self, 'shakeJoystick', None):
                d = GlobalData.camera.getShakeDirection(*self.shakeJoystick)
                return d.yaw
            elif getattr(self, 'shakeYaw', None):
                return self.shakeYaw
            else:
                return self.yaw
        return cCombatUnit.getSkillDirection.im_func(self, skillid)

    def SpecialSkillCheck(self, skill):
        if (skill.getSpecialEffectType() == 110):
            GlobalData.CHASE_EFFECT_ARGS = 0
            if self.target:
                (speed, maxtime, distance, _) = skill.getSpecialEffectArgs()
                speed = float(speed)
                maxtime = float(maxtime)
                distance = float(distance)
                distance_m = (speed * maxtime)
                pos_s = self.position
                (pos_s[1] + 1.0)
                pos_d = self.target.position
                (pos_d[1] + 1.0)
                vec_s = MType.Vector3(*pos_s)
                vec_d = MType.Vector3(*pos_d)
                direction = (vec_d - vec_s)
                direction.length = 1.0
                tgt_distance = formula.distance(pos_s, pos_d)
                bodyRadius_t = getattr(self.target, 'bodyRadius', 0)
                distance_g = max(0, (((tgt_distance - bodyRadius_t) - distance) - self.bodyRadius))
                distance_g = min(distance_m, distance_g)
                GlobalData.CHASE_EFFECT_ARGS = distance_g

    def testObstacle(self):
        if (not self.target):
            return True
        if (not self.model.isValid()):
            return
        if self.inOfflineSpace():
            return True
        if (formula.distanceCube(self.position, self.target.position) < 0.01):
            return True
        space = MEngine.GetGameplay().Scenario.ActiveWorld.PhysicsSpace
        sweepShape = MObject.CreateObject('PhysicsShapeWrapper')
        sweepShape.SetShapeToSphereImmediately(0.1)
        transform = self.model.model.Transform
        pos1 = transform.translation
        pos1.y += 1.5
        pos2 = self.target.model.model.Transform.translation
        pos2.y += 1.5
        transform.translation = pos1
        if EngineVersionCheck.engineIs400278():
            transform = self.orthogonalizeTransform(transform)
            try:
                collideResults = space.AllSweep(sweepShape, transform, pos2, cconst.PHYSICS_OBSTACLE_QUERY)
            except:
                return True
        else:
            collideResults = space.AllSweep(sweepShape, transform, pos2, cconst.PHYSICS_OBSTACLE_QUERY)
        preferLayers = (cconst.PHYSICS_COMMON_OBSTACLE, cconst.PHYSICS_GLASSWALL)
        collideResults = set([r.Body.Parent for r in collideResults if (r.Body.CollisionFilterInfo in preferLayers)])
        collideResults.discard(self.model.model)
        collideResults.discard(self.target.model.model)
        return (not collideResults)

    def orthogonalizeTransform(self, transform):
        for i in xrange(3):
            a = (getattr(transform, ('m%d%d' % (i, j))) for j in xrange(3))
            v = MType.Vector3(*a)
            for j in xrange(3):
                setattr(transform, ('m%d%d' % (i, j)), (getattr(transform, ('m%d%d' % (i, j)), 0) / v.length))
        return transform

    def doConfirmTarget(self, skill, seltgts, restricttgts):
        state = cCombatUnit.doConfirmTarget.im_func(self, skill, seltgts, restricttgts)
        if (skill and skill.needTarget() and self.target):
            if (not self.testObstacle()):
                return 29
        return state

    def updateShowSkillRange(self, skill):
        if getattr(GlobalData, 'ShowSkillRange', 0):
            isInRange = True
            if skill.needTarget():
                target = getattr(self, 'target', None)
                if ((target is None) or (not self._checkRangeForSkill(target.position, skill, rangeonly=True, bodyRadius=getattr(self.target, 'bodyRadius', 0)))):
                    isInRange = False
            if ((not isInRange) or getattr(self.model, 'ssrInfo', None)):
                print '[SKILL DEBUG] doAttack', isInRange
                self.model.showSkillRange(skill.getRange(), isInRange)

    def actionBeforeUseSkill(self, skillid, seltgts, choose_pos, restricttgts):
        if self.invisible:
            skill_avl = True
            for buff in self.buffs.itervalues():
                if (not buff.getInVisible()):
                    continue
                if (skillid not in buff.getKeepInvisibleSkills()):
                    skill_avl = False
                    break
            if (not skill_avl):
                if (not getattr(self, 'attack_show_model', 0)):
                    self.attack_show_model = 1
                    self.wait_show_model_info = (skillid, seltgts, choose_pos, restricttgts)
                    self.updateVisibleEntity(self.id)
                    return 39
                elif (self.attack_show_model == 1):
                    self.wait_show_model_info = (skillid, seltgts, choose_pos, restricttgts)
                    return 39
                elif (self.attack_show_model == 2):
                    self.attack_show_model = 3
                    self.wait_show_model_info = None
        return 1

    def actionOnWaitModelReady(self):
        if (getattr(self, 'attack_show_model', 0) == 1):
            self.attack_show_model = 2
            self.doAttack(*self.wait_show_model_info)
            return
        slotid = getattr(self, 'wait_charge_slot', 0)
        if (not slotid):
            return
        slot = None
        if (0 <= slotid < self.skillmgr.slots):
            slot = self.skillmgr.slots[slotid]
        if (slot and (slot.time > 0)):
            self.OnStartCharing(getattr(self, 'wait_charge_slot', 0))
            self.wait_charge_slot = 0

    def doAttack(self, skillid, seltgts=None, choose_pos=None, restricttgts=None):
        if (self.isInSurvivalBattle() and self.model_shapeshift):
            self.popNotificationMsg('\xe5\x8f\x98\xe8\xba\xab\xe7\x8a\xb6\xe6\x80\x81\xe4\xb8\x8b\xe6\x97\xa0\xe6\xb3\x95\xe4\xbd\xbf\xe7\x94\xa8\xe6\x8a\x80\xe8\x83\xbd')
            return
        if (self.isInSurvivalBattle() and (not self.isSurvivalSkillsValid(skillid)) and (skillid not in SurvivalBattleConst.ITEM_SKILL_LIST)):
            self.popNotificationMsg('\xe8\xaf\xb7\xe8\xa3\x85\xe5\xa4\x87\xe6\x9c\x89\xe6\x95\x88\xe6\xad\xa6\xe5\x99\xa8')
            return
        if (self.isInSurvivalBattle() and (not self.canUsingSurvivalSkill(skillid)) and (skillid not in SurvivalBattleConst.ITEM_SKILL_LIST)):
            self.popNotificationMsg(('\xe4\xb8\x8a\xe4\xb8\x80\xe6\x8a\x8a\xe6\xad\xa6\xe5\x99\xa8\xe4\xbb\x8d\xe6\x9c\x89\xe6\x8a\x80\xe8\x83\xbdCD\xe4\xb8\xad\xef\xbc\x8c\xe9\x9c\x80\xe8\xa6\x81\xe7\xad\x89\xe5\xbe\x85%d\xe7\xa7\x92\xe6\x89\x8d\xe8\x83\xbd\xe5\x86\x8d\xe6\xac\xa1\xe9\x87\x8a\xe6\x94\xbe\xe6\x8a\x80\xe8\x83\xbd' % self.maxSkillCD))
            return
        if (skillid != 609):
            self.isInHideSkillAttack = False
        else:
            self.isInHideSkillAttack = True
        (self.isRiding and self.exitRiding())
        if (self.isCharging() and (skillid == self.getDodgeSkillid())):
            self.interruptCharging()
        if (not self.stateIM.checkInstruction(SICD.USESKILL)):
            return 0
        self.skillstate.CheckSkillUsedSuccess()
        self.lastAttack = utils.getNow()
        self.clientInput()
        skill = self.GetSkill(skillid)
        if (skill is None):
            return 2
        self.updateShowSkillRange(skill)
        if self.shouldUseTeamTarget(skill, seltgts):
            seltgts = ([self.teamTarget.id] if (self.teamTarget and (not self.teamTarget.is_destroyed())) else None)
        t = cCombatUnit.doAttack.im_func(self, skillid, seltgts, choose_pos, restricttgts)
        if (t == 22):
            return self.doAttack(self.substituteSkillid, seltgts, choose_pos)
        elif (t == 5):
            if (not self.target):
                return 8
            real_distance = (formula.distance(self.position, self.target.position) - getattr(self.target, 'bodyRadius', 0))
            general_attack_skill = school_data.data.get(self.school, {}).get('GeneralAttack', 0)
            sprint_distance = school_data.data.get(self.school, {}).get('ASprtDistance', 0)
            sprint_cd = school_data.data.get(self.school, {}).get('ASprtCooldown', 0)
            if ((general_attack_skill == skillid) and sprint_distance and ((utils.getNow() - self.lastSkillSprt) >= sprint_cd)):
                if (real_distance <= sprint_distance):
                    t = 10
                    yaw = (MType.Vector3(*self.target.position) - MType.Vector3(*self.position)).yaw
                    real_distance -= 2.0
                    self.sprintTarget(real_distance, yaw, (lambda : self.doAttack(skillid)))
                else:
                    approachdist = max(0, (sprint_distance - 0.5))
                    self.approachTarget(self.target, approachdist, (lambda : self.doAttack(skillid)))
            else:
                srange = skill.getRange()
                arange = (skill.getAssistantRange() if ((skill.getAssistantType() in (1,)) and len(skill.getAssistantGraph())) else 0)
                approachdist = ((max(srange, arange) + self.target.bodyRadius) - 0.5)
                self.approachTarget(self.target, approachdist, (lambda : self.doAttack(skillid)))
        elif skill.markPosition:
            self.markPosition = self.position
        self.OnJoyStickSelectEnd()
        if (self.isInSurvivalBattle() and (t == 1)):
            self.server.decSurvivalEquipDurationBySkill()
        return t

    @rpc_method(CLIENT_STUB, Dict())
    def onAttackResult(self, result):
        if self.server_first:
            return
        cCombatUnit.onAttackResult.im_func(self, result)

    @rpc_method(CLIENT_STUB, EntityID(), Dict())
    def SendAttackResultToClient(self, entityid, result):
        entity = EntityManager.getentity(entityid)
        if (not entity):
            return
        entity.onAttackResult(result)

    def onAttackResultFix(self, result):
        result['fixed'] = True
        cCombatUnit.onAttackResult.im_func(self, result)

    @property
    def navigationflag(self):
        return cCombatUnit.navigationflag.fget(self)

    @navigationflag.setter
    def navigationflag(self, val):
        if (self.navigationflag == val):
            return
        import MPhysics
        self.model.setCharctrlProp('SimLevel', MPhysics.ECCTSimLevel.Highest)
        cCombatUnit.navigationflag.fset(self, val)

    def walk(self, dest, arrived=None, radius=0.0, showMsg=True, forbid3D=False):
        print 'PlayerAvatar walk', dest
        if getattr(self, 'skillPosIndicator', None):
            return False
        if (not self.canMove()):
            print 'PlayerAvatar walk cannot move', dest
            return False
        if (not self.space):
            print 'PlayerAvatar walk no space', dest
            return False
        obstacleRadius = getattr(self.model.navigator, 'ObstacleRadius', 0.5)
        if (not self.space.isInWalkableArea(dest, radius=obstacleRadius)):
            self.popNotificationMsg('\xe7\x9b\xae\xe6\xa0\x87\xe5\x9c\xb0\xe7\x82\xb9\xe4\xb8\x8d\xe5\x8f\xaf\xe8\x87\xaa\xe5\x8a\xa8\xe5\xaf\xbb\xe8\xb7\xaf')
            print 'PlayerAvatar not walkable', dest
            return
        if (not self.model.canMoveTo(dest)):
            self.popNotificationMsg('\xe5\xaf\xbb\xe8\xb7\xaf\xe5\xa4\xb1\xe8\xb4\xa5\xef\xbc\x8c\xe8\xaf\xb7\xe5\xb0\x9d\xe8\xaf\x95\xe7\xa7\xbb\xe5\x8a\xa8\xe5\x88\xb0\xe4\xb8\xbb\xe5\xb9\xb2\xe9\x81\x93')
            print 'PlayerAvatar cannot move to', dest
            return
        self.walk_on_skill_end = None
        if self.stateIM.applyInstruction(SICD.NAVIGATION):
            (showMsg and NavigationMessage().hide(False))
            walk_entity = self.getWalkEntity()

            def arrivedCallback():
                self.navigationflag = False
                walk_entity.hold()
                if arrived:
                    arrived()
            if ((not self.isCombating) and (walk_entity == self)):
                dist = formula.distance2D(self.position, dest)
                if ((not forbid3D) and (dist > 30) and self.stateIM.applyInstruction(SICD._3DNAVIGATE)):
                    return self.start3DNavigate(dest, arrivedCallback, radius)
                elif (dist > 10):
                    return self.walkWithHorse(functools.partial(self._walkAfterRide, dest, arrivedCallback, radius))
                else:
                    self.navigationflag = True
                    return cCombatUnit.walk.im_func(self, dest, arrivedCallback, radius)
            else:
                self.navigationflag = True
                return cCombatUnit.walk.im_func(walk_entity, dest, arrivedCallback, radius)
        else:
            print 'PlayerAvatar walk SCID failed', dest
        if self.stateIM.CheckState(SICD.S_USESKILL):
            self.walk_on_skill_end = (dest, arrived, radius)
        return False

    def _walkAfterRide(self, dest, arrived, radius):
        if self.stateIM.applyInstruction(SICD.NAVIGATION):
            self.navigationflag = True
            cCombatUnit.walk.im_func(self, dest, arrived, radius)

    def getWalkEntity(self):
        if (getattr(self, 'd_ride_info', None) and (self.d_ride_info[1] == 2) and (self.d_ride_info[0] == getattr(self, 'combatPokemonId', None))):
            return self.getCombatPokemon()
        return self

    def hold(self):
        walk_entity = self.getWalkEntity()
        cCombatUnit.hold.im_func(walk_entity)
        self.navigationflag = False
        ((not NavigationMessage.isHide()) and NavigationMessage().hide(True))

    def checkCommonCD(self, skill):
        lastSkill = self.GetSkillCCD()[0]
        if ((not lastSkill) or (self.skills[lastSkill].comboSucc == skill.id)):
            return True
        elif (time.time() < self.GetSkillCCD()[1]):
            return False
        return True

    @rpc_method(CLIENT_STUB, Dict(), Tuple())
    def fixAnticipatedSkill(self, result, newRandomState):
        self.syncCombatRandomer.state = newRandomState
        self.onAttackResultFix(result)

    def doAttackResultCalc(self, targets, skillid, skilllevel, misc):
        self.randomer = self.syncCombatRandomer
        result = self.calcAttackResult(targets, skillid, skilllevel, misc)
        self.randomer = random
        self.onAttackResult(result)
        targetids = [t.id for t in targets]
        self.server.verifyAnticipatedSkill(targetids, result, misc, self.syncCombatRandomer.state)
        skill = self.GetSkill(skillid, skilllevel)
        if (not skill):
            return
        skillType = skill.getType()
        if ((skillType != 3) and hasattr(self, '_targetid') and (self._targetid in targetids)):
            target = self.target
            if (target and (decide(self, target) == 1)):
                self.lastAttackTarget = self._targetid
        shakeStr = None
        blurStr = None
        shakeStr = skill_data.data.get((skill.id, skill.level), {}).get('cameraShake', None)
        if (shakeStr and (GlobalData.p == self)):
            scues = shakeStr.split(',')
            for scue in scues:
                delay = float(scue[:scue.find(':')])
                args = scue[(scue.find(':') + 1):]
                args = args.split(':')
                self.add_timer(delay, utils.Functor(GlobalData.camera.cueShake, args))
        blurStr = skill_data.data.get((skill.id, skill.level), {}).get('cameraBlur', None)
        if (blurStr and (GlobalData.p == self)):
            bcues = blurStr.split(',')
            for bcue in bcues:
                delay = float(bcue[:bcue.find(':')])
                args = bcue[(bcue.find(':') + 1):]
                args = args.split(':')
                self.add_timer(delay, utils.Functor(GlobalData.camera.cueBlur, args))

    def singleCalcSkillResult(self, entityid, skillid, skilllevel):
        skill = self.GetSkill(skillid, skilllevel)
        if (skill is None):
            return
        targetids = [entityid]
        misc = self.getSkillMisc(skillid, skilllevel, targetids)
        targets = []
        for tid in targetids:
            target = self.space.getEntityByID(tid)
            if (target is None):
                continue
            targets.append(target)
        self.doAttackResultCalc(targets, skillid, skilllevel, misc)

    def ComboAllowed(self, skillid):
        self.skillmgr.ComboAllowedM(skillid)
        if getattr(self, 'gernal_attack_holding', 0):
            s = self.skillmgr.getSlotBySkillid(skillid)
            if (s and (s.slotid == 0)):
                skill = self.GetSkill(skillid)
                cskillid = skill.comboSucc
                if (cskillid and (cskillid != skillid)):
                    self.AutoUseSkill(cskillid)
                    return
        cCombatUnit.ComboAllowed.im_func(self, skillid)

    def ComboBaned(self, skillid):
        self.skillmgr.ComboBanedM(skillid)

    def ComboFailed(self, skillid):
        self.skillmgr.ComboFailedM(skillid)

    def trigger_walk(self):
        if (not getattr(self, 'walk_on_skill_end', None)):
            return
        self.walk(*self.walk_on_skill_end)
        self.walk_on_skill_end = None

    def SkillProgress(self, skillid):
        self.skillmgr.SkillProgressM(skillid)

    def SkillPost(self, skillid, calcver):
        if ((getattr(self, 'skillCalcVer', 0) != calcver) and (calcver != (-1))):
            return
        self.skillmgr.SkillPostM(skillid)
        self.handleSequenceSkills()
        self.think()

    def SkillMovePost(self, skillid, calcver):
        if ((getattr(self, 'skillCalcVer', 0) != calcver) and (calcver != (-1))):
            return
        self.skillmgr.SkillMovePostM(skillid)
        if (getattr(self, 'shakeInfo', None) and (not self.skillmgr.skillNext[0])):
            self.model.gotoLocomotion(0.3)
        self.trigger_walk()

    def SkillMisc(self, skill, targets):
        if (len(targets) < skill.getMinAffectNum()):
            return False
        totaltime = skill.getCoolDown()
        cdDecrease = ((self.buffs.sumAttr('cd_decrease') + self.getPskillsSumbAttr('cd_decrease')) + self.getChildSkillCDRatio(skill.id))
        if (cdDecrease > 0):
            totaltime *= max(0, (1 - cdDecrease))
        if (skill.id in self.skillCooler):
            totaltime = (totaltime - self.skillCooler.select(skill.id))
        totaltime = max(1, totaltime)
        if (skill.id in self.skillCDReducer):
            for (other, dur) in self.skillCDReducer[skill.id].iteritems():
                self.reduceSkillCD(other, dur)
        self.SetSkillCD(skill.id, (time.time() + totaltime), totaltime)
        self.SetSkillCCD((skill.id, (time.time() + skill.getCCD()), skill.getCCD()))
        slot = self.skillmgr.getSlotBySkillid(skill.id)
        (slot and PlayerMain().UpdateButtonBySlotid(slot.slotid))
        return True

    def SkillUsed(self, skillid):
        self.skillmgr.SkillUsedM(skillid)
        self.tryNotifySkillToShadowPokemon(skillid)

    def SkillStart(self, skillid):
        skill = self.GetSkill(skillid)
        if (not skill):
            return
        if skill.isAutoComboBreakBySkill():
            self.wait_skill_break = True
        if skill.isAutoComboBreak():
            self.wait_move_break = True
        self.skillmgr.SkillStartM(skillid)
        self.skillSyncState.skillStart()
        cCombatUnit.SkillStart.im_func(self, skillid)
        self.effect_to_close = skill_data.data.get((skill.id, max(1, skill.level)), {}).get('effect_to_close', None)
        combo_data = skill.getComboTime()
        if (combo_data and (GlobalData.p == self)):
            AutoSkillBar().show(combo_data)

    def SkillCalc(self, skillid, calcver):
        if (getattr(self, 'skillCalcVer', 0) != calcver):
            return
        self.skillmgr.SkillCalcM(skillid)
        cCombatUnit.SkillCalc.im_func(self, skillid, calcver)

    def SkillEnd(self, skillid):
        skill = self.GetSkill(skillid)
        if (not skill):
            return
        if skill.isAutoComboBreakBySkill():
            self.wait_skill_break = False
        if skill.isAutoComboBreak():
            self.wait_move_break = False
        self.skillSyncState.skillEnd()
        cCombatUnit.SkillEnd.im_func(self, skillid)
        self.skillmgr.SkillEndM(skillid)
        skill = self.GetSkill(skillid)
        if (skill and skill.comboSucc and (skill.comboSucc != skillid)):
            (nextid, _) = self.skillstate.skillNext
            if (skill.comboSucc != nextid):
                self.ComboFailed(skillid)
        self.trigger_walk()
        PlayerMain().UpdateAllSkillIcon()
        PlayerMain().UpdateAttackBtnIcon()

    def removeAutoSkillEffect(self):
        if getattr(self, 'effect_to_close', None):
            effectids = self.effect_to_close.split(',')
            for eid in effectids:
                self.model.detachEffectEx(eid)
            self.effect_to_close = None

    def calcSkillResult(self, skillid, skilllevel, targetids, misc, calcver, attackinfo, targetinfo):
        skill = self.GetSkill(skillid)
        if ((getattr(self, 'skillCalcVer', 0) != calcver) and (not (skill and skill.isChildSkill()))):
            return
        if ((self.skillmgr.skillRunning[0] != skillid) and (not (skill and skill.isChildSkill()))):
            return
        cCombatUnit.calcSkillResult.im_func(self, skillid, skilllevel, targetids, misc, calcver, attackinfo, targetinfo)

    def checkRunningSkill(self, skillid):
        res = (not self.skillmgr.blockByRunningSkill(skillid))
        return res

    def getDodgeSkillid(self):
        return self.getCombatSkillsData().get('dodge', 0)

    def checkDodgeSkill(self, skillid):
        if (self.getDodgeSkillid() == skillid):
            return self.canDodge()
        return True

    def isSkillReady(self, skill):
        res = 1
        if (not self.stateIM.checkInstruction(SICD.USESKILL)):
            res = 0
        elif getattr(self, 'sprintgid', 0):
            res = 9
        elif (skill.level == 0):
            res = 0
        elif (not skill.enable):
            res = 35
        elif self.skillmgr.blockBySlot(skill.id):
            res = 9
        elif (getattr(self, 'skillPosIndicator', None) and (skill.id != self.jsSelSkillid) and (not skill.JoystickYaw())):
            res = 0
        elif (not self.checkDodgeSkill(skill.id)):
            res = 0
        elif (not self.checkOceanPowerSkill(skill.id, showMsg=True)):
            res = 0
        elif (EngineVersionCheck.checkCanLoadGraphDeffered() and (getattr(self, 'currActiveNode', '') == ('skill_%d' % skill.getSkillProto()))):
            return 0
        else:
            res = cCombatUnit.isSkillReady.im_func(self, skill)
        if (res != 1):
            return res
        return res

    def onSkillForbid(self):
        PlayerMain().UpdateAllSkillIcon()

    def onMainShowBuff(self, buffid):
        PlayerMain().UpdateMainShowBuff(buffid)

    def canUseSkill(self, combatunit, skill):
        if (self.isSkillReady(skill) != 1):
            res = False
        elif (not self.skillmgr.canUseSkill(skill.id)):
            res = False
        else:
            res = cCombatUnit.canUseSkill.im_func(self, combatunit, skill)
        return res

    def setPanelSkills(self, panelSkills):
        if (self.getCurrentPanelSkills() != panelSkills):
            seconds = panelSkills.getSkillIds()[4:]
            if (seconds.count(0) == len(seconds)):
                self.setSkillsSwitch()
            self.server.updatePanelSkills(panelSkills)

    def SaveWeaponSkills(self, selectedskills):
        if (self.selectESkills != selectedskills):
            self.server.updateESkills(selectedskills)

    def setSkillsSwitch(self, select=0):
        panelSkills = self.getCurrentPanelSkills()
        if (not panelSkills.getSkillIds()):
            return
        panelSkills = list((panelSkills[select] if (select < len(panelSkills)) else []))
        if (panelSkills.count(0) == len(panelSkills)):
            select = 0
        if (select != self.skillSwitch):
            self.skillSwitch = (select % max(1, len(panelSkills)))
            self.skillmgr.updateSkills()

    def getCurrentPanelSkillPage(self):
        panelSkills = self.getCurrentPanelSkills()
        if (not panelSkills.getSkillIds()):
            return 0
        res = 0
        for i in xrange(len(panelSkills)):
            skills = list(panelSkills[i])
            if (skills.count(0) != len(skills)):
                res += 1
        return min(res, 4)

    def _on_set_panelSkills(self, old):
        self.skillmgr.updateSkills(reset=False)

    def _on_set_panelSkills2(self, old):
        self.skillmgr.updateSkills()

    def _on_set_selectESkills(self, old):
        self.skillmgr.updateSkills()

    def onEnterCombat(self):
        cCombatUnit.onEnterCombat.im_func(self)
        (GlobalData.camera and GlobalData.camera.onCombatEngaging())
        PlayerMain().UpdateAllSkillIcon()
        self.checkIsInHomesteadArea()

    def onLeaveCombat(self):
        cCombatUnit.onLeaveCombat.im_func(self)
        self.lastAttackTarget = ''
        (GlobalData.camera and GlobalData.camera.onCombatOver())
        PlayerMain().UpdateAllSkillIcon()
        self.checkIsInHomesteadArea()

    def tryLeaveCombat(self):
        if (not getattr(self, 'leaveCombatStamp', 0)):
            self.leaveCombatStamp = 0
        self.leaveCombatStamp += 1
        self.add_timer(5, functools.partial(self._doTryLeaveCombat, self.leaveCombatStamp))

    def _doTryLeaveCombat(self, stamp):
        if (self.leaveCombatStamp != stamp):
            return
        if (not self.hates):
            self.leaveCombat()

    @rpc_method(CLIENT_STUB, Int())
    def operateAI(self, operate):
        if (operate == 1):
            self.AIResume()
        else:
            self.AISuspend()

    @property
    def sprintCD(self):
        return school_data.data.get(self.school, {}).get('ASprtCooldown', 0)

    @property
    def sprintWait(self):
        return ((self.lastSkillSprt + school_data.data.get(self.school, {}).get('ASprtCooldown', 0)) - utils.getNow())

    def _on_set_hp(self, old, attacker=None):
        if (self.hp != old):
            self.UpdateHP()
        AvatarMember._on_set_hp.im_func(self, old, attacker)

    def _on_set_vice_hp(self, old, attacker=None):
        if (self.vice_hp != old):
            self.UpdateVHP()
        cCombatUnit._on_set_vice_hp.im_func(self, old, attacker)

    def _on_set_mp(self, old):
        if (self.mp != old):
            self.UpdateMP()
        cCombatUnit._on_set_mp.im_func(self, old)

    def _on_set_sp(self, old):
        pass

    def _on_set_vice_maxhp(self, old):
        if (self.vice_maxhp != old):
            self.UpdateVHP()

    def _on_set_maxhp(self, old):
        if (self.maxhp != old):
            self.UpdateHP()

    def _on_set_maxmp(self, old):
        if (self.maxmp != old):
            self.UpdateMP()

    def _on_set_assign_credits(self, old):
        if (self.assign_credits != old):
            self.OnAssignCreditsChanged()

    def _on_set_x_assign_credits(self, value):
        if (self.x_assign_credits != value):
            if ExtraAssignCredit.isInited():
                ExtraAssignCredit().updateUI()

    def _on_set_primary_attr(self, old):
        if (self.primary_attr != old):
            self.OnPrimaryAttrChanged()

    def skillAll(self, skilllevel):
        self.server.skillAll(skilllevel)

    def CheckTgtlockFirst(self, tgtlock, skill):
        if ((skill.getType() == 3) and (getattr(tgtlock, 'id', 0) in self.teammember)):
            return True
        return skill.getAffectTgtlockFirst()

    def setOriginPanelSkills(self, panelSkills):
        if (panelSkills != self.panelSkills):
            self.server.setOriginPanelSkills(panelSkills)

    def DoChangeSchool(self, contents):
        (school, body) = contents.get('select_info', None)
        splsklidx = sorted(list(contents.get('splskl_idx', None)))
        special = SISD.data.get(school, {}).get('special', 0)
        special = SSD.data.get(special, {}).get('Skillid', 0)
        splskillids = list(SSPD.data.get(school, {}).get('skills', ()))
        ((special in splskillids) and splskillids.remove(special))
        splskills = [special]
        for idx in splsklidx:
            splskills.append(splskillids[idx])
        self.server.DoChangeSchool(school, body, splskills)

    def removeHateTargetThroughAvatar(self, srcid, tgtid):
        if ((not self.space) or self.space.is_destroyed()):
            return
        if (srcid == self.id):
            self.server.removeHateTarget(tgtid)
        else:
            self.server.removeHateTargetThroughAvatar(srcid, tgtid)

    @rpc_method(CLIENT_STUB, Int())
    def resetOneSkillCD(self, skillid):
        self.ClearSkillCD(skillid)
        PlayerMain().UpdateButtonBySkillid(skillid)
