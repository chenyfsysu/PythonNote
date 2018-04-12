# -*- coding:utf-8 -*-

import time
import functools
import random
import cconst
import bconst
import const
import utils
import GlobalData
import DesignFlags
import re
import txmco
import InputChecker
import copy
import formula
import txm
import MEngine
import MRender
import MObject
import MPlatform
import MConfig
import MType
import MHelper
import math
import EngineVersionCheck
import config
import DataHelper
import sys
import os
import ReturnConst
import GoldMallCommon
import MAccount
import base64
import hashlib
import urllib
import json
import MChecker
import datetime
import operator
import bisect
import MCharacter
from common.classutils import Property, CustomListType
from common.Crontab import Crontab
from common.RpcMethodArgs import Int
from common.rpcdecorator import CLIENT_STUB, rpc_method, SERVER_ONLY
from GUI.ActivityMain import ActivityMain, AutoCompleteWidget
from GUI.ArenaPlayOffMain import ArenaPlayOffMain
from GUI.CrossWarWidget import CanvassDialog, CrossWarWidget
from GUI.playermain.PlayerMain import PlayerMain
from GUI.ScreenPopmsg import PopmsgPool
from GUI.SupplyWidget import SupplyWidget
from GUI.BountyTaskWidget import BountyTaskWidget
from GUI.SystemSetting import SocialShare
from GUI.TxmMessageBox import MessageBox
from GUI.CJCatchGold import CJCatchGold
from GUI.CJEvolution import CJEvolution
from GUI.CJSupperzzle import CJSupperzzleMain
from GUI.activity.PoetryCompetitionPanel import PoetryCompetitionWidget
from GUI.AdventureHouseShare import AdventureHouseShare
from GUI.MidAutumnWidget import MidAutumnWidget
from GUI.FurnitureShare import FurnitureShare
from LocalData import LocalData
from iActivity import iActivity, ActivityConst, ActivityHelper
from iActivity import ActiveRewardStatus, ActivitiesStatusInfo
from SpaceInquiry import SpaceLevelInquiry, SpaceInquiry
from GUI.gameitems.ItemMeteor import ItemMeteor
from GUI.RankListMain import RankListMain
from txmdecorators import delay_call, limit_call
from data import activity_data
from data import active_reward_data
from data import state_instruction_constrain_data as SICD
from data import clan_secret_data
from iDumpling import DumplingHelper
from common.classutils import CustomMapType, Property, CustomListType
from common.RpcMethodArgs import Dict, Int
from utils import enum
from iEventNotifier import CallbackHost
from operator import itemgetter
from data import achievement_enhance_data as AED
from data import achievement_enhance_level_data as AELD
from data import achievement_enhance_upgrade_lib_data as AEULD
from data import achievement_enhance_rebuild_lib_data as AERLD
from common.RpcMethodArgs import EntityID, Int, Tuple, List, Str
from iAwards import iAwards, iAwardPoint
from GUI.LotteryMachine import LotteryMachine
from GUI.EvilOgreWidget import EvilOgreWidget
from GUI.SkillChargeBar import SkillChargeBar
from TreasureBox import TreasureError
from iTreasureBox import TreasureConst
from iMsg import ChannelType
from utils import Cache
from data import credit_data
from data import item_data
from HyperLinkCreator import HyperLinkCreator
from common.IdManager import IdManager
from iMsg import MsgManager, MsgField, WarningMessageMap, ChannelType
from iMsg import MONEY_CONSUMPTION_IN_WORLD
from iFriends import FriendConst
from cFriends import QueryDetailsCo
from ChatCache import ChatCache
from GUI.ExaminationMain import ExaminationMain
from GUI.ChatMain import ChatMain
from GUI.WorldChannelTip import WorldChannelTip
from GUI.ExchangeMain import ExchangeMain
from GUI.WorldOrder import WorldOrder
from data import team_push_chat_words_data as TPCWD
from data import team_push_match_data as TPMD
from data import team_push_const_data as TMCD
from data import chat_match_data
from functools import partial
from common.RpcMethodArgs import Bool, Dict, EntityID, Int, List, Str, Tuple, Float
from ClanSkills import ClanSkills, ClanEnemies
from clan import ClanConst, ClanError, ClanStation
from GUI.ClanRiddleWidget import ClanRiddleWidget
from GUI.ClanWidget import ClanApplicantPopup, ClanFightNotifyDialog, ClanFightResultDialog, ClanFightStatus
from GUI.ClanWidget import RedEnvelopeNotifier, ClanRenameDialog, ClanWidget
from GUI.clanwar.ClanWarStatus import ClanWarStatus
from GUI.CreditShopMain import CreditShopMain
from GUI.MainMenuBar import MainMenuBar
from GUI.ExaminationMain import ExamReplyWidget
from GUI.LGGSWidget import LGGSStatus
from GUI.gameitems.Bag import BagMain
from GUI.ClanRaiseFlagWidget import ClanRaiseFlagMain, ClanRaiseFlagWidget, ClanRaiseFlagCountDown
from iNpc import NpcConst
from LevelAuthorization import LevelAuthorization
from utils import OrderedList, Functor, Dispatcher
from GameItemConst import GAMEITEM_CONST
from data import change_scene_data as csd
from data import clan_fight_data
from data import clan_war_tower_data
from data import clan_gift_envelope_data
from data import clan_tree_data
from data import clan_raise_flag_data
from common.EntityManager import EntityManager
from mobilelog.LogManager import LogManager
from GUI.AwakePanel import AwakeSkillResult
from iAwake import AwakeConst
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
from GUI.AutoSkillPanel import AutoSkillBar
from GUI.NoticeMessage import NavigationMessage
from GUI.gameitems.ExtraAssignCredit import ExtraAssignCredit
from avatarmembers.impHideAndSeek import HsConst
from iRelation import decide
from iCombatUnit import CombatHelper
from ModelSeqLoader import ModelSeqLoader
from iSurvivalBattle import SurvivalBattleConst
from GUI.NpcShop import NpcShop
from GUI.mall.Mall import MallMain
from GUI.mall.QuickSell import QuickMoneyMallSell
from GUI.EquipmentsWorkshop.EquipmentsWorkshop import EquipmentsWorkshop
from GUI.HomeBuyWidget import HomeBuyWidget
from GUI.marriage.Engage import EngageMain
from GUI.marriage.VIPInvitation import VIPInvitation
from GUI.ride.RideSoulStarRegen import RideSoulStarRegen
from GUI.ride.RideSoulStarUpgrade import RideSoulStarUpgrade
from GUI.LGGSWidget import BossDescModifier
from GUI.WxpLottery import WxpLottery
from GUI.pokemon.SecondaryWindows import MergeAddExpWindow
from CurrencyCommon import CurrencyCommon
from GUI.child.BabyWidget import BabyWidget
from GUI.child.JuvenileWidget import JuvenileWidget
from GUI.ComradeWidget import ComradeMain
from GUI.AuthWidget import AuthWidget
from GUI.AppearanceWidget import AppearanceWidget
from GUI.RacingPanel import TimeWidget
from GUI.playermain.SnapShotWidget import SnapShotPanel
from GUI.FreeColorBase import FreeColorBase, FreeColorRecordItem
from iDress import Wardrobe, PokemonWardrobe, DressPart
from iDress import DressColor, DressFreeColor
from iDress import FreeColor, FreeColorPart, FreeColorHelper, FreeColorHistory, FreeColorError, FreeColorErrorMsg
from data import dressup_data
from data import expression_action_data as EAD
from data import dress_effect_data
from Model import FlyAction
from data import fixedfly_data
from GUI.greenhand.GuidelineEvent import GuidelineEvent
from GUI.LevelUpGrade import LevelUpGrade as LU
from data import exp_data as ed
from data import hardcode_resource_data
from GUI.SigninWidget import MergeFriendAddDialog, SigninWidget
from Space import Space, SpaceLoader
from UI import UIManager
from cQteNode import QteEvent
from JoystickMode import JSMode, JoystickGroundMode, JoystickAirMode
from GUI.Loading import LoadingDispacher
from GUI.playermain.GSkillButton import QINGGONG_BUTTON_ID
from UI.UIConst import BrightType
from GUI.ride.RideWidget import RideWidget
from iRide import Carriers, CarriersDye, RideOtherInfo
from iRideSoul import RIDESOUL_CONST
from Space import LoaderMonitor
from GUI.survivalbattle.CrossTarget import CrossTarget
from data import riding_data
from data import riding_graph_data
from data import space_level_data
from data import double_ride_hold_point_data as HRHD
from iRubbing import Rubbings
from data import rubbing_const_data
from StateInstructionManager import StateConstrainComponent
from SoloCommon import SoloCommon
from GUI.Solo import NotifyAskSoloMsg
from cEnemy import cEnemies
from iEnemy import EnemyConst
from GUI import ScreenPopmsg
from GUI.ArenaRun import ArenaRun as AR
from GUI.ArenaRun import ArenaDetail as AD
from GUI.ArenaConfirm import ArenaConfirm as AC
from GUI.ArenaConfirm import ArenaWaiting as AW
from iArena import iArenaSeasonRecords, iArenaInfo, ArenaConst, iArenaAnimInfo
from cArena import cArenaTeamInfo, cArenaResultList
from GUI.ArenaInvite import ArenaInvite as AI
from data import arena_dan_data as ADD
from GUI.ArenaMain import ArenaMain as AM
from GUI.ArenaConfirm import ArenaTmConfirm as ATM
from GUI.playermain.PlayerMain import PlayerMain as PM
from GUI.ArenaKill import ArenaKill as AK
from GUI.ArenaWatch import ArenaWatch
from data import arena_season_data as ASeasonD
from SpaceInquiry import SpaceType, SpaceInquiry
from data import qinggong_cd_data
from data import qinggong_level_data
from iReturnRoad import ReturnRoadAwards
from utils import BitList
from GUI.GeneralUI import CutShare
from GUI.SigninWidget import ReturnFriendAddDialog, SigninWidget
from GUI.ReturnWidget import ReturnWindow, ReturnController
from data import return_road_award_data
from data import return_score_award_data
from GUI.BattleWaiting import BattleWaiting as BW
from GUI.BattleStatics import BattleStatics as BS
from iBattle import BattleConst, BattleDetail
from GUI.BattleConfirm import BattleConfirm as BC
from GUI.BattleRun import BattleRun as BR
from GUI.BattleRun import BattleJazz
from GUI.BattleResult import BattleResult
from GUI.BattleExtraAward import BattleExtraAward
from GUI.ttbattle.ttRankListMain import TTRankListMain
from GUI.ttbattle.ttAwards import TTAwards
from GUI.ttbattle.ttMain import TTMain
from GUI.BattleConfirm import BattleNewbieConfirm
from iBattle import BattleInfo, BattleStartTime, MapEntities, BattleAwards, BattleResults, BattleExtraAwards, TTBattleSeasonRecords, TTBattleRecentRecords
from cBattle import cBattleCampScore
from iBamboo import BambooConst
from iBattle import BattleNewbieConst
from iDreamSource import DreamSourceConst
from iBattle import TTPerformanceRecord
from data import ttbattle_weekaward_data
from data import ttbattle_seasonaward_data
from GUI.DetailedMap import DetailedMap, BattleMap
from GUI.PVPMain import PVPMain
from data import sphere_marker_data as SMD
from GUI.NoticeMessage import OperationMessage
from iLotus import LotusComponent, LotusCollectError, LotusInquiry
from data import ways_to_obtain_item_data as WTOID
from GUI.gameitems.ResourceTips import WayType
from MallConst import MALL_ITEM_CONST
from data import pay_data as PD
from data import rebate_data as RD
from GUI.MonthCard import MonthCard, FreeFlowMonthCard
from DesktopHelper import DesktopHelper, isGas3LoginChannel
from GUI.RelatedPhone import RelatedPhoneWidget, ConfirmPhoneWidget, CheckPhoneWidget, ChangePhoneWidget
from mobilerpc import SimpleHttpClient, HttpBase
from iAvatarSpaceTag import iAvatarSpaceTag
from iTitle import iTitle
from GUI.AvatarTitles import AvatarTitles
from GUI.achievement.AchieveTips import AchieveTips
from GUI.HomeMainWidget import HomeMainWidget
from GUI.HomeTreeWidget import HomeTreeWidget
from GUI.HomeAntiqueWidget import HomeAntiqueWidget
from GUI.HomeTreeRankWidget import HomeTreeRankWidget
from utils import CallUntil
from iHome import HomeError, HomeConst, HomeAntiqueMap, HomeInfo, AvatarHomeComponent, HomeTreeInfo, HomeTreeInfoMap
from data import home_data
from data import antique_data
from data import tree_irrigate_data
from data import level_authorization_data as LAD
from iArenaPlayOff import PlayOffTeam, ArenaPlayOffJoiners
from iArenaCross import CombatGroups
from GUI.GPlayOffTeams import GPlayOffTeams
from GUI.GPlayOffApply import GPlayOffApply
from GUI.GPlayOffAllTeams import GPlayOffAllTeams
from GUI.GCombatMap import GCombatMap
from GUI.CreatePlayOffTeam import CreatePlayOffTeam
from txmdecorators import limit_call_no_msg
from Marriage import Marriage, MarriageConst, MarriageComponent, MarriageError
from cChild import cChildren
from GUI.marriage.WeddingInvite import WeddingInvite
from GUI.marriage.Certification import Certification
from GUI.marriage.WeddingProcess import WeddingProcess
from GUI.marriage.LoveInsurance import LoveInsurance
from GUI.social.Main import SocialMain
from GUI.child.DistributeWidget import DistributeWidget
from GUI.home.HomesteadMain import HomesteadSwitch
from iFish import iFish, FishConst, FishState, FishStateName, FishStatusCheck
from Input import InputEventHandler
from GUI.FishMain import FishMain, HomeBigFishWidget
from data import fish_rod_data
from data import fish_area_data
from data import home_fish_surprise_data as HFSD
from CJBattleCommon import CJBattleComponent, CJConfig, CJElfBag
from GUI.cjbattle.CJBattleMatch import CJBattleWaiting, CJWaitOtherConfirm
from utils import Functor, getNow
from data import cj_score_data
from common.classutils import _initClassWityProperty, VALID_PROPERTY_NAME, Property, CustomMapType
from iPartnerComponent import iPartnerComponent
from Partners import Formation
from cFreeFlowManager import cFreeFlowManager
from iFreeFlow import FreeFlowRecords, FreeFlowRecord, iFreeFlowConst
from GUI.MonthCard import FreeFlowMonthCard, FreeFlowApply
from iCJEvolution import CJEvolutionConst, Game2048Property, iGame2048, iCJEvolutionCurGame, iCJEvolutionRecords
from GUI.BambooRun import BambooRun
from GUI.BattleStatics import BattleStatics
from data import bamboo_args_data
from PickStarCommon import PickStarAvatarCommon, PickStarConst
from GUI.pickstar.PickStarBattleBanner import PickStarBattleBanner
from GUI.pickstar.PickStarBattleReport import PickStarBattleReport
from GUI.pickstar.PickStarMatch import PickStarMatch
from GUI.TlpWidget import TlpWindow
from iSchoolmateArena import SchoolmateArenaAvatarCommon, SchoolmateArenaError, SchoolmateArenaConst
from GUI.schoolmatearena.SchoolmateArenaWaitTime import SchoolmateArenaWaitTime, SchoolmateArenaMatchAcceptPanel
from GUI.schoolmatearena.SchoolmateArenaMain import SchoolmateArenaMain, MainMenuHandle
from GUI.schoolmatearena.SchoolmateArenaLoading import SchoolmateArenaLoading
from GUI.schoolmatearena.SchoolmateArenaTimer import SchoolmateArenaTimer
from GUI.schoolmatearena.SchoolmateArenaRankmap import SchoolmateArenaRankmap
from GUI.schoolmatearena.SchoolmateArenaRecord import SchoolmateArenaHistory, SchoolmateArenaKingHistory
from data import schoolmate_arena_data
from GUI.MarkerNpcButton import MarkerNpcButton
from iPassPower import PassPowerConst
from GUI.PassPowerWidget import PassPowerEntry, PassPowerDialog, PassPowerMain
from PassPowerCenter import PassPowerCenter
from GUI.TeamMain import TeamMain
from GUI.SurvivalBattleWidget import SurvivalBattleWaiting, SurvivalBattleConfirm, SurvivalBattleMap, FraudCardMain, FraudCardShop
from GUI.SurvivalBattleWidget import SurvivalBattleGameInfo
from GUI.SurvivalBattleWidget import RandomKillWindow, SurvivalBattleCard
from GUI.playermain.TempButtonList import TempButtonList
from GUI.ArenaKill import ArenaKill
from GUI.DungeonWarning import DungeonWarning
from iSurvivalBattle import iSurvivalBattle, SurvivalBattleError, SurvivalBattleConst
from SurvivalBattleQuery import SurvivalBattleQuery
from iSurvivalBattle import GameData, ContestRecord
from SurvivalGameItems import SurvivalGameItems
from GUI.survivalbattle.Bag import SurvivalBagMain
from GUI.survivalbattle.Bag import SurvivalTempBag
from GUI.survivalbattle.ItemTips import SurvivalEquipPopup
from SurvivalGameItem import SurvivalGameItem
from GUI.survivalbattle.HitEffect import HitEffect
from data import survival_item_type_data as SITD
from data import combatunit_data
from data import item_model_data
from data import survival_item_sfx_data as SIFD
from Dynamic import Dynamic
from PSkills import PSkillsHub
from data import survival_weapon_skill_data as SWSD
from GUI.home.FurnitureInteractWidget import FurnitureInteractWidget, FurnitureClickedHandler
from GUI.home.HomeBuildingWindow import HomeBuildingEntranceWindow, HomeBuildingWindow
from GUI.home.HomeBuildingManager import HomeBuildingManager
from GUI.home.IEntitySeqLoader import IEntitySeqLoader
from HomesteadConst import HomesteadConst
from iHomestead import HomesteadInfo, iHomesteadComponent, HomeItems, VisitRecords, OrderRecords, MakeRecords, OpenChestRecords, BuildingDataGetter, Buildings, GetGeomancyLevel, GeomancyRecords
from cHomestead import getFurnitureNavigatePos
from GUI.home.HomesteadMain import HomesteadMain, HomesteadRepertory, RepertoryMoveWidget, HomesteadBuilding, HomesteadChestWidget
from GUI.greenhand.GuidelineNavigator import GuidelineNavigator
from GUI.home.FengShuiPanel import FengShuiPanel, GeomancyDivinePanel
from txmdecorators import limit_method_args_call
from GUI.home.HomeBuildingManager import DummyModel, BuildingModel
from data import furniture_interact_data
from data import home_upgrade_data
from data import home_model_data as HMD
from data import home_geomancy_data
from data import item_building_data
from data import home_geomancy_space_data
from data import home_const_data
from data import combatproto_data
from cHomestead import HomesteadData, SingletonTickTimer
from iDinner import DinnerConst
from iHatKingBattle import HatKingBattleConst, HatKingBattleError, HatKingBattleResult
from SoundManager import SoundManager
from GUI.HatKingBattleWidget import HatKingBattleWaiting as HKBW
from GUI.HatKingBattleWidget import HatKingBattleConfirm as HKBC
from GUI.HatKingBattleWidget import HatKingBattleTips as HKBT
from GUI.HatKingBattleWidget import HatKingBattlePrepare as HKBP
from GUI.HatKingBattleWidget import HatKingBattleCombat as HKB
from iMagicParty import MpConst, MpData, MpHelper, FakeData, MagicRiddenAns
from GUI.MagicParty import MagicSelectBianshen, MagicwandPatternSelect, BianShenMain, YiRongMain
from GUI.MagicParty import MagicPartyDropRainWidget
from GUI.ChristmasCardWidget import DropRainWidget
from data import chrismas_magicwand_data
from data import mail_buildin_data
from iPhotoBoard import PhotoBoardConst, PhotoBoardError
from GUI.PhotoBoardWidget import PhotoBoardWidget
from iValentinesDay import ValentinesDayConst as VConst
from data import valentine_rose_graph_data as VRGD
from SpaceInquiry import SpaceInquiry, DungeonType
from GUI.MorningExercisePanel import MorningExercisePanel
from iMorningExercise import MorningExerciseConst as MConst
from GUI.MorningExerciseResult import MorningExerciseResult
from data import morning_exercise_const_data as MECD
from GUI.AprilFoolTrickyBox import AprilFoolTrickyBoxProducePanel
from data import april_fool_tricky_box_data as AFTBD
from Trajectory import GrenadeTrajectory
from iLanternRiddle import GrenadeConst, GrenadeQuery
from GUI.LanternRiddleWidget import GrenadeBuyWidget
from avatarmembers.impActivity import AvatarMember as impActivity_AvatarMember_2
from avatarmembers.impAward import AvatarMember as impAward_AvatarMember_3
from avatarmembers.impCombat import AvatarMember as impCombat_AvatarMember_4
from avatarmembers.impCurrency import AvatarMember as impCurrency_AvatarMember_5
from avatarmembers.impItem import AvatarMember as impItem_AvatarMember_6
from avatarmembers.impModel import AvatarMember as impModel_AvatarMember_7
from avatarmembers.impPokemon import AvatarMember as impPokemon_AvatarMember_8
from avatarmembers.impRide import AvatarMember as impRide_AvatarMember_9
from avatarmembers.impSpace import AvatarMember as impSpace_AvatarMember_10
from avatarmembers.impTeam import AvatarMember as impTeam_AvatarMember_11
from avatarmembers.impPK import AvatarMember as impPK_AvatarMember_12
from avatarmembers.impSolo import AvatarMember as impSolo_AvatarMember_13
from avatarmembers.impEnhance import AvatarMember as impEnhance_AvatarMember_14
from avatarmembers.impSphereMarker import AvatarMember as impSphereMarker_AvatarMember_15
from avatarmembers.impSpaceTag import AvatarMember as impSpaceTag_AvatarMember_16
from avatarmembers.impTitle import AvatarMember as impTitle_AvatarMember_17
from avatarmembers.impGroup import AvatarMember as impGroup_AvatarMember_18
from avatarmembers.impFish import AvatarMember as impFish_AvatarMember_19
from avatarmembers.impHideAndSeek import AvatarMember as impHideAndSeek_AvatarMember_20
from avatarmembers.impCJBattle import AvatarMember as impCJBattle_AvatarMember_21
from avatarmembers.impPartner import AvatarMember as impPartner_AvatarMember_22
from avatarmembers.impSnowBattle import AvatarMember as impSnowBattle_AvatarMember_23
from avatarmembers.impPickStar import AvatarMember as impPickStar_AvatarMember_24
from avatarmembers.impSchoolmateArena import AvatarMember as impSchoolmateArena_AvatarMember_25
from avatarmembers.impComrade import AvatarMember as impComrade_AvatarMember_26
from avatarmembers.impDinner import AvatarMember as impDinner_AvatarMember_27
EnhanceType = enum(UPGRADE=0, REBUILD=1)
CurrencyType = enum(MONEY=1, MILITARY=2, GOLD=3)
EnhanceErrorNo = enum(OTHER=(-1), SUCCESS=0, LV_WRONG=1, ACHV_POINT=2, CURRENCY=3, CREDIT=4, ITEM=5)
PROP_NAMES = ['maxhp', 'maxmp', 'str', 'dex', 'int', 'mind', 'dog', 'con', 'hit', 'pdmg', 'mdmg', 'cri', 'avoid', 'skprt', 'pdef', 'mdef', 'eff_heal', 'cri_add', 'rad0', 'cri_sub', 'raa0', 'pdmg_sub', 'mdmg_sub', 'pptr', 'mptr', 'cri_heal', 'add_heal', 'pdmg_resi', 'mdmg_resi', 'buff_resi_b', 'buff_resi_a', 'apdmg', 'amdmg', 'speed_a', 'buff_hit', 'm_hp_steal', 'p_hp_steal']
PROP_ID_DICT = {name: i for (i, name) in enumerate(PROP_NAMES)}

class cAwardPoint(iAwardPoint, ):

    def on_setattr(self, key, old, new):
        self.get_owner().updateAwardPoint()

class ClanInfo(CustomMapType, ):
    Property('no')
    Property('guid')
    Property('tag')
    Property('guidHistory')
    Listeners = {'tag': 'updateStation', 'guid': 'onClanChanged', 'guidHistory': 'updateClanNotify'}

    def on_init(self, parent):
        self.get_owner().station = ClanStation.fromTag(self.tag)

    def on_setattr(self, key, old, new):
        super(ClanInfo, self).on_setattr(key, old, new)
        listener = self.Listeners.get(key)
        (listener and getattr(self.get_owner(), listener)())

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
            elif (self.slotid == (5 + const.MAX_PANEL_SKILLS)):
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
        self.skillRunning = (0, const.SKILL_STATE_END)
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
                for idx in xrange(const.MAX_PANEL_SKILLS):
                    if (idx < len(currentPanelSkills[switch])):
                        skills.append(currentPanelSkills[switch][idx])
                    else:
                        skills.append(0)
            else:
                for idx in xrange(const.MAX_PANEL_SKILLS):
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
                for idx in xrange(const.MAX_PANEL_SKILLS):
                    if (idx < len(currentPanelSkills[switch])):
                        skills.append(currentPanelSkills[switch][idx])
                    else:
                        skills.append(0)
            else:
                for idx in xrange(const.MAX_PANEL_SKILLS):
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
                for idx in xrange(const.MAX_PANEL_SKILLS):
                    if (idx < len(currentPanelSkills[switch])):
                        skills.append(currentPanelSkills[switch][idx])
                    else:
                        skills.append(0)
            else:
                for idx in xrange(const.MAX_PANEL_SKILLS):
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
        self.skillNext = (skillid, const.SKILL_STATE_UNKNOWN)
        owner = EntityManager.getentity(self.ownerid)
        slot = self.getSlotBySkillid(skillid)
        if slot:
            slot.updateSkillState(skillid, self.skillNext[1])
        skill = owner.GetSkill(skillid)
        if skill.JoystickYaw():
            (sskillid, sstate) = self.skillRunning
            if (sstate <= const.SKILL_STATE_PRECAST):
                slot = self.getSlotBySkillid(sskillid)
                if slot:
                    slot.updateSkillState(sskillid, (-1))

    def SkillStartM(self, skillid):
        self.comboAllowed = False
        s = self.getSlotBySkillid(skillid)
        if s:
            s.onSkillStartS(skillid)
        if (self.skillNext[0] == skillid):
            self.skillRunning = (skillid, const.SKILL_STATE_PRECAST)
            slot = self.getSlotBySkillid(skillid)
            if slot:
                slot.updateSkillState(skillid, self.skillRunning[1])
        self.skillNext = (0, const.SKILL_STATE_END)
        owner = EntityManager.getentity(self.ownerid)
        if AwakeConst.canPopAwakeDamageText(skillid, owner):
            owner.add_timer(0.1, (lambda : AwakeSkillResult()))

    def SkillCalcM(self, skillid):
        if (self.skillRunning[0] == skillid):
            self.skillRunning = (skillid, const.SKILL_STATE_PROGRESS)
            slot = self.getSlotBySkillid(skillid)
            if slot:
                slot.updateSkillState(skillid, self.skillRunning[1])

    def SkillPostM(self, skillid):
        if (self.skillRunning[0] == skillid):
            self.skillRunning = (skillid, const.SKILL_STATE_POSTCAST)
            slot = self.getSlotBySkillid(skillid)
            if slot:
                slot.updateSkillState(skillid, self.skillRunning[1])

    def SkillProgressM(self, skillid):
        if (self.skillRunning[0] == skillid):
            self.skillRunning = (skillid, const.SKILL_STATE_PROGRESS)

    def SkillMovePostM(self, skillid):
        if (self.skillRunning[0] == skillid):
            self.skillRunning = (skillid, const.SKILL_STATE_MOVEPOST)
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
            self.skillRunning = (0, const.SKILL_STATE_END)
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
            elif (sstate in (const.SKILL_STATE_UNKNOWN, const.SKILL_STATE_PRECAST)):
                res = (sskill.priority >= skill.priority)
            elif (sstate >= const.SKILL_STATE_POSTCAST):
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
            elif (nstate in (const.SKILL_STATE_UNKNOWN, const.SKILL_STATE_PRECAST)):
                res = (nskill.priority >= skill.priority)
            elif (nstate >= const.SKILL_STATE_POSTCAST):
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
PlayerAvatar = None

class Dressing(CustomMapType, ):
    __slots__ = ()
    VALUE_TYPE = None

    def on_setattr(self, key, old, new):
        self.get_owner().updateDress(key, old, new)

class ColorDressing(CustomMapType, ):
    __slot__ = ()
    VALUE_TYPE = None

    def on_setattr(self, key, old, new):
        self.get_owner().updateDress(key, old, new)

class DressEffectController(object, ):

    def __init__(self):
        super(DressEffectController, self).__init__()
        self.timers = {}
        self.sfxids = {}
        self.nodeNames = {}
        self.nodeNameEnterTime = {}

    def onDressChange(self, avatar, dressNos):
        self.cancelAllEffect(avatar)
        map(functools.partial(self.remove, avatar), [dressNo for dressNo in self.sfxids if (dressNo not in dressNos)])
        map(self.add, dressNos)

    def add(self, dressNo):
        if (dressNo not in dress_effect_data.data):
            return
        if (dressNo not in self.timers):
            self.timers[dressNo] = {}
        if (dressNo not in self.sfxids):
            self.sfxids[dressNo] = []
        for name in set(dress_effect_data.data[dressNo]['graphNodes']):
            if (name not in self.nodeNames):
                self.nodeNames[name] = {dressNo}
            else:
                self.nodeNames[name].add(dressNo)

    def remove(self, avatar, dressNo):
        if (dressNo not in dress_effect_data.data):
            return
        for timer in self.timers.pop(dressNo, {}).itervalues():
            self.safe_cancel_timer(avatar, timer)
        for sfxid in self.sfxids.pop(dressNo, []):
            avatar.model.removeFx(sfxid)
        for name in set(dress_effect_data.data[dressNo]['graphNodes']):
            if ((name in self.nodeNames) and (dressNo in self.nodeNames[name])):
                self.nodeNames[name].remove(dressNo)
                ((not self.nodeNames[name]) and self.nodeNames.pop(name))
            self.nodeNameEnterTime.pop(name, None)

    def cancelAllEffect(self, avatar):
        for dressNo in self.timers:
            for timerId in self.timers[dressNo].itervalues():
                self.safe_cancel_timer(avatar, timerId)
            self.timers[dressNo] = {}
        for dressNo in self.sfxids:
            if (self.sfxids[dressNo] is None):
                self.sfxids[dressNo] = []
            for sfxid in self.sfxids[dressNo]:
                avatar.model.removeFx(sfxid)
            self.sfxids[dressNo] = []

    def dressNoTest(self, no):
        return ((no in self.timers) and (no in self.sfxids))

    def onNodeStateChange(self, avatar, name, active):
        if (name not in self.nodeNames):
            return
        if ((avatar.model._curGraphStack != 0) or avatar.hasShapeShift):
            self.cancelAllEffect(avatar)
            self.nodeNameEnterTime.pop(name, None)
            return
        if active:
            self.nodeNameEnterTime[name] = time.time()
        for no in self.nodeNames[name]:
            if (not self.dressNoTest(no)):
                continue
            for (i, ty) in enumerate(dress_effect_data.data[no]['types']):
                if ((ty == 1) and active):
                    self.handleDressEffectEnter(avatar, no, i)
                elif ((ty == 2) and (not active)):
                    self.handleDressEffectLeave(avatar, name, no, i)

    def handleDressEffectEnter(self, avatar, dressNo, index):
        timerids = self.timers[dressNo]
        if timerids.get(index):
            self.safe_cancel_timer(avatar, timerids[index])
        timerids[index] = None
        offtime = dress_effect_data.data[dressNo]['times'][index]
        if (offtime >= 0):
            tid = avatar.add_timer(offtime, (lambda : self.addEffect(avatar, dressNo, index)))
            self.timers[dressNo][index] = tid

    def handleDressEffectLeave(self, avatar, name, dressNo, index):
        if (name not in self.nodeNameEnterTime):
            return
        toremove = []
        for (i, timerid) in self.timers[dressNo].iteritems():
            if ((dress_effect_data.data[dressNo]['types'][i] == 1) and timerid):
                self.safe_cancel_timer(avatar, timerid)
                toremove.append(i)
        map(self.timers[dressNo].pop, toremove)
        off = (time.time() - self.nodeNameEnterTime[name])
        if (off > dress_effect_data.data[dressNo]['times'][index]):
            self.addEffect(avatar, dressNo, index)

    def addEffect(self, avatar, dressNo, index):
        if ((avatar.model._curGraphStack != 0) or avatar.hasShapeShift or (not self.dressNoTest(dressNo))):
            self.cancelAllEffect(avatar)
            return
        if (index in self.timers[dressNo]):
            self.timers[dressNo][index] = None
        effect = dress_effect_data.data[dressNo]['effectPaths'][index]
        for sfxNo in self.sfxids[dressNo]:
            avatar.model.removeFx(sfxNo)
        self.sfxids[dressNo] = []
        if effect:
            ret = avatar.model.do_cue_type_effect(effect)
            if (isinstance(ret, list) and (None not in ret)):
                self.sfxids[dressNo] = ret

    def safe_cancel_timer(self, avatar, timerid):
        if (timerid in avatar._timers):
            avatar.cancel_timer(timerid)

    def __repr__(self):
        pattern = '<%s>%s, %s, %s, %s'
        return (pattern % (self.__class__.__name__, self.timers, self.sfxids, self.nodeNames, self.nodeNameEnterTime))
ENABLE_SPLIT = True

class CornerPointSpliter(object, ):

    def __init__(self):
        super(CornerPointSpliter, self).__init__()
        self.posList = []

    def Split(self, startPos, cornerPos, endPos):
        if (not ENABLE_SPLIT):
            return False
        startPos = MType.Vector3(*startPos)
        cornerPos = MType.Vector3(*cornerPos)
        endPos = MType.Vector3(*endPos)
        dir0 = (startPos - cornerPos)
        dist0 = dir0.length
        dir0.length = 1.0
        dir1 = (endPos - cornerPos)
        dist1 = dir1.length
        dir1.length = 1.0
        centerDir = (dir0 + dir1)
        if (centerDir.length < 0.001):
            return False
        centerDir.length = 1.0
        maxHalfDist = min((dist0 / 2.0), (dist1 / 2.0))
        halfDot = dir0.dot(centerDir)
        if (halfDot <= 0):
            return False
        dotValue = dir0.dot(dir1)
        maxCenterDist = min((maxHalfDist / halfDot), (30 - (dotValue * 15)))
        p1 = (cornerPos + ((dir0 * maxCenterDist) * halfDot))
        p3 = (cornerPos + ((dir1 * maxCenterDist) * halfDot))
        self.posList.append((p1.x, p1.y, p1.z))
        self.posList.append((p3.x, p3.y, p3.z))
        return True

    def GetPos(self):
        if (len(self.posList) == 0):
            return None
        return self.posList.pop(0)
UPLV_EFFECT = hardcode_resource_data.data.get(31, {}).get('path', None)
CarrierHideMode = {1: ('LeftHandWeapon', 'RightHandWeapon', 'ExtraModel', 'ExtraModel1'), 2: ('ExtraModel1', 'ExtraModel2'), 3: ('LeftHandWeapon', 'RightHandWeapon', 'ExtraModel1', 'ExtraModel2')}

class BaseRideComponent(object, ):
    Property('carrierNo', 0)
    Property('enableCarrier', 0)

    def _on_set_carrierNo(self, old):
        self.tryLeaveRiding(old)
        self.updateCarrier()

    def _on_set_enableCarrier(self, old):
        self.updateCarrier(onRideFlag=True)

    def tryLeaveRiding(self, old):
        if self.isRiding:
            self.leaveRiding()
            self.onLeaveRiding(old)

    def onLeaveRiding(self, old):
        mode = riding_data.data.get(old, dict()).get('hideAttachments', 0)
        (mode and self.showAttachments(mode))

    def updateCarrier(self, onRideFlag=False):
        if (self.enableCarrier and self.carrierNo):
            if ((not self.isRiding) and (self.enableCarrier or (self.isSpeRiding and onRideFlag))):
                self.enterRiding(self.carrierNo, onRideFlag)
                self.updateModelWithCarrier(True)
        else:
            self.leaveRiding()
            self.updateModelWithCarrier(False)

    def enterRiding(self, carrierNo, needShowAnim=False):
        self.model.enterModelRiding(riding_graph_data.data.get((self.eqSchool, self.eqBody), dict()).get('graph', ''), carrierNo, needShowAnim)

    def leaveRiding(self):
        self.model.leaveModelRiding()

    def onRidingUpdate(self):
        if getattr(self, 'topLogo', None):
            self.topLogo.UpdateHeight(self)

    def updateModelWithCarrier(self, isRiding, spCarrierNo=None):
        carrierNo = (spCarrierNo if spCarrierNo else self.carrierNo)
        self.updateModelWithCarrierEx(carrierNo, isRiding)

    def updateModelWithCarrierEx(self, carrierNo, isRiding):
        mode = riding_data.data.get(carrierNo, dict()).get('hideAttachments', 0)
        if (not mode):
            return
        if isRiding:
            self.hideAttachments(mode)
        else:
            self.showAttachments(mode)

    def showAttachments(self, mode):
        model = self.model
        for name in CarrierHideMode.get(mode, tuple()):
            model.HideAttachment(name, 0, sourceid=cconst.HIDE_ATTCH_TYPE_RIDE)

    def hideAttachments(self, mode):
        model = self.model
        for name in CarrierHideMode.get(mode, tuple()):
            model.HideAttachment(name, (-1), sourceid=cconst.HIDE_ATTCH_TYPE_RIDE)

    @property
    def isRiding(self):
        model = getattr(self, 'model', None)
        flag = bool(getattr(model, 'rideGid', False))
        if (not flag):
            return False
        horse = self.getHorse()
        return bool((horse and (not horse.is_destroyed())))

    def getHorse(self):
        return EntityManager.getentity(getattr(self.model, 'horseEntityId', None))

    @property
    def isSpeRiding(self):
        return riding_data.data.get(self.carrierNo, dict()).get('preride', False)

class Rubbing(CustomMapType, ):
    __slots__ = ()

    def on_setattr(self, key, old, new):
        print 'Rubbing on_setattr', key, old, new
        self.get_owner().updateRubbing(key, old, new)

    def on_pop(self, key, old):
        self.get_owner().updateRubbing(key, old, None)
QINGGONG_SKILL_ICON = ['UI_skillicon_gen_Jump4.png', 'UI_skillicon_gen_Jump4.png', 'UI_skillicon_gen_Jump4.png', 'UI_skillicon_gen_Jump4.png']
MILITARY_PRICE = frozenset([5113])
REFINE_ITEM_MAP = {5111: 22904, 5112: 22905, 5113: 22906}
ONE_DAY = ((24 * 60) * 60)

class MonthCardMap(CustomMapType, ):

    def on_init(self, parent):
        (MonthCard.isInited() and MonthCard().refresh())
        (FreeFlowMonthCard.isInited() and FreeFlowMonthCard().refresh())

    def on_setattr(self, key, old, new):
        (MonthCard.isInited() and MonthCard().refresh())
        (FreeFlowMonthCard.isInited() and FreeFlowMonthCard().refresh())

    def on_clear(self):
        (MonthCard.isInited() and MonthCard().refresh())
        (FreeFlowMonthCard.isInited() and FreeFlowMonthCard().refresh())

    def on_update(self, value):
        (MonthCard.isInited() and MonthCard().refresh())
        (FreeFlowMonthCard.isInited() and FreeFlowMonthCard().refresh())

    def on_assign(self):
        (MonthCard.isInited() and MonthCard().refresh())
        (FreeFlowMonthCard.isInited() and FreeFlowMonthCard().refresh())
NEW_PACKAGE_CD = (((2 * 24) * 60) * 60)
SHARE_QUERY_URL = 'g55-30069.webapp.163.com'
SHARE_KEY = '8tkq8r4o79e7ufkkm0l1eecxhgtuq3jd'
SHARE_TIMEOUT = 5
SHARE_PLATFORM_YIXIN = 1
SHARE_PLATFORM_WEIXIN = 3
H5_KEY = '2ec6d1a4e25ae4f8'

class TitleMarks(BitList, ):
    UPDATE_CALLBACK = 'onTitleStatusChanged'
MIN_HEIGHT = 8
MAX_HEIGHT = 50
NAVIGATE_CONF = {'up': '@3D_up%d', 'down': '@3D_down', 'forward': '@3D_forward', 'rush': '@3D_rush'}
NAVIGATE_UP_HEIGHT = (10, 15, 15)
NAVIGATE_FORWARD_MAX = 30
NAVIGATE_FORWARD_MIN = 8
NAVIGATE_DEST_OFFSET = 5
NAVIGATE_RUSH_DIS = 5
NAVIGATE_RUSH_HEIGHT = 3

class PlayOffTeamApply(CustomMapType, ):
    Property('teamid', 0)
    Property('name', '\xe5\xad\xa3\xe5\x90\x8e\xe8\xb5\x9b\xe6\x88\x98\xe9\x98\x9f')
    Property('leadername', '\xe9\x98\x9f\xe9\x95\xbf')
    Property('leadersch', 2)
    Property('leaderlv', 0)
    Property('isApply', 0)

class PlayOffTeamApplyList(CustomListType, ):
    VALUE_TYPE = PlayOffTeamApply

    def randomAppend(self, teamid):
        tm = PlayOffTeamApply
        tm.teamid = teamid
        self.append(tm)

class Insurance(CustomMapType, ):

    def on_setattr(self, key, old, new):
        ((not LoveInsurance.isHide()) and LoveInsurance().refresh())

    def on_assign(self):
        ((not LoveInsurance.isHide()) and LoveInsurance().refresh())

class LoveInsurances(CustomMapType, ):
    VALUE_TYPE = Insurance

    def on_setattr(self, key, old, new):
        ((not LoveInsurance.isHide()) and LoveInsurance().refresh())

    def on_clear(self):
        ((not LoveInsurance.isHide()) and LoveInsurance().refresh())

    def on_update(self, value):
        ((not LoveInsurance.isHide()) and LoveInsurance().refresh())

    def on_assign(self):
        ((not LoveInsurance.isHide()) and LoveInsurance().refresh())

class cMarriage(Marriage, ):
    Property('selfLoveIns', LoveInsurances)
    Property('mateLoveIns', LoveInsurances)

    def on_setattr(self, key, old, new):
        if (key == 'state'):
            self.get_owner().onMarriageStateChange(old, new)

class BigFishHelpers(CustomMapType, ):

    def on_setattr(self, key, old, new):
        if ((key == GlobalData.p.id) and (old is None)):
            HomeBigFishWidget().show()
        elif (not HomeBigFishWidget.isHide()):
            if (not old):
                HomeBigFishWidget().avatarIconRefresh()
            HomeBigFishWidget().flash(key)

def flag2SeldomName(flag):
    name = '_seldom_prop_'
    if (flag & Property.OWN_CLIENT):
        name += 'o'
    elif (flag & Property.ALL_CLIENTS):
        name += 'a'
    if (flag & Property.PERSISTENT):
        name += 'p'
    else:
        name += 'm'
    return name

def SeldomProperty(name, flag=1):
    if (not VALID_PROPERTY_NAME.match(name)):
        raise AttributeError(('Bad Property Name [%r]' % name))
    if (flag == Property.MANUAL):
        return
    classLocals = sys._getframe(1).f_locals
    assert (name not in classLocals['_seldom_property_'])
    classLocals['_seldom_property_'][name] = flag

def UseSeldomProperty():
    classLocals = sys._getframe(1).f_locals
    props = {}
    for (name, flag) in classLocals['_seldom_property_'].iteritems():
        if (flag in props):
            continue
        props[flag] = flag2SeldomName(flag)
    classLocals = sys._getframe(1).f_locals
    _initClassWityProperty(classLocals)
    for (flag, name) in props.iteritems():
        assert (name not in classLocals['__property_all__'])
        classLocals['__property_all__'][name] = CustomMapType
        classLocals['__property_flag__'][name] = flag
    for (name, flag) in classLocals['_seldom_property_'].items():
        classLocals['_seldom_property_'][name] = flag2SeldomName(flag)

class cFreeFlowRecord(FreeFlowRecord, ):

    def on_setattr(self, key, old, new):
        (FreeFlowMonthCard.isInited() and FreeFlowMonthCard().refresh())

    def on_clear(self):
        (FreeFlowMonthCard.isInited() and FreeFlowMonthCard().refresh())

    def on_update(self, value):
        (FreeFlowMonthCard.isInited() and FreeFlowMonthCard().refresh())

    def on_assign(self):
        (FreeFlowMonthCard.isInited() and FreeFlowMonthCard().refresh())

class cFreeFlowRecords(FreeFlowRecords, ):
    VALUE_TYPE = cFreeFlowRecord

    def on_setattr(self, key, old, new):
        (FreeFlowMonthCard.isInited() and FreeFlowMonthCard().refresh())

    def on_clear(self):
        (FreeFlowMonthCard.isInited() and FreeFlowMonthCard().refresh())

    def on_update(self, value):
        (FreeFlowMonthCard.isInited() and FreeFlowMonthCard().refresh())

    def on_assign(self):
        (FreeFlowMonthCard.isInited() and FreeFlowMonthCard().refresh())

class cItemBuyCounts(CustomMapType, ):

    def on_setattr(self, key, old, new):
        (CJEvolution.isInited() and CJEvolution().refreshItemPrice())

    def on_clear(self):
        (CJEvolution.isInited() and CJEvolution().refreshItemPrice())

class cCJEvolutionCurGame(iCJEvolutionCurGame, ):
    Property('status', 0)
    Property('curBoard', CustomListType)
    Property('synthesisCounts', CustomMapType)
    Property('itemBuyCounts', cItemBuyCounts)
    Property('itemUseCounts', CustomMapType)

class cSynthesisDayAwards(CustomMapType, ):

    def on_setattr(self, key, old, new):
        (CJEvolution.isInited() and CJEvolution().refreshDailyAward())

    def on_clear(self):
        (CJEvolution.isInited() and CJEvolution().refreshDailyAward())

class cSynthesisDayCounts(CustomMapType, ):

    def on_setattr(self, key, old, new):
        if (key == CJEvolutionConst.RANK_LIST_NUM_CCC):
            (CJEvolution.isInited() and CJEvolution().addJump('2048'))
            (CJEvolution.isInited() and CJEvolution().addJump('achv1'))

class cCJEvolutionDayRecords(iCJEvolutionRecords, ):
    Property('participateCount', 0)
    Property('synthesisCounts', cSynthesisDayCounts)
    Property('synthesisAwards', cSynthesisDayAwards)

class cSynthesisWeekCounts(CustomMapType, ):

    def on_setattr(self, key, old, new):
        if (key == CJEvolutionConst.RANK_LIST_NUM_CCC):
            (CJEvolution.isInited() and CJEvolution().refreshRankList())

    def on_clear(self):
        (CJEvolution.isInited() and CJEvolution().refreshRankList())

class cCJEvolutionWeekRecords(iCJEvolutionRecords, ):
    Property('participateCount', 0)
    Property('synthesisCounts', cSynthesisWeekCounts)
    Property('synthesisAwards', CustomMapType)

class cItemCounts(CustomMapType, ):

    def on_setattr(self, key, old, new):
        ((new > old) and CJEvolution.isInited() and CJEvolution().refreshItemSelect(key))
        (CJEvolution.isInited() and CJEvolution().refreshItemCount(key))

    def on_clear(self):
        (CJEvolution.isInited() and CJEvolution().refreshItemSelect(0))
        (CJEvolution.isInited() and CJEvolution().refreshItemCount(0))

class cGame2048(iGame2048, ):
    pass

class SurvivalBattlePSkillsHub(Dynamic, ):
    Base = PSkillsHub

    def iterValidPskills(self):
        sids = (const.SKILL_SRC_SHAPESHIFT, const.SKILL_SRC_EQUIP)
        pskills = []
        for sid in sids:
            pskill = self.get(sid, None)
            if pskill:
                pskills.append((sid, pskill))
        return pskills

class cHomesteadInfo(HomesteadInfo, ):
    Property('visitRecords', VisitRecords, Property.OWN_CLIENT)
    Property('thumbsUpRecords', VisitRecords, Property.OWN_CLIENT)
    Property('orderRecords', OrderRecords, Property.OWN_CLIENT)
    Property('makeRecords', MakeRecords, Property.OWN_CLIENT)
    Property('geomancyRecords', GeomancyRecords, Property.OWN_CLIENT)
    Property('openChestRecords', OpenChestRecords, Property.OWN_CLIENT)

    def on_setattr(self, key, old, new):
        if HomesteadMain.isInited():
            HomesteadMain().showDetailPanel()
        if (key == 'homeid'):
            MainMenuBar().restoreButtonList()
        elif (key == 'note'):
            if (not CreditShopMain.isHide()):
                CreditShopMain().showConsumePlane()
        elif (key == 'geomancyItemsFlag'):
            MainMenuBar().onRetainerUpdate()

    @property
    def thumbsUpShow(self):
        return (self.thumbsUp if (self.thumbsUp < 10000) else ('%.1fw' % (self.thumbsUp / 10000.0)))

    @property
    def scaleShow(self):
        return (self.scale if (self.scale < 10000) else ('%.1fw' % (self.scale / 10000.0)))

    @property
    def geomancyShow(self):
        return home_geomancy_data.data[GetGeomancyLevel(self.geomancy)]['name']

    def updateBuildings(self, buildings):
        for (bid, detail) in buildings.iteritems():
            if (bid not in self):
                continue
            building = self[bid]
            building.update(detail)

def playSoundEffect(name):
    path = ('sfx/ui/christmas/' + name)
    SoundManager().PlayUIEffect(path)

def playMorningExerciseEffect(index):
    path = ('sfx/QTE/QTE%d' % index)
    SoundManager().PlayEvent(SoundManager.FMOD_MEDIA_PATH, SoundManager.FMOD_SFX_FILE, path)

class MorningExerciseDanceController(object, ):
    ACTIONS = ('dance2', 'dance3', 'dance1')
    SOUND_MAX = 30

    def __init__(self):
        super(MorningExerciseDanceController, self).__init__()
        self.player = None
        self.danceBias = 0
        self.cameraSetting = None
        self.isRunning = False
        self.soundIndex = 1
        self.resetVolume = None

    def start(self, player):
        if self.isRunning:
            return
        self.player = player
        self.isRunning = True
        self.saveCameraSetting()
        for event in MConst.ExerciseStartEvents:
            player.space.triggerEvent(player, event)
        GlobalData.playerMain.showMorningExercisePanel()
        self.resetVolume = SoundManager().GetVolume()
        SoundManager().SetVolume(0, (self.resetVolume[1] * 100), (self.resetVolume[2] * 100))

    def saveCameraSetting(self):
        self.cameraSetting = None
        if GlobalData.camera:
            follower = getattr(GlobalData.camera.currMode, 'follower', None)
            if (not follower):
                return
            placer = follower.followPlacer
            self.cameraSetting = {'offset': placer.TargetPosOffset, 'direction': placer.Direction, 'bounceDelay': GlobalData.bounceCameraDelay, 'bounceArgs': GlobalData.bounceCameraArgs}

    def restoreCameraSetting(self):
        if (GlobalData.camera and self.cameraSetting):
            follower = getattr(GlobalData.camera.currMode, 'follower', None)
            if (not follower):
                return
            placer = follower.followPlacer
            placer.TargetPosOffset = self.cameraSetting['offset']
            placer.Direction = self.cameraSetting['direction']
            GlobalData.bounceCameraDelay = self.cameraSetting['bounceDelay']
            GlobalData.bounceCameraArgs = self.cameraSetting['bounceArgs']

    def stop(self):
        if (not self.isRunning):
            return
        self.isRunning = False
        GlobalData.playerMain.closeMorningExercisePanel()
        SoundManager().SetVolume((self.resetVolume[0] * 100), (self.resetVolume[1] * 100), (self.resetVolume[2] * 100))

    def playAction(self, player, actionNo):
        state = self.ACTIONS[actionNo]
        print state
        if (not (player.model and player.model.isValid() and player.model.ClearEventQueue((-1)) and player.model.JumpToState((-1), state, 0.1))):
            return

    def npcRunAction(self, actionNo):
        state = self.ACTIONS[actionNo]
        npcNos = MECD.data.get('npcNoSet', ())
        for npcNo in npcNos:
            for npc in self.player.findAllNpcWithNo(npcNo):
                npc.model.ClearEventQueue((-1))
                npc.model.JumpToState((-1), state, 0.1)

    def playExerciseSound(self):
        playMorningExerciseEffect(self.soundIndex)
        self.soundIndex += 1
        if (self.soundIndex > self.SOUND_MAX):
            self.soundIndex = 1
import time
import Timer
import utils
import formula
from client.ClientEntity import AvatarEntity, ClientAreaEntity
from common.Crontab import Crontab
from common.IdManager import IdManager
from common.RpcMethodArgs import Dict, Float, Str, Bool, BinData, List, EntityID
from common.classutils import Components, Property
from common.mobilecommon import NonexistentSwallower
from common.rpcdecorator import CLIENT_STUB, rpc_method
import MDump
import MEngine
import MRender
import MType
import MObject
import MConfig
import MHelper
from GUI.GeneralUI import GeneralEvaluate
from GUI.Loading import LoadingDispacher
from GUI.TxmMessageBox import MessageBoxLogin as MessageBox
from GUI.playermain.PlayerMain import PlayerMain
from GUI.HomeMainWidget import HomePartnerDialogue
from DeviceSetting import DeviceSetting as DS
from clan import ClanConst
from cRole import cRole
from cTopLogo import cTopLogo, LayerType, RGBA, LayerFont
from iActivity import ActivityConst
from iRide import CarrierInteractType
from iHates import AvatarHates
from iHomestead import HomesteadConst
from iTaste import TasteQuery
from txmdecorators import with_tag, delay_call
from txmengine import ModelComponent
import GlobalData
import avatarmembers
import cconst
import config
import const
import txm
import GeneralLog
import DesignFlags
import bconst
from data import riding_data
from data import school_data
from data import combatunit_data as CD
from data import combatunit_model_data as CMD

class AvatarTopLogo(cTopLogo, ):
    AbbrFontSize = LayerFont[LayerType.ClanAbbr]

    def createTextLayers(self, owner):
        super(AvatarTopLogo, self).createTextLayers(owner)
        if (owner.isInClan and owner.clanAbbr):
            offset = max(((len(unicode(owner.GetName())) * self.NameFontSize) / 2), ((len(unicode(getattr(owner, 'title', ''))) * self.TitleFontSize) / 2))
            offset += ((self.AbbrFontSize / 2) + 10)
            self.setTextLayer(LayerType.ClanAbbr, owner.clanAbbr, MType.Vector4(0, 1, 0, 1), MType.Vector4(1, 0, 0, 1), MType.Vector2((- offset), 38))

    def getExpectedTextLayerCount(self, owner):
        expectedCount = super(AvatarTopLogo, self).getExpectedTextLayerCount(owner)
        if (owner.isInClan and owner.clanAbbr):
            expectedCount += 1
        return expectedCount

    def updateTextLayers(self, owner, color, stroke):
        super(AvatarTopLogo, self).updateTextLayers(owner, color, stroke)
        isFaking = getattr(owner, 'isFaking', False)
        fakeData = getattr(owner, 'fakeData', None)
        title = (fakeData.title if isFaking else getattr(owner, 'title', ''))
        offset = max(((len(unicode(owner.GetName())) * self.NameFontSize) / 2), ((len(unicode(title)) * self.TitleFontSize) / 2))
        offset += ((self.AbbrFontSize / 2) + 10)
        if (owner.crossClanReginWinner or owner.crossClanTowerTaken):
            offset += 40
        clanLogo = (fakeData.clanLogo if isFaking else owner.clanLogo)
        color = (ClanConst.TopLogoColors.get(clanLogo) or next(ClanConst.TopLogoColors.itervalues()))
        clanAbbr = (fakeData.clanAbbr if isFaking else owner.clanAbbr)
        self.setTextLayer(LayerType.ClanAbbr, clanAbbr, RGBA(*color), stroke, MType.Vector2((- offset), 38))
        if (owner.crossClanReginWinner or owner.crossClanTowerTaken):
            icon = 'ui_dfsl_yin_0725.png'
            if owner.crossClanReginWinner:
                icon = 'ui_dfsl_jin_0725.png'
            imginfo = (icon, 150, 150, (- offset), 38)
            self.setImageLayer(LayerType.ClanAbbr, 20, imginfo=imginfo)

class AvatarRoleComponent(cRole, ):

    def createBloodBar(self, topLogoCls=None):
        if (self.IsAvatar and self.isInSurvivalBattle() and self.survivalHideBuff):
            return ''
        topLogoCls = (topLogoCls or AvatarTopLogo)
        cRole.createBloodBar.im_func(self, topLogoCls)

    def GetName(self):
        if (self.IsAvatar and self.isInSurvivalBattle() and self.survivalHideBuff):
            return ''
        if getattr(self, 'isFaking', False):
            return self.fakeData.name
        name = self.name
        if (self.monster_shapeshift and hasattr(self, 'buffs')):
            if self.buffs.hasFlag('shapeshift_name'):
                name = CD.data.get(self.monster_shapeshift, {}).get('name', '')
        crossservering = GlobalData.p.crossservering
        hostnum = getattr(self, 'hostnum', 0)
        server = GlobalData.serverList.get(hostnum, None)
        if (crossservering and hostnum and server):
            name = ('%s-%s' % (name, server.name))
        return name

    def GetNameHeight(self):
        if self.monster_shapeshift:
            no = self.monster_shapeshift
            height = (CMD.data.get(no, {}).get('nameheight', 0) * CMD.data.get(no, {}).get('Scale', 1.0))
        else:
            height = school_data.data.get(self.school, {}).get('Bodynameheight', {}).get(self.body, 0)
        if self.isDoubleCarrierAttach:
            height = riding_data.data.get(self.dCarrierInfo[2], dict()).get('attachNameHeight', height)
        elif self.isRiding:
            carrierNo = (getattr(self, 'fixedFlyCarrierNo', 0) or self.rideOtherInfo.carrierNo or self.carrierNo)
            height = riding_data.data.get(carrierNo, dict()).get('nameHeight', height)
        if (getattr(self, 'd_ride_info', None) and (self.d_ride_info[1] == const.DR_SIDE_BASE)):
            height += 0.5
        if getattr(self, 'conveyorId', None):
            carrierNo = self.getParadeCarrierNo()
            height = riding_data.data.get(carrierNo, dict()).get('nameHeight', height)
        return height

class PlayerAvatarRoleComponent(AvatarRoleComponent, ):

    def checkBloodbarVisible(self):
        if self.isInCJBattle():
            return True
        return False

    def checkTopNameVisible(self):
        return cRole.checkTopNameVisible.im_func(self)

    def checkSFXVisible(self):
        return True

class AvatarModelComponent(ModelComponent, ):

    def getModelScale(self):
        if self.monster_shapeshift:
            if self.buffs.needCombatprotoScale():
                return CMD.data.get(self.monster_shapeshift, {}).get('Scale', 1.0)
        elif self.model_shapeshift:
            return self.buffs.ModelShapeShiftScale()
        return school_data.data.get(self.school, {}).get('Scale', 1.0)

@with_tag('IsAvatar')
@Components(AvatarModelComponent, AvatarRoleComponent, impActivity_AvatarMember_2, impAward_AvatarMember_3, impCombat_AvatarMember_4, impCurrency_AvatarMember_5, impItem_AvatarMember_6, impModel_AvatarMember_7, impPokemon_AvatarMember_8, impRide_AvatarMember_9, impSpace_AvatarMember_10, impTeam_AvatarMember_11, impPK_AvatarMember_12, impSolo_AvatarMember_13, impEnhance_AvatarMember_14, impSphereMarker_AvatarMember_15, impSpaceTag_AvatarMember_16, impTitle_AvatarMember_17, impGroup_AvatarMember_18, impFish_AvatarMember_19, impHideAndSeek_AvatarMember_20, impCJBattle_AvatarMember_21, impPartner_AvatarMember_22, impSnowBattle_AvatarMember_23, impPickStar_AvatarMember_24, impSchoolmateArena_AvatarMember_25, impComrade_AvatarMember_26, impDinner_AvatarMember_27)
class Avatar(ClientAreaEntity, ):
    Property('school')
    Property('uid')
    Property('hates', AvatarHates)
    Property('xw')
    Property('origin_account', '')
    Property('body')

    def onClick(self):
        p = GlobalData.p
        if p.isInSurvivalBattle():
            return
        if (self.id != p.id):
            if (not p.canLockTarget(self)):
                p.popNotificationMsg(cconst.ANTI_LOCK_WARNING)
            else:
                p.lockTarget(self)
            if (TasteQuery.tasteInActDuration and self.buffs.tasteCarrierNo()):
                HomePartnerDialogue().show(self.id, 5)

    def destroy(self):
        try:
            self.destroyNotifyPokemon()
        except:
            import sys
            sys.excepthook(*sys.exc_info())
        super(Avatar, self).destroy()

    class EnhancePropsType(CustomListType, ):
        VALUE_TYPE = CustomMapType
    Property('achvEnhanceLv', 0)
    Property('achvEnhanceFixedPropsOrigin', EnhancePropsType)
    Property('achvEnhanceRandomPropsOrigin', EnhancePropsType)
    Property('achvEnhanceFixedGroupIds', CustomMapType)
    Property('teacherName', '', (Property.ALL_CLIENTS | Property.PERSISTENT))
    Property('msgBg', 0)
    Property('enableMsgBg', True)
    Property('msgBgMap', CustomMapType)
    Property('clanInfo', ClanInfo)
    Property('clanName', '')
    Property('clanAbbr', '')
    Property('clanLogo', '')
    Property('clanCon', 0)
    Property('clanConFrozen', 0)
    Property('clanConstrs', CustomListType)
    Property('crossClanReginWinner', CustomListType)
    Property('crossClanTowerTaken', CustomListType)
    Property('dressing', Dressing)
    Property('colorEquiped', ColorDressing)
    Property('enableCloakShow', 1)
    Property('cloakModelChoose', 0)
    Property('freeColor', FreeColor)
    Property('freeColorFirstTime', True)
    Property('freeColorHistory', FreeColorHistory)
    Property('fixedFlyNo', 0)
    Property('fixedFlyCarrierNo', 0)
    Property('mergeFriendCD', 0)
    Property('rubbing', Rubbing)
    Property('enemies', cEnemies)
    Property('enemyWatched', CustomListType)
    Property('arenaCredit', 100)
    Property('arenaInfo', iArenaInfo)
    Property('arenaReadyState', 0)
    Property('arenaTeamInfo', cArenaTeamInfo)
    Property('arenaHarmDetail', CustomMapType)
    Property('arenaStarNum', 0)
    Property('arenaDan', 1)
    Property('arenaWinInRow', 0)
    Property('arenaQLRank', 0)
    Property('arenaRobotIds', CustomListType)
    Property('arenaTimesAwardInfo', 0)
    Property('flyStage', 0)
    Property('returnFriendCD', 0)
    Property('returnScore', 0)
    Property('recallFriends', CustomMapType)
    Property('scoreGiftMask', BitList)
    Property('getRecallGiftStamp', 0)
    Property('canGetRecallGift', False)
    Property('returnRoadAwards', ReturnRoadAwards)
    Property('returnNotify', 0)
    Property('battleInfo', BattleInfo)
    '\n\t\xe5\xbf\xab\xe6\x8d\xb7\xe5\x85\x83\xe5\xae\x9d\xe6\x93\x8d\xe4\xbd\x9c\xef\xbc\x8c\xe5\x8f\xaa\xe5\x9c\xa8\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe8\xbf\x9b\xe8\xa1\x8c\xe5\x8d\xb3\xe5\x8f\xaf\xef\xbc\x8c\xe9\x81\xbf\xe5\x85\x8d\xe7\x9b\xb4\xe6\x8e\xa5\xe8\xb0\x83\xe7\x94\xa8\xe6\x9c\x8d\xe5\x8a\xa1\xe7\xab\xaf\xe6\x8e\xa5\xe5\x8f\xa3\xe5\x87\xba\xe7\x8e\xb0\xe6\xbc\x8f\xe6\xb4\x9e\n\t\xe5\x9c\xa8\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe9\x9b\x86\xe6\x88\x90\xe4\xb8\x80\xe4\xba\x9b\xe6\x93\x8d\xe4\xbd\x9c\xef\xbc\x8c\xe7\x9b\xae\xe7\x9a\x84\xe5\x8f\xaa\xe6\x98\xaf\xe4\xb8\xba\xe4\xba\x86\xe7\xae\x80\xe5\x8c\x96\xe5\xa4\xa7R\xe6\x93\x8d\xe4\xbd\x9c\xef\xbc\x8c\xe5\x8f\xaf\xe4\xbb\xa5\xe8\xae\xa4\xe4\xb8\xba\xe6\x98\xaf\xe5\xb8\xae\xe4\xbb\x96\xe6\x89\x8b\xe7\x82\xb9\xef\xbc\x8c\xe8\xbf\x99\xe6\xa0\xb7\xe8\xbe\x83\xe4\xb8\xba\xe5\xae\x89\xe5\x85\xa8\n\t'
    Property('d_ride_info', CustomListType)
    Property('isPlayOffWatcher', 0)
    Property('marriage', Marriage)
    Property('expressionAction', 0)
    Property('itemGraphAction', '')
    Property('conveyorId', '')
    _seldom_property_ = {}
    SeldomProperty('merge_from_server', (Property.ALL_CLIENTS | Property.PERSISTENT))
    SeldomProperty('returnFlag', (Property.ALL_CLIENTS | Property.PERSISTENT))
    SeldomProperty('retrunFlagStart', (Property.OWN_CLIENT | Property.PERSISTENT))
    SeldomProperty('canUploadImage', (Property.OWN_CLIENT | Property.PERSISTENT))
    UseSeldomProperty()
    Property('noGravityTeleport', 0)
    Property('gravityValue', 10)
    Property('tlpExpiredTime', 0)
    Property('tlpExtraPct', 0)
    Property('tlpGiftGold', 0)
    Property('tlpGetGiftFlag', 0)
    Property('isInPassPowering', False)
    Property('isInPassPoweringReady', False)
    Property('passPowerType', 0)
    Property('passPowerExpCount', 0)
    Property('passedPowerExpCount', 0)
    Property('interruptPassPowerCount', 0)
    Property('passPowerPartnerId', '')
    Property('survivalGameItems', SurvivalGameItems)
    Property('survivalHeavy', 0)
    Property('survivalExtraHeavy', 0.0)
    Property('survivalUpdateDressing', 0)
    Property('survivalSpecialHideBuff', 0)
    Property('survivalSchool', 1)
    Property('survivalProtoNo', 0)
    Property('survivalHideBuff', 0)
    Property('forbidenCommonCombatProps', 0)
    Property('furnitureInteractId', '', Property.ALL_CLIENTS)
    Property('furnitureInteractId', '', Property.ALL_CLIENTS)
    Property('fakeData', FakeData)
    Property('pbPhotoes', CustomListType)
    Property('likePBPhotoes', CustomListType)
    Property('photoLikeCountDaily', 0)
    Property('photoBoardItems', CustomListType)
    Property('isInSendingRose', 0)
    Property('sendingRoseType', 0)
    Property('sendingRosePartnerId', '')
    Property('isInShowRose', 0)
    Property('dTransformNo', 0)
    Property('dTransformInfo', CustomListType)
    Property('transformExpressionNo', 0)
    Property('combatFollowerId', '')
    Property('aprilFoolTrickyBoxEffectRefresh', 0)
    Property('aprilFoolTrickyBoxBuffEffect', 0)
    Property('grenadeHitCount')
    Property('dailyGrenadeCount')

    @property
    def achvEnhanceMaxLevel(self):
        return max(AED.data.get((self.school, (-1)), 0), AED.data.get(((-1), (-1)), 0))

    def getAchvEnhanceNeed(self, enhanceType):
        if (enhanceType == EnhanceType.UPGRADE):
            prefix = 'upgrade'
            lv = (self.achvEnhanceLv + 1)
        elif (enhanceType == EnhanceType.REBUILD):
            prefix = 'rebuild'
            lv = self.achvEnhanceLv
        else:
            return
        needs = {}
        record = (AED.data.get((self.school, lv), {}) or AED.data.get(((-1), lv), {}))
        needs['currency'] = record.get((prefix + 'Gold'), ())
        needs['credit'] = record.get((prefix + 'Credit'), ())
        needs['item'] = record.get((prefix + 'Item'), ())
        return needs

    def getNextNeedAchvPoint(self):
        lv = (self.achvEnhanceLv + 1)
        record = (AED.data.get((self.school, lv), {}) or AED.data.get(((-1), lv), {}))
        return record.get('needAchvPoint', 0)

    def calcAchvEnhanceProps(self, refresh_mask):
        props = {}
        achvEnhanceProps = self.curAchvEnhanceProps
        for prop in achvEnhanceProps:
            (name, value) = (prop['name'], prop['value'])
            props[name] = (props.get(name, 0) + value)
        return props

    @property
    def curAchvEnhanceProps(self):
        if (getattr(self, '_curAchvEnhanceProps', None) is None):
            self._curAchvEnhanceProps = self._calcCurAchvEnhanceProps()
        return self._curAchvEnhanceProps

    def _clearCurAchvEnhanceProps(self):
        self._curAchvEnhanceProps = None

    def _calcCurAchvEnhanceProps(self):
        props = []
        for prop in self.achvEnhanceFixedPropsOrigin:
            lvFactor = self._getAchvEnhanceLevelFactor(prop['name'], self.achvEnhanceLv)
            v = (prop['value'] * lvFactor)
            dl = (prop['dl'] * lvFactor)
            ul = (prop['ul'] * lvFactor)
            props.append({'name': prop['name'], 'value': v, 'dl': dl, 'ul': ul, 'type': 'fixed'})
        for prop in self.achvEnhanceRandomPropsOrigin:
            v = (prop['value'] * lvFactor)
            dl = (prop['dl'] * lvFactor)
            ul = (prop['ul'] * lvFactor)
            props.append({'name': prop['name'], 'value': v, 'dl': dl, 'ul': ul, 'type': 'random'})
        return props

    @property
    def rebuildAchvEnhanceProps(self):
        return self._calcRebuildAchvEnhanceProps()

    def _calcRebuildAchvEnhanceProps(self):
        props = []
        if self._achvEnhanceNewFixedPropsOrigin:
            for prop in self._achvEnhanceNewFixedPropsOrigin:
                lvFactor = self._getAchvEnhanceLevelFactor(prop['name'], self.achvEnhanceLv)
                v = (prop['value'] * lvFactor)
                dl = (prop['dl'] * lvFactor)
                ul = (prop['ul'] * lvFactor)
                props.append({'name': prop['name'], 'value': v, 'dl': dl, 'ul': ul, 'type': 'fixed'})
        if self._achvEnhanceNewRandomPropsOrigin:
            for prop in self._achvEnhanceNewRandomPropsOrigin:
                lvFactor = self._getAchvEnhanceLevelFactor(prop['name'], self.achvEnhanceLv)
                v = (prop['value'] * lvFactor)
                dl = (prop['dl'] * lvFactor)
                ul = (prop['ul'] * lvFactor)
                props.append({'name': prop['name'], 'value': v, 'dl': dl, 'ul': ul, 'type': 'random'})
        return props

    @property
    def nextAchvEnhanceProps(self):
        if (getattr(self, '_nextAchvEnhanceProps', None) is None):
            self._nextAchvEnhanceProps = self._calNextAchvEnhanceProps()
        return self._nextAchvEnhanceProps

    def _clearNextAchvEnhanceProps(self):
        self._nextAchvEnhanceProps = None

    def _calNextAchvEnhanceProps(self):
        props = []
        lv = (self.achvEnhanceLv + 1)
        for (libId, groupId) in self.achvEnhanceFixedGroupIds.iteritems():
            lib = AEULD.data.get(libId, {})
            group = lib.get('groups', {}).get(groupId, [])
            for prop in group:
                lvFactor = self._getAchvEnhanceLevelFactor(prop['name'], lv)
                dl = (prop['dl'] * lvFactor)
                ul = (prop['ul'] * lvFactor)
                props.append({'name': prop['name'], 'dl': dl, 'ul': ul, 'type': 'fixed'})
        for prop in self.achvEnhanceRandomPropsOrigin:
            lvFactor = self._getAchvEnhanceLevelFactor(prop['name'], lv)
            dl = (prop['dl'] * lvFactor)
            ul = (prop['ul'] * lvFactor)
            props.append({'name': prop['name'], 'dl': dl, 'ul': ul, 'type': 'random'})
        return props

    @property
    def nextFullAchvEnhanceProps(self):
        if (getattr(self, '_nextFullAchvEnhanceProps', None) is None):
            self._nextFullAchvEnhanceProps = self._calNextFullAchvEnhanceProps()
        return self._nextFullAchvEnhanceProps

    def _clearNextFullAchvEnhanceProps(self):
        self._nextFullAchvEnhanceProps = None

    def _calNextFullAchvEnhanceProps(self):
        props = {'fixed': [], 'random': []}
        lv = (self.achvEnhanceLv + 1)
        if (lv >= self.achvEnhanceMaxLevel):
            return props
        record = (AED.data.get((self.school, lv), {}) or AED.data.get(((-1), lv), {}))
        fixedLibs = record.get('upgradeLib', [])
        propsFixed = props['fixed']
        for libId in fixedLibs:
            propsOneLib = []
            groups = AEULD.data.get(libId, {}).get('groups', {})
            for group in groups.itervalues():
                propsOneGroup = []
                for prop in group:
                    lvFactor = self._getAchvEnhanceLevelFactor(prop['name'], lv)
                    dl = (prop['dl'] * lvFactor)
                    ul = (prop['ul'] * lvFactor)
                    propsOneGroup.append({'name': prop['name'], 'dl': dl, 'ul': ul})
                if propsOneGroup:
                    propsOneLib.append(propsOneGroup)
            propsOneLib.sort(cmp=self.cmpProps, key=itemgetter(0))
            if propsOneLib:
                propsFixed.append(propsOneLib)
        randomLibs = record.get('rebuildLib', [])
        propsRandom = props['random']
        for libId in randomLibs:
            groups = AERLD.data.get(libId, {}).get('groups', {})
            for group in groups.itervalues():
                for prop in group:
                    lvFactor = self._getAchvEnhanceLevelFactor(prop['name'], lv)
                    dl = (prop['dl'] * lvFactor)
                    ul = (prop['ul'] * lvFactor)
                    propsRandom.append({'name': prop['name'], 'dl': dl, 'ul': ul})
        propsRandom.sort(self.cmpProps)
        return props

    def _getAchvEnhanceLevelFactor(self, propName, lv):
        if (lv == 0):
            return 1.0
        tmp = (AELD.data.get((self.school, propName), {}) or AELD.data.get(((-1), propName), {}))
        ratio = tmp.get('ratio', 1.0)
        factor = pow(ratio, (lv - 1))
        spSections = tmp.get('spSections', ())
        for section in spSections:
            if (lv <= section['dl']):
                break
            cnt = (min(lv, section['ul']) - section['dl'])
            factor *= pow((section['ratio'] / ratio), cnt)
        return factor

    def cmpProps(self, prop1, prop2):
        id1 = PROP_ID_DICT.get(prop1['name'], (-1))
        id2 = PROP_ID_DICT.get(prop2['name'], (-1))
        if ((id1 == (-1)) and (id2 >= 0)):
            return 1
        elif ((id2 == (-1)) and (id1 >= 0)):
            return (-1)
        else:
            return cmp(id1, id2)

    def sortProps(self, oldProps, newProps):
        oldFixedProps = filter((lambda v: (v['type'] == 'fixed')), oldProps)
        newFixedProps = filter((lambda v: (v['type'] == 'fixed')), newProps)
        commonFixedNames = (set([prop['name'] for prop in oldFixedProps]) & set([prop['name'] for prop in newFixedProps]))
        oldCommonFixedProps = []
        newCommonFixedProps = []
        commonFixedProps = []
        for name in commonFixedNames:
            propsOld = filter((lambda v: (v['name'] == name)), oldFixedProps)
            propsNew = filter((lambda v: (v['name'] == name)), newFixedProps)
            if (propsOld and propsNew):
                oldCommonFixedProps.append(propsOld[0])
                newCommonFixedProps.append(propsNew[0])
                commonFixedProps.append((propsOld[0], propsNew[0]))
        oldUniqueFixedProps = [prop for prop in oldFixedProps if (prop not in oldCommonFixedProps)]
        newUniqueFixedProps = [prop for prop in newFixedProps if (prop not in newCommonFixedProps)]
        oldCommonFixedProps.sort(cmp=self.cmpProps)
        oldUniqueFixedProps.sort(cmp=self.cmpProps)
        newCommonFixedProps.sort(cmp=self.cmpProps)
        newUniqueFixedProps.sort(cmp=self.cmpProps)
        commonFixedProps.sort(cmp=self.cmpProps, key=itemgetter(0))
        oldRandomProps = filter((lambda v: (v['type'] == 'random')), oldProps)
        newRandomProps = filter((lambda v: (v['type'] == 'random')), newProps)
        commonRandomNames = (set([prop['name'] for prop in oldRandomProps]) & set([prop['name'] for prop in newRandomProps]))
        oldCommonRandomProps = []
        newCommonRandomProps = []
        commonRandomProps = []
        for name in commonRandomNames:
            propsOld = filter((lambda v: (v['name'] == name)), oldRandomProps)
            propsNew = filter((lambda v: (v['name'] == name)), newRandomProps)
            if (propsOld and propsNew):
                oldCommonRandomProps.append(propsOld[0])
                newCommonRandomProps.append(propsNew[0])
                commonRandomProps.append((propsOld[0], propsNew[0]))
        oldUniqueRandomProps = [prop for prop in oldRandomProps if (prop not in oldCommonRandomProps)]
        newUniqueRandomProps = [prop for prop in newRandomProps if (prop not in newCommonRandomProps)]
        oldCommonRandomProps.sort(cmp=self.cmpProps)
        oldUniqueRandomProps.sort(cmp=self.cmpProps)
        newCommonRandomProps.sort(cmp=self.cmpProps)
        newUniqueRandomProps.sort(cmp=self.cmpProps)
        commonRandomProps.sort(cmp=self.cmpProps, key=itemgetter(0))
        oldPropsOut = (((oldCommonFixedProps + oldUniqueFixedProps) + oldCommonRandomProps) + oldUniqueRandomProps)
        newPropsOut = (((newCommonFixedProps + newUniqueFixedProps) + newCommonRandomProps) + newUniqueRandomProps)
        allProps = {'fixed': {'common': commonFixedProps, 'oldUnique': oldUniqueFixedProps, 'newUnique': newUniqueFixedProps}, 'random': {'common': commonRandomProps, 'oldUnique': oldUniqueRandomProps, 'newUnique': newUniqueRandomProps}}
        return (oldPropsOut, newPropsOut, allProps)

    @CallbackHost(key=None)
    def achvEnhanceUpgrade(self, callback=None):
        self.server.achvEnhanceUpgrade()

    @rpc_method(CLIENT_STUB, Int(), Dict())
    def onAchvEnhanceUpgrade(self, errno, detail):
        if (errno != EnhanceErrorNo.SUCCESS):
            self.achvEnhanceUpgrade.notify(errno, detail)
            return
        self._clearCurAchvEnhanceProps()
        self._clearNextAchvEnhanceProps()
        self._clearNextFullAchvEnhanceProps()
        self.achvEnhanceUpgrade.notify(errno, {})

    @CallbackHost(key=None)
    def achvEnhanceRebuild(self, callback=None):
        self.server.achvEnhanceRebuild()

    @rpc_method(CLIENT_STUB, Int(), Dict())
    def onAchvEnhanceRebuild(self, errno, detail):
        if (errno != EnhanceErrorNo.SUCCESS):
            self.achvEnhanceRebuild.notify(errno, detail)
            return
        self._achvEnhanceNewFixedPropsOrigin = detail['newFixedPropsOrigin']
        self._achvEnhanceNewRandomPropsOrigin = detail['newRandomPropsOrigin']
        self.achvEnhanceRebuild.notify(errno, {})

    @CallbackHost(key=None)
    def achvEnhanceRebuildApply(self, callback=None):
        self.server.achvEnhanceRebuildApply()

    @rpc_method(CLIENT_STUB)
    def onAchvEnhanceRebuildApply(self):
        self._clearAchvEnhanceRebuildResult()
        self._clearCurAchvEnhanceProps()
        self._clearNextAchvEnhanceProps()
        self._clearNextFullAchvEnhanceProps()
        self.achvEnhanceRebuildApply.notify()

    def achvEnhanceRebuildDrop(self):
        self.server.achvEnhanceRebuildDrop()
        self._clearAchvEnhanceRebuildResult()

    def _clearAchvEnhanceRebuildResult(self):
        self._achvEnhanceNewFixedPropsOrigin = None
        self._achvEnhanceNewRandomPropsOrigin = None

    def achvEnhanceRollback(self):
        self.server.achvEnhanceRollback()

    @rpc_method(CLIENT_STUB)
    def onAchvEnhanceRollback(self):
        self._clearCurAchvEnhanceProps()
        self._clearNextAchvEnhanceProps()
        self._clearNextFullAchvEnhanceProps()

    def achvEnhanceReset(self):
        if (not DesignFlags.innerServer()):
            return
        self.achvEnhanceLv = 0
        self.achvEnhanceFixedPropsOrigin.clear()
        self.achvEnhanceFixedGroupIds.clear()
        self.achvEnhanceRandomPropsOrigin.clear()
        self._clearAchvEnhanceRebuildResult()
        self._clearCurAchvEnhanceProps()
        self._clearNextAchvEnhanceProps()
        self._clearNextFullAchvEnhanceProps()
        self.server.achvEnhanceReset()

    @rpc_method(CLIENT_STUB, Dict())
    def sayMsg(self, msg):
        GlobalData.p.onNewMsg(msg)

    @rpc_method(CLIENT_STUB, Str())
    def onStartTextEmotion(self, graph):
        self.onStopTextEmotion()
        if graph:
            self._textEmotionGid = self.model.PushGraph(graph, 0.1, 0)

    @rpc_method(CLIENT_STUB)
    def onStopTextEmotion(self):
        if getattr(self, '_textEmotionGid', None):
            self.model.PopGraph(self._textEmotionGid)
            self._textEmotionGid = None

    def __post_component__avatarmembers_impClan(self, bdict):
        self.station = ClanStation.fromTag(self.clanInfo.tag)

    def _on_set_clanAbbr(self, _):
        self.RefreshBloodBar()

    def _on_set_clanLogo(self, _):
        self.RefreshBloodBar()

    def _on_set_clanName(self, _):
        self.RefreshBloodBar()

    def _on_set_clanCon(self, _):
        ((not CreditShopMain.isHide()) and CreditShopMain().showConsumePlane())

    def updateStation(self):
        self.station = ClanStation.fromTag(self.clanInfo.tag)

    def onClanChanged(self):
        self.updateSceneTopLogo()

    @property
    def clanNo(self):
        return self.clanInfo.no

    @property
    def clanID(self):
        return self.clanInfo.guid

    @property
    def isInClan(self):
        return bool(self.clanInfo.guid)

    @property
    def isClanOwner(self):
        return (self.isInClan and (self.clanInfo.tag == ClanStation.OWNER))

    @property
    def isInClanWar(self):
        return (self.spaceno in clan_war_tower_data.data)

    def __post_component__avatarmembers_impDress(self, bdict):
        self.dressEffectController = DressEffectController()
        self.dressEffectController.onDressChange(self, self.dressing.values())

    def onDressEffectNodeActive(self, node):
        self.dressEffectController.onNodeStateChange(self, node, True)

    def onDressEffectNodeDeActive(self, node):
        self.dressEffectController.onNodeStateChange(self, node, False)

    def updateDress(self, key, old, new):
        model = getattr(self, 'model', None)
        (model and model.Reload(self.getModelData()))
        if (key == DressPart.WING):
            self.refreshEquipHalo()
        if (new in dress_effect_data.data):
            self.dressEffectController.add(new)
        if (old in dress_effect_data.data):
            self.dressEffectController.remove(self, old)

    def refreshFreeColor(self, freeColorParameter, refreshModel=False):
        model = getattr(self, 'model', None)
        if (not model):
            return
        if refreshModel:
            model.Reload(self.getModelData(), callback=functools.partial(FreeColorHelper.refreshFreeColorModel, self.dressing, self.model.model, freeColorParameter))
        else:
            FreeColorHelper.refreshFreeColorModel(self.dressing, self.model.model, freeColorParameter, self.model.modelParts)

    @property
    def isDressing(self):
        return (self.enableDress and self.dressNo)

    @property
    def isTryingDress(self):
        return False

    def _on_set_cloakModelChoose(self, old):
        model = getattr(self, 'model', None)
        if ((self.cloakModelChoose < 0) and (old >= 0)):
            self.showAttachmentsInCloak()
        elif ((self.cloakModelChoose >= 0) and (old < 0)):
            self.hideAttachmentsInCloak()
        (model and model.Reload(self.getModelData()))

    def isShowingCloak(self):
        if (not hasattr(self, 'cloakModelChoose')):
            return False
        if (not hasattr(self, 'gameItems')):
            return False
        if ('equipments' not in self.gameItems):
            return False
        if (const.EQU_PART_CLOAK not in self.gameItems['equipments']):
            return False
        return ((self.cloakModelChoose >= 0) and self.gameItems['equipments'][const.EQU_PART_CLOAK])

    def _on_set_fixedFlyNo(self, old):
        if self.fixedFlyNo:
            self.enterFixedFly()
        else:
            self.exitFixedFly()

    def _on_set_fixedFlyCarrierNo(self, old):
        self.tryLeaveRiding(old)
        self.updateFixedFlyCarrier()

    def updateFixedFlyCarrier(self, carrierCallback=None):
        carrierNo = self.fixedFlyCarrierNo
        if carrierNo:
            if (not self.isRiding):
                self.enterRiding(carrierNo)
                self.carrierCallback = utils.Functor(self.onFixedFlyCarrierLoaded, carrierCallback)
                self.updateModelWithCarrierEx(carrierNo, True)
        else:
            self.leaveRiding()
            self.updateModelWithCarrier(False)
            (carrierCallback and carrierCallback())

    def onFixedFlyCarrierLoaded(self, carrierCallback):
        self.carrierCallback = None
        (self.fixedFlyNo and self.enterFixedFly())
        (carrierCallback and carrierCallback())

    def enterFixedFly(self):
        self.doStartFly()

    def exitFixedFly(self):
        self.doExitFly()

    def _on_set_lv(self, value):
        self.updateSceneTopLogo()

    @rpc_method(CLIENT_STUB, Dict())
    def onQueryMergeFriends(self, data):
        ((not SigninWidget.isHide()) and SigninWidget().mergeFriendPanel.showFriends(data))

    @rpc_method(CLIENT_STUB, Dict())
    def onQueryMergeFriendsSize(self, data):
        ((not MergeFriendAddDialog.isHide()) and MergeFriendAddDialog().onQuerySize(data))

    @rpc_method(CLIENT_STUB, Dict())
    def onQueryMergeFriendDegree(self, data):
        ((not SigninWidget.isHide()) and SigninWidget().mergeFriendPanel.onQueryDegree(data))

    @rpc_method(CLIENT_STUB, EntityID(), Int())
    def onGetMergeFriendAward(self, eid, value):
        ((not SigninWidget.isHide()) and SigninWidget().mergeFriendPanel.onGetMergeFriendAward(eid, value))

    @rpc_method(CLIENT_STUB, EntityID(), Str())
    def onReceiveMergeFriend(self, eid, name):
        MessageBox().show(('#G%s#W\xe9\x82\x80\xe8\xaf\xb7\xe6\x82\xa8\xe4\xb8\x80\xe8\xb5\xb7\xe5\xae\x8c\xe6\x88\x90\xe6\x9c\x89\xe7\xbc\x98\xe5\x8d\x83\xe9\x87\x8c\xe6\x9d\xa5\xe7\x9b\xb8\xe4\xbc\x9a\xe4\xbb\xbb\xe5\x8a\xa1\xef\xbc\x8c\xe6\x82\xa8\xe6\x98\xaf\xe5\x90\xa6\xe6\x8e\xa5\xe5\x8f\x97\xef\xbc\x9f#R\xe6\xb3\xa8\xe6\x84\x8f\xef\xbc\x9a\xe4\xb8\x80\xe6\x97\xa6\xe6\x8e\xa5\xe5\x8f\x97\xe5\x90\x8e\xe5\xb0\x86\xe4\xb8\x8d\xe5\x8f\xaf\xe8\xa7\xa3\xe9\x99\xa4#W' % name), {'name': '\xe6\x8b\x92\xe7\xbb\x9d', 'callback': functools.partial(self.sendMergeFriendConfirm, eid, False)}, {'name': '\xe7\xa1\xae\xe5\xae\x9a', 'callback': functools.partial(self.sendMergeFriendConfirm, eid, True)})

    def sendMergeFriendConfirm(self, eid, confirm):
        self.server.confirmMergeFriend(eid, confirm)
        (confirm and PopmsgPool().AddMsg('\xe6\x81\xad\xe5\x96\x9c\xe6\x82\xa8\xe6\x8e\xa5\xe5\x8f\x97\xe4\xba\x86\xe9\x82\x80\xe8\xaf\xb7\xef\xbc\x81\xe8\xaf\xb7\xe5\x88\xb0\xe7\xa6\x8f\xe5\x88\xa9\xe7\x95\x8c\xe9\x9d\xa2\xe5\xaf\xb9\xe5\xba\x94\xe7\x95\x8c\xe9\x9d\xa2\xe4\xb8\xad\xe6\x9f\xa5\xe7\x9c\x8b\xef\xbc\x81'))

    @rpc_method(CLIENT_STUB, Str(), Bool())
    def onMergeFriendConfirm(self, name, confirm):
        if confirm:
            ((not SigninWidget.isHide()) and self.server.queryMergeFriends())
            PopmsgPool().AddMsg(('\xe6\x81\xad\xe5\x96\x9c\xef\xbc\x8c#G%s#W\xe6\x8e\xa5\xe5\x8f\x97\xe4\xba\x86\xe6\x82\xa8\xe7\x9a\x84\xe9\x82\x80\xe8\xaf\xb7\xef\xbc\x8c\xe8\xaf\xb7\xe5\x88\xb0\xe7\xa6\x8f\xe5\x88\xa9\xe7\x95\x8c\xe9\x9d\xa2\xe5\xaf\xb9\xe5\xba\x94\xe7\x95\x8c\xe9\x9d\xa2\xe4\xb8\xad\xe6\x9f\xa5\xe7\x9c\x8b\xef\xbc\x81' % name))
        else:
            PopmsgPool().AddMsg(('\xe6\x8a\xb1\xe6\xad\x89\xef\xbc\x81#G%s#W\xe6\x8b\x92\xe7\xbb\x9d\xe4\xba\x86\xe6\x82\xa8\xe7\x9a\x84\xe9\x82\x80\xe8\xaf\xb7\xef\xbc\x8c\xe8\xaf\xb7\xe9\x87\x8d\xe8\xaf\x95' % name))

    @rpc_method(CLIENT_STUB, Int(), Dict())
    def otherClientStartQte(self, qteno, params):
        graphs = {1: 'shuoyan_climb2.graph', 2: 'shuoyan_qte2.graph', 3: 'shuoyan_qte2.graph', 4: 'shuoyan_qte2.graph'}
        gvars = {1: 0, 2: 0, 3: 1, 4: 2}
        self.qteparam = params
        self.model.applyGravity(False)
        self.syncPosOff()
        self.model.PushQteGraph(graphs.get(qteno))
        self.model.SetVariableI((-1), 'QTE_NUM', gvars.get(qteno))
        if params.get('DestPos'):
            QteEvent(self).onSetDestByParam('DestPos')

    @rpc_method(CLIENT_STUB)
    def otherClientExitQte(self):
        self.syncPosOn()
        self.model.applyGravity(True)
        self.model.PopQteGraph()

    @rpc_method(CLIENT_STUB, Str())
    def otherClientSyncQteStatus(self, nodename):
        if getattr(self.model, '_qtegraph', None):
            self.model.JumpToState(self.model._qtegraph, nodename, 0.1)

    @rpc_method(CLIENT_STUB, Float(), Float())
    def otherClientSyncSkillASprint(self, distance, yaw):
        space = Space()
        if (space and space.world and space.world.PhysicsSpace and self.model.isValid()):
            self.syncPosOff()
            self.doSprintTarget(distance, yaw)

    def triggerQte(self, signal, params):
        QteEvent(self).run(signal, params)

    def getQteParam(self, argname):
        if getattr(self, 'qteparam', None):
            return self.qteparam.get(argname)

    def on_speed(self, speed):
        if self.d_ride_info:
            (entityid, dr_side, _) = self.d_ride_info
            entity = EntityManager.getentity(entityid)
            if (dr_side == const.DR_SIDE_ATTACH):
                speed = (entity.speed if entity else speed)
            else:
                (entity and entity.on_speed(speed))
        (getattr(self, 'model', None) and self.model.on_speed(speed))

    def doSprintTarget(self, distance, yaw):
        graph = school_data.data.get(self.school, {}).get('ASprintGraph', '')
        if (not graph):
            return
        sprintpos = self.calcSprintPosition(distance, yaw)
        if (not sprintpos):
            return
        self.model.SetSendActivatedSignal(0, graph, True)
        self.model.JumpToState(0, graph, 0.1)
        sprintpos = MType.Vector3(*sprintpos)
        self.model.SetVariableV3(0, 'G_MOTION_DEST_POS', sprintpos)
        self.model.SetVariableF(0, 'G_YAW', self.yaw)

    @property
    def canJumpToLocomotion(self):
        return ((not self.isQinggong()) and (not self.isCharging()) and (not self.is3DNavigating()) and (not getattr(self, 'skillPosIndicator', None)))

    def getSweepShape(self):
        if hasattr(self, '_sweepShape'):
            return self._sweepShape
        self._sweepShape = MObject.CreateObject('PhysicsShapeWrapper')
        self._sweepShape.SetShapeToSphereImmediately((self.bodyRadius / 2))
        return self._sweepShape

    def sweepClosest(self, startPoint, endingPoint):
        sweepMatrix = MType.Matrix4x3()
        sweepMatrix.translation = startPoint
        physicsSpace = Space().world.PhysicsSpace
        filterInfo = 6
        collideResult = physicsSpace.AllSweep(self.getSweepShape(), sweepMatrix, endingPoint, filterInfo)
        return collideResult

    def sweepGround(self, pos):
        pos = (pos[0], pos[1], pos[2])
        startPoint = MType.Vector3(*pos)
        endPoint = MType.Vector3(*pos)
        endPoint.y = (endPoint.y - 100.0)
        results = self.sweepClosest(startPoint, endPoint)
        results = filter((lambda obj: (not isinstance(obj.Body, MObject.PhysicsTriggerComponent))), results)
        if (results and results[0].IsHit and results[0].Body.Parent.AnimatorDestructor):
            return results[0].Pos
        else:
            return None

    def sweepTerrainHeight(self, pos, radius):
        sweepShape = MObject.CreateObject('PhysicsShapeWrapper')
        sweepShape.SetShapeToBoxImmediately((2 * radius), (2 * radius), 0.2)
        diff = 6
        startPoint = MType.Vector3(*pos)
        endPoint = MType.Vector3(*pos)
        startPoint.y = (startPoint.y + diff)
        sweepMatrix = MType.Matrix4x3()
        sweepMatrix.translation = startPoint
        physicsSpace = Space().world.PhysicsSpace
        collideResult = physicsSpace.ClosestSweep(sweepShape, sweepMatrix, endPoint, 6)
        if collideResult:
            return max(collideResult.Pos.y, endPoint.y)
        return endPoint.y

    def getNearestSnarePos(self):
        nearest = None
        mindist = None
        from SpaceSnare import SpaceSnare
        for snare in Space().entities.itervalues():
            if (not isinstance(snare, SpaceSnare)):
                continue
            if ((not mindist) or (formula.distance2DSqr(snare.position, self.position) < mindist)):
                mindist = formula.distance2DSqr(snare.position, self.position)
                nearest = snare
        return nearest.position

    def pickCliffAround(self):
        closest = self.raycastCliff(239.5, 100)
        if closest:
            groundPos = self.sweepGround((closest.Pos.x, 300, closest.Pos.z))
            self.position = (groundPos.x, groundPos.y, groundPos.z)
            self.yaw = (closest.Normal.yaw - 3.14)
            return ((groundPos.x, groundPos.y, groundPos.z), (closest.Normal.yaw - 3.14))

    def pickSafeLand(self, direction=None, srcpos=None):
        direction = (direction or self.yaw)
        startpos = self.position
        zvector = formula.yawToVector(direction)
        if srcpos:
            detectpos = (srcpos[0], (srcpos[1] + 1.0), srcpos[2])
            result = self.sweepGround(detectpos)
            if result:
                return (result.x, result.y, result.z)
        for i in xrange(3, 50):
            detectpos = ((startpos[0] + (zvector[0] * i)), (startpos[1] + 20.0), (startpos[2] + (zvector[(-1)] * i)))
            result = self.sweepGround(detectpos)
            if result:
                return (result.x, result.y, result.z)
        for i in xrange(3, 1, (-1)):
            detectpos = ((startpos[0] + (zvector[0] * i)), (startpos[1] + 20.0), (startpos[2] + (zvector[(-1)] * i)))
            result = self.sweepGround(detectpos)
            if result:
                return (result.x, result.y, result.z)
        return self.position

    def raycastCliff(self, ylevel, dist):
        if (not self.model.isValid()):
            return
        transform = self.model.model.Transform
        frm = transform.translation
        frm.y = ylevel
        probes = [transform.x_axis, transform.z_axis, (MType.Vector3(0, 0, 0) - transform.x_axis), (MType.Vector3(0, 0, 0) - transform.z_axis)]
        castresults = [Space().rawRaycast(frm, to, dist, cconst.PHYSICS_OBSTACLE_QUERY) for to in probes]
        castresults = filter((lambda result: (result.IsHit and result.Body.Parent and result.Body.Parent.AnimatorDestructor)), castresults)
        if castresults:
            closest = min(castresults, key=(lambda c: c.Distance))
            return closest

    def updateRubbing(self, key, old, new):
        model = getattr(self, 'model', None)
        (model and model.Reload(self.getModelData()))

    def isQinggong(self):
        return (self.flyStage > 0)

    def checkExpressing(self):
        return (not (not self.expressionAction))

    @rpc_method(CLIENT_STUB, Tuple())
    def moveToEnemiesPos(self, pos):
        print 'client run: =====', pos
        self.model.moveTo(pos, None)

    @rpc_method(CLIENT_STUB, Int())
    def watchFail(self, failno):
        msg = EnemyConst.FAILMSG[failno]
        ScreenPopmsg.PopmsgPool().AddMsg(msg)

    def isEnemy(self, eid):
        for em in self.enemies:
            if (em.id == eid):
                return True
        return False

    def watchEnemyPos(self, eid):
        if ((eid not in self.enemyWatched) and (not self.checkSkyEye())):
            self.watchFail(EnemyConst.SKYEYE_NOT_ENOUGH)
            return
        self.server.watchEnemyPos(eid)

    def checkSkyEye(self):
        itemList = self.gameItems.getSortedItemsByItemId(EnemyConst.SKYEYE_ITEM_ID)
        if (len(itemList) == 0):
            return False
        return True

    def delEnemy(self, eid):
        self.server.delEnemy(eid)
        pass

    def onDelEnemy(self, eid):
        pass

    def onAddEnemy(self, eid):
        pass

    @property
    def arenaTeamSide(self):
        return self.arenaInfo.teamSide

    @property
    def arenaTeamsShowInfo(self):
        return self.arenaInfo.teamsShowInfo

    @rpc_method(CLIENT_STUB)
    def confirmOnArena(self):
        AW().destroy()
        AC().show()
        print 'match success, confirm?'

    @rpc_method(CLIENT_STUB, Int())
    def applyArenaSuccess(self, wTime):
        (AW.isHide() and AW().show(wTime))

    @rpc_method(CLIENT_STUB, Bool())
    def onFetchArenaGameStart(self, isStart):
        if (not AR.isHide()):
            AR().onFetchArenaGameStart(isStart)

    def onConfirmOnArena(self, isConfirm):
        self.server.onConfirmOnArena(isConfirm)

    def cancelApplyArena(self):
        self.server.cancelArenaApply()

    @rpc_method(CLIENT_STUB, EntityID(), Str(), Int())
    def onCancelApplyArena(self, eid, name, reason):
        AW().destroy()
        if (eid == self.id):
            return
        msg = ''
        if (reason == ArenaConst.CANCEL_ARENA_REASON_PLAYER_CLICK):
            msg = ('#G%s#W\xe5\x8f\x96\xe6\xb6\x88\xe6\x9c\xac\xe6\xac\xa1\xe7\xab\x9e\xe6\x8a\x80\xe5\x9c\xba\xe9\x98\x9f\xe6\x8e\x92\xe6\x8a\xa5\xe5\x90\x8d' % name)
        elif (reason == ArenaConst.CANCEL_ARENA_REASON_LOGOFF):
            msg = ('#G%s#W\xe6\x8e\x89\xe7\xba\xbf\xef\xbc\x8c\xe6\x9c\xac\xe6\xac\xa1\xe7\xab\x9e\xe6\x8a\x80\xe5\x9c\xba\xe6\x8a\xa5\xe5\x90\x8d\xe5\x8f\x96\xe6\xb6\x88' % name)
        elif (reason == ArenaConst.CANCEL_ARENA_REASON_LEAVETEAM):
            msg = ('#G%s#W\xe7\xa6\xbb\xe9\x98\x9f\xef\xbc\x8c\xe6\x9c\xac\xe6\xac\xa1\xe7\xab\x9e\xe6\x8a\x80\xe5\x9c\xba\xe6\x8a\xa5\xe5\x90\x8d\xe5\x8f\x96\xe6\xb6\x88' % name)
        elif (reason == ArenaConst.CANCEL_ARENA_REASON_TEAM_CHANGE):
            msg = '\xe9\x98\x9f\xe4\xbc\x8d\xe6\x88\x90\xe5\x91\x98\xe5\x8f\x91\xe7\x94\x9f\xe5\x8f\x98\xe5\x8c\x96\xef\xbc\x8c\xe6\x9c\xac\xe6\xac\xa1\xe7\xab\x9e\xe6\x8a\x80\xe5\x9c\xba\xe6\x8a\xa5\xe5\x90\x8d\xe5\x8f\x96\xe6\xb6\x88'
        elif (reason == ArenaConst.CANCEL_ARENA_REASON_BATTLE):
            return
        elif (reason == ArenaConst.CANCEL_ARENA_REASON_LEVELDAN):
            msg = ('#G%s#W\xe5\x8d\x87\xe7\xba\xa7\xe7\xad\x89\xe7\xba\xa7\xe6\xae\xb5\xef\xbc\x8c\xe6\x9c\xac\xe6\xac\xa1\xe7\xab\x9e\xe6\x8a\x80\xe5\x9c\xba\xe6\x8a\xa5\xe5\x90\x8d\xe5\x8f\x96\xe6\xb6\x88' % name)
        self.popNotificationMsg(msg)

    @rpc_method(CLIENT_STUB)
    def onArenaShutDown(self):
        self.popNotificationMsg('\xe7\xab\x9e\xe6\x8a\x80\xe5\x9c\xba\xe5\x85\xb3\xe9\x97\xad')
        AW().destroy()

    @rpc_method(CLIENT_STUB)
    def clearArenaConfirmUI(self):
        print 'cleara ui ====='
        self.clearArenaConfirmUIClient()

    def clearArenaConfirmUIClient(self):
        AC().destroy()

    @rpc_method(CLIENT_STUB)
    def matchOverTime(self):
        self.clearArenaConfirmUIClient()

    @rpc_method(CLIENT_STUB)
    def onOneConfirm(self):
        AC().onConfirm()

    def _on_set_arenaReadyState(self, old):
        self.logger.debug('on _on_set_arenaReadyState id %s', self.id)
        self.updateSceneTopLogo()

    @rpc_method(CLIENT_STUB)
    def arenaCountDown(self):
        PM().countDownShow()

    @rpc_method(CLIENT_STUB, Int())
    def arenaRoundEnd(self, res):
        if (res == 0):
            PM().playTieAnim()
        elif (res == 1):
            PM().playWinAnim()
        else:
            PM().playLoseAnim()
        self.add_timer(3, (lambda : self.popNotificationMsg('\xe4\xb8\x8b\xe4\xb8\x80\xe5\xb1\x80\xe6\xaf\x94\xe8\xb5\x9b\xe5\x8d\xb3\xe5\xb0\x86\xe5\xbc\x80\xe5\xa7\x8b\xef\xbc\x8c\xe8\xaf\xb7\xe5\x81\x9a\xe5\xa5\xbd\xe5\x87\x86\xe5\xa4\x87\xef\xbc\x81')))
        AR().resetClock()
        if (not ArenaWatch.isHide()):
            ArenaWatch().resetAvtInfo()

    @rpc_method(CLIENT_STUB, Int())
    def applyArenaFail(self, failno):
        msg = const.ARENA_FAIL_MSG[failno]
        self.popNotificationMsg(msg)

    @rpc_method(CLIENT_STUB, Int())
    def arenaRoundStart(self):
        AR().startCount()
        self.clearArenaKillTimes()

    @rpc_method(CLIENT_STUB, Dict())
    def roundOver(self, winRes):
        pass

    def fetchArenaRoundTime(self):
        self.server.fetchArenaRoundTime()

    @rpc_method(CLIENT_STUB, Int())
    def arenaRoundCountDown(self, remain):
        print 'start count down client run reconnect', remain
        AR().show()
        AR().startCount(remain)

    @rpc_method(CLIENT_STUB, Int(), Int(), Int(), Int())
    def calArenaResult(self, winc, tiec, losec, res):
        print 'result win: %d tie: %d lose: %d'
        if (res == 0):
            print 'IT IS TIE GAME'
        elif (res == (-1)):
            print 'YOU LOSE'
        elif (res == 1):
            print 'YOU WIN'

    @rpc_method(CLIENT_STUB, Int())
    def arenaResult(self, res):
        if (res == 0):
            print 'GAME RESULT: TIE'
        elif (res == 1):
            print 'GAME RESULT: YOU WIN'
        else:
            print 'GAME RESULT: YOU LOSE'

    @rpc_method(CLIENT_STUB, Int())
    def clearArenaUI(self, iswin):
        if (not self.isInArena()):
            return
        if (not self.arenaTeamInfo.isAvailable):
            return
        if AR().visible:
            AR().destroy()
        if AD().visible:
            AD().destroy()
        self.arearesultmap = iswin
        print 'clearArenaUI: ', self.arearesultmap

    @rpc_method(CLIENT_STUB)
    def clearArenaUIRunAway(self):
        AR().destroy()
        AD().destroy()

    @rpc_method(CLIENT_STUB)
    def updatePlayerLive(self):
        AR().updateAllTeamAlive()

    def isInArena(self):
        if (not getattr(self, 'spaceno', None)):
            return False
        inquiry = SpaceInquiry(self.spaceno)
        return (inquiry.type == SpaceType.ARENA)

    @rpc_method(CLIENT_STUB, List())
    def printArenaForGM(self, eids):
        print eids

    @rpc_method(CLIENT_STUB, Str())
    def matchTeamInfos(self, teaminfo):
        print teaminfo

    @rpc_method(CLIENT_STUB)
    def arenaDanInfoDebug(self):
        print '\xe6\x98\x9f\xe6\x95\xb0\xef\xbc\x9a', self.arenaStarNum
        print '\xe6\xae\xb5\xe4\xbd\x8d\xe7\xbc\x96\xe5\x8f\xb7\xef\xbc\x9a', self.arenaDan
        print '\xe6\xae\xb5\xe4\xbd\x8d\xe5\x90\x8d\xe7\xa7\xb0: ', ADD.data.get(self.arenaDan, {}).get('name', '')
        print '\xe6\x9c\x80\xe8\xbf\x91\xe8\xbf\x9e\xe8\x83\x9c\xe6\x95\xb0: ', self.arenaWinInRow

    @rpc_method(CLIENT_STUB)
    def setArenaLimit(self):
        self.arenaLimit = False

    @rpc_method(CLIENT_STUB)
    def playArenaDeadEff(self):
        print 'playArenaDeadEff'
        eff = HRD.data.get(46, {}).get('path', '')
        if eff:
            self.model.play_effect_inner(eff)

    def isLVForArena(self):
        return (self.lv >= space_data.data.get(206, {}).get('LevelMin', 1))

    def getQinggongIcon(self):
        index = min(self.flyStage, (self.getMaxQinggongStage() - 1))
        return QINGGONG_SKILL_ICON[index]

    def getMaxQinggongStage(self):
        if (self.isJumping() or self.isHatKingJumping()):
            return 2
        return min(qinggong_level_data.data.get(self.lv, 0), SpaceInquiry(self.spaceno).maxQinggongStage)

    def isJumping(self):
        return (const.BUFF_ID_JUMP in self.buffs)

    def isHatKingJumping(self):
        return (const.BUFF_ID_HATKING in self.buffs)

    def stopQinggong(self):
        self.flyStage = 0
        self.model.FireEvent(0, '@qg_break')

    @rpc_method(CLIENT_STUB, Int())
    def onStartQinggong(self, stage):
        self.showAttachmentsInCloak(1)
        fullpath = ('qg_%d' % stage)
        self.flyStage = 1
        self.model.JumpToState(0, fullpath, 0)

    def onQinggongStarted(self):
        pass

    def onQinggongStage(self, stage):
        if ((stage < 0) or (stage > self.getMaxQinggongStage())):
            raise ('invalid qinggong stage %d' % stage)
        self.flyStage = stage

    def onQinggongPost(self):
        pass

    @rpc_method(CLIENT_STUB)
    def onQinggongEnded(self):
        self.flyStage = 0

    def _on_set_returnNotify(self, _):
        (ReturnWindow.isInited() and ReturnWindow().updateNotifier())
        self.updateReturnNotify()

    @rpc_method(CLIENT_STUB, Dict())
    def onQueryReturnFriends(self, data):
        if SigninWidget.isHide():
            return
        widget = SigninWidget()
        panel = getattr(widget, 'returnFriendPanel', None)
        if (not panel):
            if data.get('friends', tuple()):
                widget.showReturnFriendPanel()
                panel = widget.returnFriendPanel
            else:
                return
        panel.showFriends(data)

    @rpc_method(CLIENT_STUB, Dict())
    def onQueryReturnFriendsSize(self, data):
        ((not ReturnFriendAddDialog.isHide()) and ReturnFriendAddDialog().onQuerySize(data))

    @rpc_method(CLIENT_STUB, Dict())
    def onQueryReturnFriendDegree(self, data):
        ((not SigninWidget.isHide()) and SigninWidget().returnFriendPanel.onQueryDegree(data))

    @rpc_method(CLIENT_STUB, EntityID(), Int())
    def onGetReturnFriendAward(self, eid, value):
        ((not SigninWidget.isHide()) and SigninWidget().returnFriendPanel.onGetReturnFriendAward(eid, value))

    @rpc_method(CLIENT_STUB, EntityID(), Str())
    def onReceiveReturnFriend(self, eid, name):
        MessageBox().show(('#G%s#W\xe9\x82\x80\xe8\xaf\xb7\xe6\x82\xa8\xe4\xb8\x80\xe8\xb5\xb7\xe5\xae\x8c\xe6\x88\x90\xe4\xba\xb2\xe5\x8f\x8b\xe5\xb8\xae\xe5\xb8\xae\xe5\xbf\x99\xe4\xbb\xbb\xe5\x8a\xa1\xef\xbc\x8c\xe6\x82\xa8\xe6\x98\xaf\xe5\x90\xa6\xe6\x8e\xa5\xe5\x8f\x97\xef\xbc\x9f#R\xe6\xb3\xa8\xe6\x84\x8f\xef\xbc\x9a\xe4\xb8\x80\xe6\x97\xa6\xe6\x8e\xa5\xe5\x8f\x97\xe5\x90\x8e\xe5\xb0\x86\xe4\xb8\x8d\xe5\x8f\xaf\xe8\xa7\xa3\xe9\x99\xa4#W' % name), {'name': '\xe6\x8b\x92\xe7\xbb\x9d', 'callback': functools.partial(self.sendReturnFriendConfirm, eid, False)}, {'name': '\xe7\xa1\xae\xe5\xae\x9a', 'callback': functools.partial(self.sendReturnFriendConfirm, eid, True)})

    def sendReturnFriendConfirm(self, eid, confirm):
        self.server.confirmReturnFriend(eid, confirm)
        (confirm and PopmsgPool().AddMsg('\xe6\x81\xad\xe5\x96\x9c\xe6\x82\xa8\xe6\x8e\xa5\xe5\x8f\x97\xe4\xba\x86\xe9\x82\x80\xe8\xaf\xb7\xef\xbc\x81\xe8\xaf\xb7\xe5\x88\xb0\xe7\xa6\x8f\xe5\x88\xa9\xe7\x95\x8c\xe9\x9d\xa2\xe5\xaf\xb9\xe5\xba\x94\xe7\x95\x8c\xe9\x9d\xa2\xe4\xb8\xad\xe6\x9f\xa5\xe7\x9c\x8b\xef\xbc\x81'))

    @rpc_method(CLIENT_STUB, Str(), Bool())
    def onReturnFriendConfirm(self, name, confirm):
        if confirm:
            ((not SigninWidget.isHide()) and self.server.queryReturnFriends())
            PopmsgPool().AddMsg(('\xe6\x81\xad\xe5\x96\x9c\xef\xbc\x8c#G%s#W\xe6\x8e\xa5\xe5\x8f\x97\xe4\xba\x86\xe6\x82\xa8\xe7\x9a\x84\xe9\x82\x80\xe8\xaf\xb7\xef\xbc\x8c\xe8\xaf\xb7\xe5\x88\xb0\xe7\xa6\x8f\xe5\x88\xa9\xe7\x95\x8c\xe9\x9d\xa2\xe5\xaf\xb9\xe5\xba\x94\xe7\x95\x8c\xe9\x9d\xa2\xe4\xb8\xad\xe6\x9f\xa5\xe7\x9c\x8b\xef\xbc\x81' % name))
        else:
            PopmsgPool().AddMsg(('\xe6\x8a\xb1\xe6\xad\x89\xef\xbc\x81#G%s#W\xe6\x8b\x92\xe7\xbb\x9d\xe4\xba\x86\xe6\x82\xa8\xe7\x9a\x84\xe9\x82\x80\xe8\xaf\xb7\xef\xbc\x8c\xe8\xaf\xb7\xe9\x87\x8d\xe8\xaf\x95' % name))

    def onReturnShareConfirm(self, platform, cycle):
        if ((not platform) and (not cycle)):
            return
        GlobalData.accountMgr.ShareToFriend(platform, ('[\xe5\xa4\xa9\xe4\xb8\x8b\xe6\x89\x8b\xe6\xb8\xb8]%s\xe7\x9a\x84\xe5\x9b\xbe\xe7\x89\x87\xe5\x88\x86\xe4\xba\xab' % self.name), time.ctime(), (MEngine.AppLocalPath + '/LocalData/Patch/ui_share_replay_0110.png'), '', '', cycle)
        GlobalData.accountMgr.BindEvent('ShareEnd', self.onReturnShareEnd)
        CutShare().hide()

    def onReturnShareEnd(self, platform, ret, reason):
        PopmsgPool().AddMsg(('\xe5\x88\x86\xe4\xba\xab\xe6\x88\x90\xe5\x8a\x9f' if (ret == 0) else '\xe5\x88\x86\xe4\xba\xab\xe5\xa4\xb1\xe8\xb4\xa5'))

    @rpc_method(CLIENT_STUB, Dict())
    def onQueryRecallFriends(self):
        if ((not SigninWidget.isHide()) and (len(self.recallFriends) > 0)):
            if (not getattr(SigninWidget(), 'recallFriendPanel', None)):
                SigninWidget().showRecallFriendPanel()
            else:
                SigninWidget().recallFriendPanel.refresh()

    @rpc_method(CLIENT_STUB, Dict())
    def onGetRecallFriendGift(self):
        if getattr(SigninWidget(), 'recallFriendPanel', None):
            SigninWidget().recallFriendPanel.refreshGiftButton()

    @rpc_method(CLIENT_STUB, Dict())
    def onGetReturnScoreGift(self):
        from GUI.ReturnWidget import ReturnWindow, ReturnController
        if (not ReturnWindow.isHide()):
            panel = ReturnWindow().panels.get(ReturnController.CreditsExchange)
            (panel and panel.refresh())

    def checkReturnOnEnterSpace(self):
        if getattr(self, 'ReturnBtnShowFlag', False):
            return
        self.ReturnBtnShowFlag = True
        if self.isNewReturnPlayer():
            PlayerMain().tempBtnList.refreshBtns()
            PlayerMain().tempBtnList2.refreshBtns()
            ((not ReturnWindow.isInited()) and ReturnWindow().show())

    @rpc_method(CLIENT_STUB)
    def onGetReturnRoadAward(self):
        if (not ReturnWindow.isHide()):
            panel = ReturnWindow().panels.get(ReturnController.Activity)
            (panel and panel.refresh())

    def isNewReturnPlayer(self):
        return (self.getSeldomProperty('returnFlag', False) and ReturnConst.isInNewReturnActivity(self.getSeldomProperty('retrunFlagStart', None)))

    def updateReturnNotify(self):
        PlayerMain().tempBtnList.updateReturnButtonRedDot()
        PlayerMain().tempBtnList2.updateReturnButtonRedDot()

    @property
    def needReturnNotify(self):
        ret = (self.hasReturnSigninAward() or self.canGetReturnRoadAward() or self.canGetReturnScoreAward() or self.canGetReturnRaffleItem())
        if (not ret):
            return self.checkActivityRebateNotify(ReturnConst.RETURN_REBATE_ACTIVITYNO)
        return ret

    def canGetReturnRoadAward(self):
        for (no, data) in sorted(return_road_award_data.data.items()):
            if ((not self.returnRoadAwards.hasGetAward(no)) and self.returnRoadAwards.canGetAward(no)):
                return True
        return False

    def canGetReturnScoreAward(self):
        for score in return_score_award_data.data.iterkeys():
            if ((not self.scoreGiftMask.getBit(score)) and (self.returnScore >= score)):
                return True
        return False

    def isInBattle(self):
        if (not getattr(self, 'spaceno', None)):
            return False
        inquiry = SpaceInquiry(self.spaceno)
        return (inquiry.type == SpaceType.BATTLE)

    def isInBattleNew(self):
        return (self.spaceno == BattleNewbieConst.SPACENO)

    def isInAnyPVPSpace(self):
        return (self.isInBattle() or self.isInArena() or self.isInClanFight() or self.isInSnowBattle() or self.isInCJBattle())

    def isInClanFight(self):
        if (not getattr(self, 'spaceno', None)):
            return False
        inquiry = SpaceInquiry(self.spaceno)
        return (inquiry.type == SpaceType.CLAN_FIGHT)

    @property
    def battleTeamSide(self):
        return self.battleInfo.teamside

    def __init_component__avatarmembers_impQuickConsume(self, bdict):
        self.quickConsumeCallback = None
        self.quickConsumeIndex = 1
        self.inquirePriceMoneyCb = {}
        self._isQuickConsuming = False
        self.setQuickConsumingTimer = None
        self.moneyItemPriceExpired = {}

    @property
    def isQuickConsuming(self):
        return self._isQuickConsuming

    @isQuickConsuming.setter
    def isQuickConsuming(self, v):
        if self.setQuickConsumingTimer:
            self.cancel_timer(self.setQuickConsumingTimer)
            self.setQuickConsumingTimer = None
        self._isQuickConsuming = v
        if v:
            self.setQuickConsumingTimer = self.add_timer(2, self.resetQuickConsuming)

    def resetQuickConsuming(self):
        self.setQuickConsumingTimer = None
        self.isQuickConsuming = False

    def queryQuickConsumeGold(self, cost, callback):
        if (not self.isQuickConsuming):
            self.tryQueryGoldPrice(0, cost, callback)

    @limit_call(0.5)
    def goldConsumeCheck(self, cost, checkCallback=None, costCallback=None, callback=None, msg=''):

        def okCallback():
            checkCallback()
            self.tryQuickConsume(cost, costCallback, callback)
        if (not self.canQuickConsume(cost)):
            MessageBox().show(msg, {'name': '\xe5\x8f\x96\xe6\xb6\x88', 'countdown': 20}, {'name': '\xe7\xa1\xae\xe5\xae\x9a', 'callback': (lambda : okCallback())})
            return False
        return True

    @limit_call(0.5)
    def tryQuickConsume(self, cost, costGoldCallback=None, consumeCallback=None):
        if self.canQuickConsume(cost):
            (consumeCallback and consumeCallback())
            return
        if self.isQuickConsuming:
            return
        self.quickConsumeIndex += 1
        self.quickConsumeCallback = consumeCallback
        self.tryQueryGoldPrice(self.quickConsumeIndex, cost, costGoldCallback)

    def tryQueryGoldPrice(self, index, cost, costGoldCallback):
        lack = dict()
        if (self.money < cost.get('money', 0)):
            lack['money'] = int(math.ceil((float((cost.get('money', 0) - self.money)) / const.EXCHANGE_GOLD_MONEY)))
        if (self.military < cost.get('military', 0)):
            lack['military'] = int(math.ceil((float((cost.get('military', 0) - self.money)) / const.EXCHANGE_GOLD_MILITARY)))
        items = cost.get('items', {})
        if items:
            lack['items'] = {}
        moneyItems = {}
        for (itemId, count) in items.iteritems():
            if (self.gameItems.getItemCountByItemId(itemId) >= count):
                continue
            n = (count - self.gameItems.getItemCountByItemId(itemId))
            ways = map((lambda w: w[0]), WTOID.data.get(itemId, {}).get('ways', ()))
            ways = filter((lambda w: (w in (WayType.MONEY_MALL, WayType.GOLD_MALL))), ways)
            if (not ways):
                print itemId, ways
                return costGoldCallback({})
            if (WayType.GOLD_MALL in ways):
                info = GoldMallCommon.getItemInfoByItemId(itemId)
                if (info is None):
                    return costGoldCallback({})
                lack['items'][itemId] = (info['price'] * n)
            else:
                moneyItems[itemId] = n
        if moneyItems:
            self.inquirePrice(MALL_ITEM_CONST.MALL_TYPE_MONEY, moneyItems.keys())
            self.inquirePriceMoneyCb[self.inquirePriceMoney] = (index, cost, lack, moneyItems, costGoldCallback)
        else:
            self.inquirePriceMoney(index, cost, lack, {}, costGoldCallback)

    def inquirePriceMoney(self, index, cost, lack, moneyItems, costGoldCallback=None):
        for (itemId, count) in moneyItems.iteritems():
            if (itemId in MILITARY_PRICE):
                lack['items'][itemId] = int(math.ceil((float((count * self.tradeInfoMoney.getTradeItem(itemId).price)) / const.EXCHANGE_GOLD_MILITARY)))
            else:
                lack['items'][itemId] = int(math.ceil((float((count * self.tradeInfoMoney.getTradeItem(itemId).price)) / const.EXCHANGE_GOLD_MONEY)))
        if (not lack.get('items', {})):
            lack.pop('items', None)
        totalGold = sum(map((lambda s: ((isinstance(s, dict) and sum(s.values())) or s)), lack.itervalues()))
        (costGoldCallback and costGoldCallback(lack))
        if self.gameItems.getContainerById(GAMEITEM_CONST.TEMP_BAG_ID):
            PopmsgPool().AddMsg('\xe6\x82\xa8\xe7\x9a\x84\xe5\x8c\x85\xe8\xa3\xb9\xe5\xb7\xb2\xe6\xbb\xa1\xef\xbc\x8c\xe8\xaf\xb7\xe5\xb0\x86\xe4\xb8\xb4\xe6\x97\xb6\xe5\x8c\x85\xe8\xa3\xb9\xe4\xb8\xad\xe7\x89\xa9\xe5\x93\x81\xe5\x8f\x96\xe5\x87\xba\xe5\x90\x8e\xe5\x86\x8d\xe8\xaf\x95')
            return
        if (index != self.quickConsumeIndex):
            return
        if (not self.quickConsumeCallback):
            return
        if (not self.isEnoughGold(totalGold, showRecharge=True)):
            return
        self.setQuickConsumeStatus(False)
        moneyGold = (lack.get('money', 0) + sum([lack['items'][itemId] for itemId in moneyItems if (itemId not in MILITARY_PRICE)]))
        if moneyGold:
            self.exchangeGoldMoney(moneyGold)
        militaryGold = (lack.get('military', 0) + sum([lack['items'][itemId] for itemId in moneyItems if (itemId in MILITARY_PRICE)]))
        if militaryGold:
            self.exchangeGoldMilitary(militaryGold)
        items = cost.get('items', {})
        goldItems = {}
        moneyItems = {}
        for (itemId, count) in items.iteritems():
            if (self.gameItems.getItemCountByItemId(itemId) >= count):
                continue
            n = (count - self.gameItems.getItemCountByItemId(itemId))
            ways = map((lambda w: w[0]), WTOID.data.get(itemId, {}).get('ways', ()))
            ways = filter((lambda w: (w in (WayType.MONEY_MALL, WayType.GOLD_MALL))), ways)
            if (WayType.GOLD_MALL in ways):
                info = GoldMallCommon.getItemInfoByItemId(itemId)
                goldItems[info['itemno']] = n
            else:
                moneyItems[itemId] = n
        (goldItems and self.server.quickBuyGoldMallItem(goldItems))
        (moneyItems and self.server.quickPlayerBuy(MALL_ITEM_CONST.MALL_TYPE_MONEY, moneyItems))
        self.add_timer(0, functools.partial(self.tickQuickConsume, index, cost))

    def tickQuickConsume(self, index, cost):
        if (index != self.quickConsumeIndex):
            return
        if (not hasattr(self, 'startQuickConsume')):
            self.startQuickConsume = time.time()
        if self.canQuickConsume(cost):
            del self.startQuickConsume
            self.setQuickConsumeStatus(True)
            (self.quickConsumeCallback and self.quickConsumeCallback())
            self.quickConsumeCallback = None
            return
        if ((time.time() - self.startQuickConsume) > 1):
            del self.startQuickConsume
            self.setQuickConsumeStatus(True)
            lacks = {REFINE_ITEM_MAP.get(itemId, itemId): (count - self.gameItems.getItemCountByItemId(itemId)) for (itemId, count) in cost.get('items', {}).iteritems() if (self.gameItems.getItemCountByItemId(itemId) < count)}
            if lacks:
                itemId = lacks.keys()[0]
                ways = map((lambda w: w[0]), WTOID.data.get(itemId, {}).get('ways', ()))
                ways = filter((lambda w: (w in (WayType.MONEY_MALL, WayType.GOLD_MALL))), ways)
                if (WayType.GOLD_MALL in ways):
                    info = GoldMallCommon.getItemInfoByItemId(itemId)
                    (canbuy, reason) = self.canBuyGoldMallItem(info['itemno'], lacks[itemId])
                    if (not canbuy):
                        PopmsgPool().AddMsg(('\xe8\xb4\xad\xe4\xb9\xb0#G%s#W\xe5\xa4\xb1\xe8\xb4\xa5, %s' % (item_data.data.get(itemId, {}).get('Name', ''), reason)))
                elif (self.getMaxBuycount(itemId) < lacks[itemId]):
                    PopmsgPool().AddMsg(('\xe6\x93\x8d\xe4\xbd\x9c\xe5\xa4\xb1\xe8\xb4\xa5, #G%s#W\xe5\x89\xa9\xe4\xbd\x99\xe5\x8f\xaf\xe8\xb4\xad\xe6\x95\xb0\xe9\x87\x8f\xe4\xb8\x8d\xe8\xb6\xb3' % item_data.data.get(itemId, {}).get('Name', '')))
                else:
                    PopmsgPool().AddMsg('\xe6\x93\x8d\xe4\xbd\x9c\xe5\xa4\xb1\xe8\xb4\xa5')
            return
        self.add_timer(0, functools.partial(self.tickQuickConsume, index, cost))

    def canQuickConsume(self, cost):
        if (self.money < cost.get('money', 0)):
            return False
        if (self.military < cost.get('military', 0)):
            return False
        for (itemId, count) in cost.get('items', {}).iteritems():
            if (self.gameItems.getItemCountByItemId(itemId) < count):
                return False
        return True

    def setQuickConsumeStatus(self, v):
        PopmsgPool().setEnable(v)
        ItemMeteor.setEnable(v)
        self.isQuickConsuming = (not v)

    def checkCostMilitaryMall(self, items=None, callback=None):
        if (not items):
            (callback and callback())
            return
        lack = {}
        for (itemId, count) in items.iteritems():
            if (self.gameItems.getItemCountByItemId(itemId) >= count):
                continue
            n = (count - self.gameItems.getItemCountByItemId(itemId))
            ways = [w[0] for w in WTOID.data.get(itemId, {}).get('ways', ()) if (w[0] == WayType.MILITARY_MALL)]
            if ways:
                lack[itemId] = n
        if lack:
            itemNo = lack.keys()[0]
            MessageBox().show(('\xe6\x82\xa8\xe7\xbc\xba\xe5\xb0\x91#G%s#W\xef\xbc\x8c\xe6\x98\xaf\xe5\x90\xa6\xe5\x89\x8d\xe5\xbe\x80\xe8\xb4\xad\xe4\xb9\xb0\xef\xbc\x9f' % item_data.data.get(itemNo, {}).get('Name', '')), {'name': '\xe5\x8f\x96\xe6\xb6\x88', 'countdown': 10}, {'name': '\xe7\xa1\xae\xe5\xae\x9a', 'callback': (lambda : MallMain().showMilitary().buyItem(itemNo, (-1)))})
            return
        (callback and callback())

    @limit_call(0.1)
    def quickRfineUseMoney(self, cost, queryCallback=None, consumeCallback=None):
        print cost, queryCallback, consumeCallback, self.isQuickConsuming
        if (consumeCallback and self.canQuickConsume(cost)):
            consumeCallback()
            return
        moneyItems = {}
        for (itemId, count) in cost['items'].iteritems():
            if (self.gameItems.getItemCountByItemId(itemId) >= count):
                continue
            n = (count - self.gameItems.getItemCountByItemId(itemId))
            ways = map((lambda w: w[0]), WTOID.data.get(REFINE_ITEM_MAP.get(itemId, itemId), {}).get('ways', ()))
            ways = filter((lambda w: (w in (WayType.MONEY_MALL,))), ways)
            if (not ways):
                (queryCallback and queryCallback())
                (consumeCallback and consumeCallback())
                return
            moneyItems[REFINE_ITEM_MAP.get(itemId, itemId)] = n
        if self.isQuickConsuming:
            return
        self.quickConsumeIndex += 1
        self.quickConsumeCallback = consumeCallback
        querys = [itemId for itemId in moneyItems.keys() if (time.time() > self.moneyItemPriceExpired.get(itemId, 0))]
        if querys:
            self.inquirePrice(MALL_ITEM_CONST.MALL_TYPE_MONEY, querys)
            self.inquirePriceMoneyCb[self.inquireRefineMoney] = (self.quickConsumeIndex, cost, moneyItems, queryCallback, querys)
        else:
            self.inquireRefineMoney(self.quickConsumeIndex, cost, moneyItems, queryCallback, querys)

    def inquireRefineMoney(self, index, cost, moneyItems, queryCallback, querys):
        for itemId in querys:
            self.moneyItemPriceExpired[itemId] = (time.time() + 5)
        total = 0
        for (itemId, count) in moneyItems.iteritems():
            total += (count * self.tradeInfoMoney.getTradeItem(itemId).price)
        if queryCallback:
            queryCallback((total + cost.get('money')))
        if (index != self.quickConsumeIndex):
            return
        if self.quickConsumeCallback:

            def doQuickBuy():
                (moneyItems and self.server.quickPlayerBuy(MALL_ITEM_CONST.MALL_TYPE_MONEY, moneyItems))
                self.add_timer(0, functools.partial(self.tickQuickConsume, index, cost))
            if (self.money < (total + cost.get('money'))):
                ExchangeMain().showMoneyConfirmPlane(((total + cost.get('money')) - self.money), doQuickBuy)
                return
            doQuickBuy()

    def _on_set_d_ride_info(self, old):
        print '_on_set_d_ride_info >>>', self.d_ride_info, old
        self.UpdateDoubleRide()
        if (not self.d_ride_info):
            self.speed = 5.0
            self.model.HideAttachment('RightHandWeapon', 0, sourceid=cconst.HIDE_ATTCH_TYPE_DRIDE)
            self.model.HideAttachment('LeftHandWeapon', 0, sourceid=cconst.HIDE_ATTCH_TYPE_DRIDE)
        else:
            self.model.HideAttachment('RightHandWeapon', (-1), sourceid=cconst.HIDE_ATTCH_TYPE_DRIDE)
            self.model.HideAttachment('LeftHandWeapon', (-1), sourceid=cconst.HIDE_ATTCH_TYPE_DRIDE)
        (self.hideExtraModel(cconst.HIDE_ATTCH_TYPE_DRIDE) if self.d_ride_info else self.showExtraModel(cconst.HIDE_ATTCH_TYPE_DRIDE))

    def UpdateDoubleRide(self):
        print 'UpdateDoubleRide >>>', self
        self.model.updateDoubleRide()
        if getattr(self, 'topLogo', None):
            self.topLogo.UpdateHeight(self)
        PlayerMain().UpdateAttackBtnIcon()

    def is3DNavigating(self):
        return (self._3d_navigate_status != '')

    @rpc_method(CLIENT_STUB, Str())
    def onStart3DNavigate(self, status):
        self._3d_navigate_status = status
        self.model.JumpToState(0, '3DNavigate', 0)

    @rpc_method(CLIENT_STUB, Str(), Str(), Tuple())
    def onUpdate3DNavigate(self, status, event, dest):
        if (event == ''):
            event = '@3DNavigateBreak'
        self._3d_navigate_status = status
        self.model.FireEvent(0, event)
        self.model.SetVariableV3(0, 'G_MOTION_DEST_POS', MType.Vector3(*dest))

    def isInWeddingSite(self):
        return (self.space and (SpaceInquiry(self.space.spaceno).type == SpaceType.WEDDING))

    def isInWedding(self):
        return (self.isInWeddingSite() and (self.id in (GlobalData.p.weddingInfo.get('husbandId', ''), GlobalData.p.weddingInfo.get('wifeId', ''))))

    def doExpression(self, action):
        self.expressionAction = action
        event = EAD.data.get(action, {}).get('event', '')
        self.hideAttachments(1)
        self.model.gotoLocomotion(0)
        self.model.FireEvent(0, ('@' + event))

    def doExitExpression(self):
        self.model.gotoLocomotion(0)
        self.showAttachments(1)

    def updateExpressionAction(self):
        if self.expressionAction:
            self.doExpression(self.expressionAction)

    def _on_set_expressionAction(self, old):
        if self.expressionAction:
            self.doExpression(self.expressionAction)
        elif old:
            self.doExitExpression()

    def _on_set_itemGraphAction(self, old):
        self.model.updateItemGraphState(self.itemGraphAction)

    def _on_set_conveyorId(self, old):
        self.tryLeaveParade(old)
        self.updateParade()

    def tryLeaveParade(self, old):
        if old:
            conveyor = EntityManager.getentity(old)
            (conveyor and self.onLeaveRiding(conveyor.no))

    def updateParade(self):
        self.model.updateParadeBase()
        self.updateModelWithCarrierEx(self.getParadeCarrierNo(), bool(self.conveyorId))
        if getattr(self, 'topLogo', None):
            self.topLogo.UpdateHeight(self)
        (self.hideExtraModel(cconst.HIDE_ATTCH_TYPE_PARADE) if self.conveyorId else self.showExtraModel(cconst.HIDE_ATTCH_TYPE_PARADE))

    def getConveyor(self):
        return EntityManager.getentity(self.conveyorId)

    def getParadeCarrierNo(self):
        conveyor = self.getConveyor()
        return (conveyor.no if conveyor else 0)

    def hasSeldomProperty(self, name):
        flag = self._seldom_property_.get(name, None)
        return ((not flag) or (name in getattr(self, flag)))

    def getSeldomProperty(self, name, default=None):
        flag = self._seldom_property_.get(name, None)
        return (default if (not flag) else getattr(self, flag).get(name, default))

    @rpc_method(CLIENT_STUB)
    def refreshHomePage(self):
        from GUI.social.TxSpriteDialog import TxSpriteDialog
        from GUI.social.Main import SocialMain
        if SocialMain.isHide():
            TxSpriteDialog.refreshSpriteRecommend(self.onRefreshRecommend)
        else:
            SocialMain().txSpriteDialog.askForSpriteRecommend(forceRefresh=True)

    def onRefreshRecommend(self, text):
        from GUI.social.TxSpriteDialog import TxSpriteDialog
        TxSpriteDialog.refreshSpriteHomePageContent(text.split('|')[0])

    def resumeGravity(self):
        self.gravityValue = 10
        self.model.applyGravity(True)

    def setGravityValue(self, value):
        self.gravityValue = (10 * value)
        self.model.applyGravity(True)

    def isInBamboo(self):
        if (not getattr(self, 'space', None)):
            return False
        if (not getattr(self, 'spaceno', None)):
            return False
        inquiry = SpaceInquiry(self.spaceno)
        return (inquiry.type == SpaceType.BAMBOO_BATTLE)

    def onBambooEnterSpace(self):
        if self.isInBamboo():
            BambooRun().show()
        elif (not BambooRun.isHide()):
            BambooRun().destroy()

    def onExitBambooFlag(self, flagid):
        self.cancel_cleaningBambooFlag()
        self.server.onExitBambooFlag(flagid)

    def onEnterBambooFlag(self, eid):
        print 'onEnterBambooFlag ', SkillChargeBar.isHide()
        self.showCleanBambooFlag(eid, '\xe5\x87\x80\xe5\x8c\x96\xe6\x97\x97\xe5\xb8\x9c', 'ui_602.png', bamboo_args_data.data.get('cleanTime', 10))
        self.server.onEnterBambooFlag(eid)

    @rpc_method(CLIENT_STUB, EntityID(), Int())
    def checkBambooFlagUI(self, flagid, dis):
        flag = self.space.entities.get(flagid, None)
        if (flag and formula.inRange(flag.position, self.position, dis) and SkillChargeBar.isHide()):
            self.showCleanBambooFlag(flagid, '\xe5\x87\x80\xe5\x8c\x96\xe6\x97\x97\xe5\xb8\x9c', 'ui_602.png', bamboo_args_data.data.get('cleanTime', 10))

    @rpc_method(CLIENT_STUB, Str())
    def bambooFlagInterrupt(self, msg):
        if (not SkillChargeBar.isHide()):
            SkillChargeBar().onCollectingInterrupted()
        self.popNotificationMsg(msg)

    def showCleanBambooFlag(self, eid, title, icon, duration):
        SkillChargeBar().npcButtonShow(title, icon, duration, startCallback=functools.partial(self.onCleanBambooFlagStart, eid), interruptCallback=functools.partial(self.onCleanBambooFlagInterrupt, eid), endCallback=functools.partial(self.onCleanBambooFlagEnd, eid))
        SkillChargeBar().setNpcButtonClickCB(functools.partial(self.tryCleanBambooFlag, eid))

    def tryCleanBambooFlag(self, eid):
        self.server.tryCleanBambooFlag(eid)

    @rpc_method(CLIENT_STUB, Int())
    def onTryCleanBambooFlag(self, res):
        if (res == 1):
            self.popNotificationMsg('\xe6\x97\x97\xe5\xb8\x9c\xe4\xb8\x8d\xe5\xad\x98\xe5\x9c\xa8')
            return
        if (res == 2):
            self.popNotificationMsg('\xe6\x97\x97\xe5\xb8\x9c\xe6\xad\xa3\xe5\x9c\xa8\xe8\xa2\xab\xe5\x85\xb6\xe5\xae\x83\xe4\xba\xba\xe5\x87\x80\xe5\x8c\x96')
            return
        if (res == 3):
            self.popNotificationMsg('\xe6\x97\x97\xe5\xb8\x9c\xe5\xb7\xb2\xe8\xa2\xab\xe6\x88\x91\xe6\x96\xb9\xe5\x8d\xa0\xe6\x9c\x89')
            return
        if (res == 4):
            self.popNotificationMsg('\xe6\x97\x97\xe5\xb8\x9c\xe4\xb8\x8d\xe5\x9c\xa8\xe5\x87\x80\xe5\x8c\x96\xe8\x8c\x83\xe5\x9b\xb4')
            return
        if (res == 0):
            SkillChargeBar().npcButtonOriginClick()

    def onCleanBambooFlagStart(self, flagid):
        print 'onCleanBambooStart ', flagid
        if (not self.stateIM.applyInstruction(SICD.BAMBOO_CLEAN_FLAG)):
            return
        self.server.onCleanBambooFlagStart(flagid)
        self.isBambooCleanFlag = True
        return True

    def onCleanBambooFlagInterrupt(self, flagid):
        print 'onCleanBambooInterrupt ', flagid
        self.isBambooCleanFlag = False
        self.server.onCleanBambooInterrupt(flagid)

    def onCleanBambooFlagEnd(self, flagid):
        print 'onCleanBambooEnd ', flagid
        self.server.onCleanBambooFlagEnd(flagid)
        self.isBambooCleanFlag = False

    @rpc_method(CLIENT_STUB, Int(), Int())
    def onBambooTeamScoreChanged(self, redScore, blueScore):
        if (not BambooRun.isHide()):
            BambooRun().refreshScore(redScore, blueScore)

    @rpc_method(CLIENT_STUB)
    def onFetchBambooTime(self):
        if (not BambooRun.isHide()):
            BambooRun().refreshRemainTime(self.battleStartTime.starttime, self.battleStartTime.isBegin)
        if (not BattleStatics.isHide()):
            BattleStatics().showCountDown()

    @rpc_method(CLIENT_STUB)
    def showBambooResult(self):
        BattleResult().show()

    def _on_set_tlpExpiredTime(self, _):
        if self.isDuringTlp():
            self.popNotificationMsg('\xe6\x81\xad\xe5\x96\x9c\xe4\xbd\xa0\xef\xbc\x8c\xe4\xbd\xa0\xe8\x8e\xb7\xe5\xbe\x97\xe4\xba\x86\xe4\xb8\x80\xe6\xac\xa1\xe9\x99\x90\xe6\x97\xb6\xe5\x85\x85\xe5\x80\xbc\xe4\xbc\x98\xe6\x83\xa0\xef\xbc\x8c\xe8\xb5\xb6\xe7\xb4\xa7\xe5\x8e\xbb\xe7\x9c\x8b\xe7\x9c\x8b\xe5\x90\xa7')
            self.clickTlpBtn = False
            PlayerMain().tempBtnList.refreshBtns()
            PlayerMain().tempBtnList2.refreshBtns()

    def isDuringTlp(self):
        return (time.time() < self.tlpExpiredTime)

    @rpc_method(CLIENT_STUB)
    def onTlpPushEnd(self):
        PlayerMain().tempBtnList.onTlpEnd()
        PlayerMain().tempBtnList2.onTlpEnd()
        ((not TlpWindow.isHide()) and TlpWindow().destroy())

    @rpc_method(CLIENT_STUB)
    def onTriggerTlpCompensate(self):
        '\xe8\x8e\xb7\xe5\xbe\x97\xe5\x85\x85\xe5\x80\xbc\xe5\xa5\x96\xe5\x8a\xb1'
        ((not TlpWindow.isHide()) and TlpWindow().refreshButtonState())

    @rpc_method(CLIENT_STUB)
    def onGetTlpCompensate(self):
        PlayerMain().tempBtnList.onTlpEnd()
        PlayerMain().tempBtnList2.onTlpEnd()
        ((not TlpWindow.isHide()) and TlpWindow().destroy())

    def isTlpActive(self):
        return (self.isDuringTlp() and ((not self.tlpGetGiftFlag) or (self.tlpGiftGold > 0)))

    @property
    def canPassOrPassed(self):
        if (self.interruptPassPowerCount < 3):
            return True
        return False

    @property
    def canPassPower(self):
        if self.canPassOrPassed:
            return True
        return False

    @property
    def canPassedPower(self):
        if self.canPassOrPassed:
            return True
        return False

    def _on_set_isInPassPowering(self, old):
        if ((not self.isInPassPowering) and (self.isInPassPowering == old)):
            return
        if (not hasattr(self, 'passGraphId')):
            self.passGraphId = None
        if ((not old) and self.isInPassPowering):
            self.startPassPowerDelay()
        if (old and (not self.isInPassPowering)):
            self.stopPassPower()

    def _on_set_passPowerExpCount(self, old):
        ((not PassPowerMain.isHide()) and PassPowerMain().updateExpCount())

    def _on_set_passedPowerExpCount(self, old):
        ((not PassPowerMain.isHide()) and PassPowerMain().updateExpCount())

    def enterPasssPowerSpace(self):
        if self.isInPassPowering:
            self.startPassPowerDelay()

    def startPassPower(self):
        if (hasattr(self, 'passGraphId') and self.passGraphId):
            return
        self.hideAttachments(1)
        self.model.gotoLocomotion(0)
        self.model.leaveModelRiding()
        if (self.passPowerType == PassPowerConst.PassPowerType):
            self.passGraphId = self.model.PushGraph('chuangong_giver.graph', 0, 0)
            self.model.FireEvent((-1), 'chuangong_next')
        elif (self.passPowerType == PassPowerConst.PassedPowerType):
            self.passGraphId = self.model.PushGraph('chuangong_accepter.graph', 0, 0)
            self.model.FireEvent((-1), 'chuangong_next')
        if getattr(self, 'startPassTimer', None):
            self.cancel_timer(self.startPassTimer)
            self.startPassTimer = None
        if (self.id == GlobalData.p.id):
            if (not self.stateIM.applyInstruction(SICD.PASSPOWER_INTERACT)):
                self.exitPassPowerSystem()
                return
            PassPowerMain().show()
            return

    def startPassPowerDelay(self):
        if getattr(self, 'startPassTimer', None):
            self.cancel_timer(self.startPassTimer)
            self.startPassTimer = None
        self.startPassTimer = self.add_repeat_timer(0.5, self.startRealPP)

    def isPassPowerPosReady(self):
        return (all(map(PassPowerConst.passPowerPosNear, self.pos, self.position)) and (abs((self.yaw - self.area.yaw)) < 0.1) and self.model.isValid() and PassPowerConst.checkSpace(self.space))

    def startRealPP(self):
        if (getattr(self, 'model', None) and getattr(self.model, 'model', None) and self.isPassPowerPosReady() and (not self.enableCarrier)):
            self.startPassPower()
            if getattr(self, 'startPassTimer', None):
                self.cancel_timer(self.startPassTimer)
                self.startPassTimer = None

    def stopPassPower(self):
        '\n\t\t\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe7\xbb\x93\xe6\x9d\x9f\xe4\xbc\xa0\xe5\x8a\x9f\n\t\t1. \xe9\x80\x80\xe5\x87\xba\xe4\xbc\xa0\xe5\x8a\x9f\xe7\x9a\x84\xe4\xb8\xbb\xe7\x95\x8c\xe9\x9d\xa2\n\t\t2. \xe4\xbb\x8e\xe4\xbc\xa0\xe5\x8a\x9f\xe5\x8a\xa8\xe4\xbd\x9c\xe6\x81\xa2\xe5\xa4\x8d\xe5\x88\xb0\xe9\xbb\x98\xe8\xae\xa4\xe7\x9a\x84\xe5\x8a\xa8\xe4\xbd\x9c\n\t\t3. \xe6\x81\xa2\xe5\xa4\x8d\xe4\xb8\x80\xe5\x88\x87\xe8\xbe\x93\xe5\x85\xa5\n\t\t'
        if (hasattr(self, 'passGraphId') and (self.passGraphId is not None)):
            self.model.FireEvent((-1), 'chuangong_next')
            self.add_timer(3, self.exitPassPowerAction)

    def exitPassPowerAction(self):
        (self.passGraphId and self.model.PopGraph(self.passGraphId))
        self.model.gotoLocomotion(0)
        self.showAttachments(1)
        self.passGraphId = None

    def isInSurvivalBattle(self):
        if (not getattr(self, 'spaceno', None)):
            return False
        inquiry = SpaceInquiry(self.spaceno)
        return (inquiry.type == SpaceType.SURVIVAL_BATTLE)

    def _on_set_survivalUpdateDressing(self, old):
        if (not self.isSurvivalHideBuff()):
            model = getattr(self, 'model', None)
            (model and model.Reload(self.getModelData()))
            if (self.enableCarrier and self.carrierNo):
                self.updateCarrier()
                self.add_timer(0.5, self.survivalUpdateCarrier)

    def _on_set_survivalSpecialHideBuff(self, old):
        model = getattr(self, 'model', None)
        (model and model.Reload(self.getModelData()))
        if (self.enableCarrier and self.carrierNo and (not self.isRiding)):
            self.updateCarrier()
            self.add_timer(0.5, self.survivalUpdateCarrier)

    def survivalUpdateCarrier(self):
        if (not self.isInSurvivalBattle()):
            return
        if (self.enableCarrier and self.carrierNo and (not self.isRiding)):
            self.updateCarrier()
            self.add_timer(0.5, self.survivalUpdateCarrier)

    def survivalLeaveRiding(self):
        self.server.survivalLeaveRiding()

    def getSurvivalSpecialHideModelData(self):
        MODEL_REPLACE_MAP = {4129: 4103, 4020: 4103}
        modelItemId = MODEL_REPLACE_MAP.get(self.survivalSpecialHideBuff, self.survivalSpecialHideBuff)
        proto_id = (-1)
        if (SurvivalGameItem.getTypeByItemId(modelItemId) == GAMEITEM_CONST.BASETYPE_WEAPON):
            proto_id = item_data.data.get(modelItemId, {}).get('ItemModelRightHand', (-1))
        elif (SurvivalGameItem.getTypeByItemId(modelItemId) == GAMEITEM_CONST.BASETYPE_ARMS):
            proto_id = item_data.data.get(modelItemId, {}).get('ItemModelLeftHand', (-1))
            if (proto_id < 0):
                proto_id = item_data.data.get(modelItemId, {}).get('ItemModelExtra', (-1))
        model_data = dict()
        if (proto_id < 0):
            model_data['Models'] = {}
            effectId = SIFD.data.get(self.survivalSpecialHideBuff)
            if effectId:
                model_data['AttachEffect'] = ('%s,%s' % (effectId, 'root'))
            else:
                model_data['Models'] = (('Item/yl/2017/yl_item_2017', ''),)
        else:
            data = item_model_data.data.get(proto_id, {})
            model_data['Models'] = data.get('Models', {})
            model_data['Name'] = data.get('Name', '')
            model_data['Skeleton'] = data.get('Skeleton', '')
            model_data['BasicGraph'] = 'weapon_rotate.graph'
            effectId = data.get('Effects')
            if effectId:
                if isinstance(effectId, (tuple,)):
                    effectId = effectId[0]
                if isinstance(effectId, (str,)):
                    effectId = effectId[:effectId.find(':')]
                    if effectId:
                        model_data['AttachEffect'] = ('%s,%s' % (effectId, 'root'))
        return model_data

    def survivalUpdateModel(self):
        model = getattr(self, 'model', None)
        (model and model.Reload(self.getModelData()))

    def isSurvivalHideBuff(self):
        if (self.isInSurvivalBattle() and self.survivalHideBuff):
            return True
        return False

    def _on_set_furnitureInteractId(self, old):
        if (old and (not self.furnitureInteractId)):
            furniture = HomeBuildingManager().buildingMap.get(old)
            if (self.model.model and self.model.model.IsValid()):
                if furniture:
                    furniture.leaveInteract(self.model.model, self.id)
                    self.onLeaveFurnitureInteract(old)
                    if (furniture.interactType == 4):
                        self.showFurnitureInteractAttachments()
                else:
                    ientity = self.model.model
                    ientity.Detach()
                    if ientity.Tach:
                        ientity.Tach.Hardpoint = ''
                        ientity.Tach.Basepoint = ''
                    self.showFurnitureInteractAttachments()
                if getattr(self, 'furnitureInteractGid', None):
                    self.model.PopGraph(self.furnitureInteractGid)
                    delattr(self, 'furnitureInteractGid')
                self.model.model.CharCtrl.Enable = True
                if (self.id != getattr(GlobalData.p, 'id', '')):
                    self.syncPosOn()

    def updateFurnitureInteract(self):
        fid = self.furnitureInteractId
        slots = GlobalData.p.currentHomestead.buildings.get(fid, {}).get('interactSlots', [])
        furniture = HomeBuildingManager().buildingMap.get(fid)
        if ((not slots) or (not furniture)):
            return
        else:
            for (i, eid) in enumerate(slots):
                if (eid == self.id):
                    furniture.enterFurenitureInteract(self, i)
                    break

    def onFurnitureInteractModelChange(self):
        (self.furnitureInteractId and self.updateFurnitureInteract())

    def getInteractFurniture(self):
        return HomeBuildingManager().buildingMap.get(self.furnitureInteractId)

    def showFurnitureInteractAttachments(self):
        model = self.model
        names = ('LeftHandWeapon', 'RightHandWeapon', 'ExtraModel', 'ExtraModel1', 'CloakModel', 'EquipHalo')
        for name in names:
            model.HideAttachment(name, 0, sourceid=cconst.HIDE_ATTCH_TYPE_FURNITURE)

    def hideFurnitureInteractAttachments(self):
        model = self.model
        names = ('LeftHandWeapon', 'RightHandWeapon', 'ExtraModel', 'ExtraModel1', 'CloakModel', 'EquipHalo')
        for name in names:
            model.HideAttachment(name, (-1), sourceid=cconst.HIDE_ATTCH_TYPE_FURNITURE)

    @property
    def isFurnitureInteracting(self):
        return self.furnitureInteractId

    def onLeaveFurnitureInteract(self, fid):
        self.topLogo.UpdateHeight(self)

    def onEnterFurnitureInteract(self, fid):
        self.topLogo.UpdateHeight(self)

    def _on_set_furnitureInteractId(self, old):
        if (old and (not self.furnitureInteractId)):
            furniture = HomeBuildingManager().buildingMap.get(old)
            if (self.model.model and self.model.model.IsValid()):
                if furniture:
                    furniture.leaveInteract(self.model.model, self.id)
                    self.onLeaveFurnitureInteract(old)
                    if (furniture.interactType == 4):
                        self.showFurnitureInteractAttachments()
                else:
                    ientity = self.model.model
                    ientity.Detach()
                    if ientity.Tach:
                        ientity.Tach.Hardpoint = ''
                        ientity.Tach.Basepoint = ''
                    self.showFurnitureInteractAttachments()
                if getattr(self, 'furnitureInteractGid', None):
                    self.model.PopGraph(self.furnitureInteractGid)
                    delattr(self, 'furnitureInteractGid')
                self.model.model.CharCtrl.Enable = True
                if (self.id != getattr(GlobalData.p, 'id', '')):
                    self.syncPosOn()

    def updateFurnitureInteract(self):
        fid = self.furnitureInteractId
        slots = GlobalData.p.currentHomestead.buildings.get(fid, {}).get('interactSlots', [])
        furniture = HomeBuildingManager().buildingMap.get(fid)
        if ((not slots) or (not furniture)):
            return
        else:
            for (i, eid) in enumerate(slots):
                if (eid == self.id):
                    furniture.enterFurenitureInteract(self, i)
                    break

    def onFurnitureInteractModelChange(self):
        (self.furnitureInteractId and self.updateFurnitureInteract())

    def getInteractFurniture(self):
        return HomeBuildingManager().buildingMap.get(self.furnitureInteractId)

    def showFurnitureInteractAttachments(self):
        model = self.model
        names = ('LeftHandWeapon', 'RightHandWeapon', 'ExtraModel', 'ExtraModel1', 'CloakModel', 'EquipHalo')
        for name in names:
            model.HideAttachment(name, 0, sourceid=cconst.HIDE_ATTCH_TYPE_FURNITURE)

    def hideFurnitureInteractAttachments(self):
        model = self.model
        names = ('LeftHandWeapon', 'RightHandWeapon', 'ExtraModel', 'ExtraModel1', 'CloakModel', 'EquipHalo')
        for name in names:
            model.HideAttachment(name, (-1), sourceid=cconst.HIDE_ATTCH_TYPE_FURNITURE)

    @property
    def isFurnitureInteracting(self):
        return self.furnitureInteractId

    def onLeaveFurnitureInteract(self, fid):
        self.topLogo.UpdateHeight(self)

    def onEnterFurnitureInteract(self, fid):
        self.topLogo.UpdateHeight(self)

    def isInHatKingBattle(self):
        if (not getattr(self, 'spaceno', None)):
            return False
        inquiry = SpaceInquiry(self.spaceno)
        return (inquiry.type == SpaceType.HATKING_BATTLE)

    @rpc_method(CLIENT_STUB, Str())
    def onPlayerEffectInner(self, path):
        self.model.play_effect_inner(path)

    def _on_set_fakeData(self, old):
        self.playBianshenEffect()
        model = self.model
        model.Reload(self.getModelData())
        self.refreshEquipHalo()
        self.refreshTitleSFX()
        (getattr(self, 'topLogo', None) and self.topLogo.UpdateToplogo(self))
        combatPokemon = self.getCombatPokemon()
        (combatPokemon and getattr(combatPokemon, 'topLogo', None) and combatPokemon.topLogo.UpdateToplogo(combatPokemon))

    def playBianshenEffect(self):
        dataGetter = chrismas_magicwand_data.data.values()[0].get
        sfxID = dataGetter('sfxID', None)
        if (not sfxID):
            return
        sfx = hardcode_resource_data.data.get(sfxID, {}).get('path', '')
        MCharacter.PlayEffectInWorld(sfx, MType.Vector3(*self.position), 5)

    @property
    def isFaking(self):
        return bool((self.fakeData.id and (self.fakeData.timeout >= time.time())))

    @property
    def eqSchool(self):
        return (self.fakeData.school if self.isFaking else self.school)

    @property
    def eqBody(self):
        return (self.fakeData.body if self.isFaking else self.body)

    @property
    def eqName(self):
        return (self.fakeData.name if self.isFaking else self.name)

    @property
    def eqLv(self):
        return (self.fakeData.lv if self.isFaking else self.lv)

    @property
    def isGetPhotoBoardItemToday(self):
        itemNo = PhotoBoardConst.getItemByTheme(PhotoBoardConst.realCurrentTheme)
        if (itemNo not in self.photoBoardItems):
            return True
        return False

    @rpc_method(CLIENT_STUB, Dict())
    def onUpgradePhotoBoardPhotoLevel(self, record):
        if record:
            ((not PhotoBoardWidget.isHide()) and PhotoBoardWidget().onUpgradePhotoBoardPhotoLevel(record))
            return
        else:
            self.popNotificationMsg('\xe5\x8d\x87\xe7\xba\xa7\xe5\xa4\xb1\xe8\xb4\xa5')

    @rpc_method(CLIENT_STUB, Int(), Dict())
    def onUpdatePhotoDesc(self, result, record):
        if (result == PhotoBoardError.SUCCESS):
            ((not PhotoBoardWidget.isHide()) and PhotoBoardWidget().onUpdatePhotoDesc(record))
        else:
            self.popNotificationMsg('\xe6\x9a\x82\xe6\x97\xb6\xe6\x97\xa0\xe6\xb3\x95\xe6\x89\xa7\xe8\xa1\x8c\xe6\xad\xa4\xe6\x93\x8d\xe4\xbd\x9c')

    @rpc_method(CLIENT_STUB, Dict())
    def onAddPhotoBoardPhotoLike(self, record):
        if record:
            self.popNotificationMsg('\xe7\x82\xb9\xe8\xb5\x9e\xe6\x88\x90\xe5\x8a\x9f')
            ((not PhotoBoardWidget.isHide()) and PhotoBoardWidget().updateRecord(record))
        else:
            self.popNotificationMsg('\xe5\xb7\xb2\xe7\xbb\x8f\xe4\xb8\xba\xe8\xaf\xa5\xe7\x85\xa7\xe7\x89\x87\xe7\x82\xb9\xe8\xbf\x87\xe8\xb5\x9e\xe4\xba\x86')

    @rpc_method(CLIENT_STUB, List(), Int())
    def onPhotoBoardQuery(self, records, page):
        ((not PhotoBoardWidget.isHide()) and PhotoBoardWidget().onPhotoBoardQuery(records, page))

    @rpc_method(CLIENT_STUB, Dict(), Dict())
    def onQuerySomeoneRank(self, photoInfo, avatarInfo):
        ((not PhotoBoardWidget.isHide()) and PhotoBoardWidget().onQuerySomeoneRank(photoInfo, avatarInfo))

    @rpc_method(CLIENT_STUB, List(), Int())
    def onQueryPhotoBoardComment(self, comments, page):
        '\n\t\t\xe8\xb7\xb3\xe8\xbd\xac\xe5\x88\xb0\xe7\x95\x8c\xe9\x9d\xa2\xe8\xbf\x9b\xe8\xa1\x8c\xe5\xbc\xb9\xe5\xb9\x95\xe6\x92\xad\xe6\x94\xbe\n\t\t'
        ((not PhotoBoardWidget.isHide()) and PhotoBoardWidget().onQueryPhotoBoardComment(comments, page))

    def setPhotoBoardPhotoLevel(self, itemno, level, pid, desc=''):
        '\n\t\t\xe5\x9b\xbe\xe7\x89\x87\xe4\xb8\x8a\xe7\x85\xa7\xe7\x89\x87\xe5\xa2\x99\n\t\t'
        theme = PhotoBoardConst.getThemeByItemNo(itemno)
        (theme and self.server.setPhotoBoardPhotoLevel(itemno, level, pid, theme, desc))

    def oneKeyCallPhotoBoard(self, channel, theme=1, level=1):
        '\n\t\t'
        hlc = HyperLinkCreator
        _hlc = hlc.createPhotoBoard(theme, level, self.id)
        content = ('%s\xe7\xbb\x99\xe6\x82\xa8\xe5\x88\x86\xe4\xba\xab\xe4\xba\x86\xe5\x9c\xa8\xe4\xb8\xbb\xe9\xa2\x98#O%s#E\xe4\xb8\xad\xe7\x9a\x84\xe4\xbd\x9c\xe5\x93\x81#G' % (self.name, PhotoBoardConst.getThemeName(theme)))
        text = (content + _hlc)
        succ = True
        if (channel == ChannelType.WORLD):
            succ = self.sendTextToChannel(ChannelType.WORLD, text, {MsgField.ONE_KEY_CALL: False})
        elif (channel == ChannelType.CLAN):
            if self.isInClan:
                succ = self.sendTextToChannel(ChannelType.CLAN, text, {MsgField.ONE_KEY_CALL: False})
            else:
                self.popNotificationMsg('\xe8\xaf\xb7\xe5\x85\x88\xe5\x8a\xa0\xe5\x85\xa5\xe5\x8a\xbf\xe5\x8a\x9b')
                return
        elif (channel == ChannelType.SCHOOL):
            succ = self.sendTextToChannel(ChannelType.SCHOOL, text, {MsgField.ONE_KEY_CALL: False})
        elif (channel == ChannelType.CURRENT):
            succ = self.sendTextToChannel(ChannelType.CURRENT, text, {MsgField.ONE_KEY_CALL: False})
        if succ:
            self.popNotificationMsg('\xe6\x82\xa8\xe7\x9a\x84\xe5\x96\x8a\xe8\xaf\x9d\xe5\xb7\xb2\xe5\x8f\x91\xe9\x80\x81\xef\xbc\x8c\xe8\xaf\xb7\xe8\x80\x90\xe5\xbf\x83\xe7\xad\x89\xe5\xbe\x85')
        else:
            self.popLastSendFailReasonMsg()

    def showThemeLevelPhoto(self, aid, theme, level):
        '\n\t\t\xe7\x82\xb9\xe5\x87\xbb\xe8\xb6\x85\xe9\x93\xbe\xe6\x8e\xa5\xe4\xb9\x8b\xe5\x90\x8e\xe6\x9f\xa5\xe8\xaf\xa2\xe6\x9f\x90\xe4\xb8\xaa\xe7\x8e\xa9\xe5\xae\xb6\xe7\x9a\x84\xe7\x85\xa7\xe7\x89\x87\xe4\xbf\xa1\xe6\x81\xaf\n\t\t'
        pass

    @rpc_method(CLIENT_STUB, Dict())
    def onAddPhotoBoardPhotoCommentCount(self, record):
        ((not PhotoBoardWidget.isHide()) and PhotoBoardWidget().onAddPhotoBoardPhotoCommentCount(record))

    @rpc_method(CLIENT_STUB, Dict())
    def onGetOtherAvatarInfo(self, details):
        ((not PhotoBoardWidget.isHide()) and PhotoBoardWidget().onGetOtherAvatarInfo(details))

    def getOtherAvatarInfo(self, aid):
        (aid and self.server.getOtherAvatarInfo(aid, ('name', 'school', 'body')))

    def _on_set_isInSendingRose(self, old):
        if (not hasattr(self, 'sendRoseGraphId')):
            self.sendRoseGraphId = None
        if self.isInSendingRose:
            self.sendingRoseStart()
        else:
            self.sendingRoseEnd()

    def _on_set_isInShowRose(self, old):
        if (not hasattr(self, 'showRoseGraphId')):
            self.showRoseGraphId = None
        if self.isInShowRose:
            self.showValentineRoseStart()
        else:
            self.showValentineRoseEnd()

    def sendingRoseStart(self):
        print 'sendingRoseStart'
        if self.IsPlayerAvatar:
            GlobalData.F11_flag = 0
            GlobalData.playerMain.swithcHideOther(GlobalData.playerMain.hideother)
        entity = EntityManager.getentity(self.sendingRosePartnerId)
        if (not entity):
            return
        if (hasattr(self, 'sendRoseGraphId') and self.sendRoseGraphId):
            return
        self.hideAttachments(1)
        self.model.gotoLocomotion(0)
        self.model.leaveModelRiding()
        self.faceTo(entity.position)
        graph = VRGD.data.get(self.school, {}).get('graph', VConst.senderGraph)
        if (self.sendingRoseType == VConst.SendRoseType.SEND):
            self.model.attachItemModel(VConst.partName, VConst.attachItemId)
            self.sendRoseGraphId = self.model.PushGraph(graph, 0, 0)
            self.model.FireEvent(self.sendRoseGraphId, 'happy_flower')
        elif (self.sendingRoseType == VConst.SendRoseType.RECEIVE):
            self.sendRoseGraphId = self.model.PushGraph(graph, 0, 0)

    def sendingRoseEnd(self):
        print 'sendingRoseEnd'
        if (not (hasattr(self, 'sendRoseGraphId') and self.sendRoseGraphId)):
            return
        if self.IsPlayerAvatar:
            GlobalData.F11_flag = 1
            GlobalData.playerMain.swithcHideOther(GlobalData.playerMain.hideother)
        self.model.DelAttachment(VConst.partName)
        (self.sendRoseGraphId and self.model.PopGraph(self.sendRoseGraphId))
        self.model.gotoLocomotion(0)
        self.showAttachments(1)
        self.sendRoseGraphId = None

    def showValentineRoseStart(self):
        self.hideAttachments(1)
        self.model.gotoLocomotion(0)
        self.model.leaveModelRiding()
        graph = VRGD.data.get(self.school, {}).get('graph', VConst.senderGraph)
        self.model.attachItemModel(VConst.partName, VConst.attachItemId)
        self.showRoseGraphId = self.model.PushGraph(graph, 0, 0)
        self.model.FireEvent(self.showRoseGraphId, 'happy_flower')

    def showValentineRoseEnd(self):
        if (not (hasattr(self, 'showRoseGraphId') and self.showRoseGraphId)):
            return
        self.model.DelAttachment(VConst.partName)
        (self.showRoseGraphId and self.model.PopGraph(self.showRoseGraphId))
        self.model.gotoLocomotion(0)
        self.showAttachments(1)
        self.showRoseGraphId = None

    def _on_set_dTransformNo(self, old):
        if self.dTransformNo:
            mode = riding_data.data.get(self.transformRideNo, dict()).get('hideAttachments', 0)
            (mode and self.hideAttachments(mode))
        else:
            no = EAD.data.get(old, {}).get('relateRideNo', 0)
            mode = riding_data.data.get(no, dict()).get('hideAttachments', 0)
            (mode and self.showAttachments(mode))

    def _on_set_dTransformInfo(self, old):
        self.updateTransform()
        if self.dTransformInfo:
            mode = riding_data.data.get(self.transformRideNo, dict()).get('hideAttachments', 0)
            (mode and self.hideAttachments(mode))
        else:
            no = EAD.data.get((old[2] if old else 0), {}).get('relateRideNo', 0)
            mode = riding_data.data.get(no, dict()).get('hideAttachments', 0)
            (mode and self.showAttachments(mode))

    def tryUpdateTransform(self):
        if (not self.dTransformInfo):
            return
        (side, eid, _) = self.dTransformInfo
        other = getattr(self.space, 'entities', dict()).get(eid)
        if (other and other.model and other.model.isValid()):
            avt = (self if (side == const.DR_SIDE_ATTACH) else other)
            avt.updateTransform()
            mode = riding_data.data.get(avt.transformRideNo, dict()).get('hideAttachments', 0)
            (mode and avt.hideAttachments(mode))

    def updateTransform(self):
        playerMain = GlobalData.playerMain
        (playerMain and playerMain.UpdateAttackBtnIcon())
        if self.dTransformInfo:
            (side, eid, _) = self.dTransformInfo
            if (side == const.DR_SIDE_BASE):
                return self.lockTarget(None)
            else:
                master = getattr(self.space, 'entities', dict()).get(eid)
                if (not master):
                    return
                graph = riding_graph_data.data[(self.eqSchool, self.eqBody)]['graph']
                self.model.enterInviteRide(master, self.dTransformInfo[2], graph)
                ((self is GlobalData.p) and self.server.transformRideSyncPos(master.id))
        else:
            ((not self.dTransformNo) and self.model.leaveInviteRide())

    @property
    def isTransformAttach(self):
        return (self.dTransformInfo and (self.dTransformInfo[0] == const.DR_SIDE_ATTACH))

    @property
    def isTransformBase(self):
        return (self.dTransformInfo and (self.dTransformInfo[0] == const.DR_SIDE_BASE))

    @property
    def isTransform(self):
        if self.dTransformNo:
            return bool(self.transformRideNo)
        else:
            return bool(self.dTransformInfo)

    @property
    def canBeRide(self):
        return (('holdPoints' in EAD.data.get(self.dTransformNo, {})) if self.isTransform else False)

    @property
    def transformRideNo(self):
        if self.dTransformNo:
            no = self.dTransformNo
        elif self.dTransformInfo:
            no = self.dTransformInfo[2]
        else:
            no = 0
        return EAD.data.get(no, {}).get('relateRideNo', 0)

    @property
    def transformRelateRideNo(self):
        if self.transformRideNo:
            return self.transformRideNo
        elif self.transformExpressionNo:
            if self.d_ride_info:
                return 0
            else:
                return EAD.data.get(self.transformExpressionNo, {}).get('relateRideNo', 0)
        else:
            return 0

    def getCombatFollower(self):
        return EntityManager.getentity(self.combatFollowerId)

    def isInMorningExercise(self):
        return (self.space and (SpaceInquiry(self.spaceno).dungeonType == DungeonType.MORNING_EXERCISE))

    def _on_set_aprilFoolTrickyBoxEffectRefresh(self, old):
        for effectId in AFTBD.data['EffectIds']:
            self.playAprilFoolTrickyBoxEffect(effectId)

    def _on_set_aprilFoolTrickyBoxBuffEffect(self, old):
        self.playAprilFoolTrickyBoxBuffEffect()

    def playAprilFoolTrickyBoxEffect(self, effectId):
        if (not self.model.isValid()):
            return
        effectArgs = effectId.split(':')
        for (i, arg) in enumerate(effectArgs):
            if ((i > 3) and arg.startswith('p')):
                pos = map(float, arg[1:].split(','))
                effectArgs[i] = ('p' + ','.join((str(n) for n in pos)))
        effectArgs = ':'.join(effectArgs)
        self.model.do_cue_type_effect(effectArgs, initiative=True)

    def playAprilFoolTrickyBoxBuffEffect(self):
        sfx = hardcode_resource_data.data.get(91, {}).get('path', '')
        (sfx and MCharacter.PlayEffectInWorld(sfx, MType.Vector3(*self.position), 5))

    def throwGrenade(self, targetid, buff, itemid):
        self.model.FireEvent(0, '@throw')
        self.model.hideWeapons(2, cconst.HIDE_ATTCH_TYPE_GRENADE)
        traj = GrenadeTrajectory(GrenadeConst.traj(itemid), self.id, targetid, 1, buff, itemid)
        if (not getattr(self, 'trajectories', None)):
            self.trajectories = {}
        self.trajectories[traj.id] = traj

    @rpc_method(CLIENT_STUB, EntityID(), Int(), Int())
    def onThrowGrenade(self, targetid, buff, itemid):
        self.throwGrenade(targetid, buff, itemid)

    @rpc_method(CLIENT_STUB, Int())
    def onHitByGrenade(self, buff):
        effectPath = HRD.data.get(GrenadeQuery.hitEffect(buff, self.school, self.body), {}).get('path', '')
        self.model.play_effect_inner(effectPath)
        if (self == GlobalData.p):
            self.popNotificationMsg(GrenadeQuery.defendMessage(buff, self.school, self.body))

    def isInDreamSource(self):
        if (not getattr(self, 'spaceno', None)):
            return False
        inquiry = SpaceInquiry(self.spaceno)
        return (inquiry.type == SpaceType.DREAMSOURCE)

    def _host_init(self, bdict):
        self.__init_component__avatarmembers_impQuickConsume(bdict)

    def _host_post(self, bdict):
        self.__post_component__avatarmembers_impClan(bdict)
        self.__post_component__avatarmembers_impDress(bdict)

@with_tag('IsPlayerAvatar')
@Components(PlayerAvatarRoleComponent, *avatarmembers.importall())
class PlayerAvatar(Avatar, AvatarEntity, ):
    Property('account')
    Property('origin_account')
    Property('crossservering')
    Property('createroletime', 0, (Property.OWN_CLIENT | Property.PERSISTENT))

    def init_from_dict(self, bdict):
        GlobalData.p = self
        self.initEventNotifier()
        super(PlayerAvatar, self).init_from_dict(bdict)
        self.bad_network_timer = 0
        self.set_tick(const.TICK_TIME_HIGH_FREQUENCY)

    def finishLoginLoading(self):
        '\n\t\t\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf\xe5\xae\x8c\xe6\x88\x90\xe7\x99\xbb\xe5\xbd\x95\xe5\x90\x8e\xe7\x9a\x84loading\xe5\x90\x8e\xe5\xa4\x84\xe7\x90\x86\xe7\x9b\xb8\xe5\x85\xb3\xe4\xba\x8b\xe4\xbb\xb6\n\t\t'
        self.server.onAdventureClientLogined()
        self.unregisterLoadingListener('End', self.finishLoginLoading)

    @rpc_method(CLIENT_STUB)
    def become_player(self):
        self.logger.info('become_player %s(%s)', self.name, IdManager.id2str(self.id))
        self.registerLoadingListener('End', GeneralLog.GeneralLog().logLoad)
        self.registerLoadingListener('End', self.finishLoginLoading)
        (GlobalData.camera and GlobalData.camera.stopController())
        self.registerProduct()
        self.reviewCheckedOrders()
        LoadingDispacher.initCurDispatch()
        LoadingDispacher.LoadingShow()
        self.onStatusUpdate()
        self.updateTargetStatus()
        self.add_repeat_timer(3.3, self.ping)
        if GlobalData.roleCreating:
            self.uploadUserInfo(cconst.USERINFO_STAGE_CREATE_ROLE)
            GlobalData.roleCreating = False
            if (GlobalData.accountMgr.GetChannel() in ('huawei', 'ylwl')):
                self.uploadUserInfo(cconst.USERINFO_STAGE_ENTER_SERVER)
        else:
            self.uploadUserInfo(cconst.USERINFO_STAGE_ENTER_SERVER)
        self.setDumpInfo()
        MEngine.SetWindowTitle(('%s - %s' % (config.LocalConfig.LastServer.get(config.LocalConfig.Account, ''), self.name)))
        if self.is_dead:
            MRender.GrayToPercent(1, 1)
        self.updatePushRegid()
        self.update_graphic_level(config.LocalConfig.SystemSettings.get('AOIRange', const.GRAPHICS_LEVEL_HIGH))
        self.update_aoi_range(DS().getSettingDetail(DS.KEY_AOI_RANGE, (const.GRAPHICS_LEVEL_HIGH + 1)))
        self.refreshWindowTitle()
        self.checkNewPackage()
        self.saveGraphicLevel()
        if getattr(GlobalData, 'idle_timer', 0):
            Timer.ensure_cancel_timer(GlobalData.idle_timer)
        GlobalData.idle_timer = Timer.add_callback(30, True, utils.Functor(self.checkIdle))
        GlobalData.firstEnterSpace = True
        GlobalData.immediatelyShowHaibao = True
        GlobalData.serverNum = self.hostnum
        from GUI.GUIComponent import GUIComponentBase, clearUIRecord
        recordUILog = (GlobalData.serverNum == GlobalData.recordUIHostnum)
        if (recordUILog != GUIComponentBase.recordUILog):
            clearUIRecord()
        GUIComponentBase.recordUILog = recordUILog

    def checkIdle(self, timerid):
        ctime = time.time()
        lastUIDispatchTime = getattr(GlobalData, 'lastUIDispatchTime', 0)
        cur_pos = self.position
        if (formula.distance(getattr(self, 'lastIdlePos', (0, 0, 0)), cur_pos) < 0.1):
            if (not getattr(GlobalData, 'lastPositionTime', 0)):
                GlobalData.lastPositionTime = ctime
        else:
            GlobalData.lastPositionTime = 0
        self.lastIdlePos = cur_pos
        lastPositionTime = getattr(GlobalData, 'lastPositionTime', 0)
        if ((lastUIDispatchTime and ((ctime - lastUIDispatchTime) >= const.IDLE_TIME)) and (lastPositionTime and ((ctime - GlobalData.lastPositionTime) >= const.IDLE_TIME))):
            if (not getattr(GlobalData, 'idleflag', 0)):
                self.server.OnIDLE(1)
                self.checkTeamSingleTimer()
            GlobalData.idleflag = 1
        else:
            if getattr(GlobalData, 'idleflag', 0):
                self.server.OnIDLE(0)
                GlobalData.p.resetTeamSingleTimer()
            GlobalData.idleflag = 0

    @rpc_method(CLIENT_STUB, Str())
    def setAccountURS(self, account_urs):
        GlobalData.account_urs = account_urs

    @rpc_method(CLIENT_STUB, Str())
    def showLoginMessage(self, message):
        from GUI.TxmMessageBox import MessageBoxLogin
        MessageBoxLogin().show(message)

    def update_graphic_level(self, level):
        self.server.update_graphic_level(level)

    def update_aoi_range(self, aoiRange):
        self.server.update_aoi_range(aoiRange)

    def uploadUserInfo(self, stage=None):
        mgr = GlobalData.accountMgr
        if (not mgr):
            return
        (stage and mgr.SetPropStr(cconst.USERINFO_STAGE, stage))
        if (stage == cconst.USERINFO_STAGE_ENTER_SERVER):
            mgr.SetPropStr(cconst.USERINFO_DATATYPE, '1')
        elif (stage == cconst.USERINFO_STAGE_CREATE_ROLE):
            mgr.SetPropStr(cconst.USERINFO_DATATYPE, '2')
        mgr.SetPropStr(cconst.APP_NAME, '\xe5\xa4\xa9\xe4\xb8\x8b')
        mgr.SetPropStr(cconst.USERINFO_UID, str(self.uid))
        mgr.SetPropStr(cconst.USERINFO_HOSTID, str(GlobalData.serverNum))
        mgr.SetPropStr(cconst.USERINFO_HOSTNAME, GlobalData.serverName)
        print '------------------------ upload user info: uid', mgr.GetPropStr(cconst.USERINFO_UID)
        print '------------------------ upload user info: hostid', mgr.GetPropStr(cconst.USERINFO_HOSTID)
        print '------------------------ upload user info: hostname', mgr.GetPropStr(cconst.USERINFO_HOSTNAME)
        mgr.SetPropStr(cconst.USERINFO_REGION_ID, str(GlobalData.serverNum))
        mgr.SetPropStr(cconst.USERINFO_REGION, GlobalData.serverName)
        mgr.SetPropStr(cconst.USERINFO_NAME, self.name)
        mgr.SetPropStr(cconst.USERINFO_GRADE, str(self.lv))
        mgr.SetPropStr(cconst.USERINFO_MENPAIID, str(self.school))
        mgr.SetPropStr(cconst.USERINFO_MENPAINAME, school_data.data.get(self.school, {}).get('Name', ''))
        mgr.SetPropStr(cconst.USERINFO_GANDID, str(self.clanID))
        mgr.SetPropStr(cconst.USERINFO_GAND, self.clanName)
        if self.clanConstrs:
            mgr.SetPropStr(cconst.USERINFO_GAND_LEVEL, str(self.clanConstrs[0]))
        else:
            mgr.SetPropStr(cconst.USERINFO_GAND_LEVEL, '0')
        mgr.SetPropStr(cconst.USERINFO_GAND_LEADER, '0')
        mgr.SetPropStr(cconst.USERINFO_TYPEID, str(self.school))
        mgr.SetPropStr(cconst.USERINFO_TYPENAME, school_data.data.get(self.school, {}).get('Name', ''))
        mgr.SetPropStr(cconst.USERINFO_BALANCE, str(self.gold))
        mgr.SetPropStr(cconst.USERINFO_VIP, str(self.vip))
        mgr.SetPropStr(cconst.USERINFO_ORG, self.clanName)
        mgr.SetPropStr(cconst.USERINFO_ROLE_CTIME, str(self.createroletime))
        mgr.SetPropStr(cconst.USERINFO_ROLE_LEVELMTIME, str(self.levelmtime))
        mgr.SetPropStr(cconst.USERINFO_CAPABILITY, str(self.equipScore))
        mgr.SetPropStr(cconst.GAME_NAME, '\xe5\xa4\xa9\xe4\xb8\x8b')
        mgr.UploadUserInfo()

    def setDumpInfo(self):
        mgr = MDump.GetDumpManager()
        mgr.SetEntityParam('uid', self.id)
        mgr.SetEntityParam('username', self.name)

    @rpc_method(CLIENT_STUB)
    def clearSpace(self):
        self.space.clear()

    def destroy(self):
        MEngine.GetGameplay().Scenario.Move()
        if (GlobalData.p == self):
            GlobalData.p = None
        self.resetRender()
        if getattr(GlobalData, 'idle_timer', 0):
            Timer.ensure_cancel_timer(GlobalData.idle_timer)
        GlobalData.idle_timer = 0
        super(PlayerAvatar, self).destroy()

    def resetRender(self):
        MRender.GrayToPercent(0, 1)
        MRender.OldMovieToPercent(0, 1)
        MRender.SetScreenColor(0, 0, 0, 0, 1)

    def on_lose_server(self):
        super(PlayerAvatar, self).on_lose_server()
        self.server = NonexistentSwallower()

    def tick(self, dtime):
        self.tickPlayerForm(dtime)
        super(PlayerAvatar, self).tick(dtime)

    def enter_world(self, entity):
        super(PlayerAvatar, self).enter_world(entity)
        if entity.IsAvatar:
            entity.refreshTopLogo()

    def ping(self):
        if self.bad_network_timer:
            return
        self.server.ping()
        self.bad_network_timer = self.add_timer(3, self.on_bad_network)

    @rpc_method(CLIENT_STUB, Float())
    def pong(self, servertime):
        if self.bad_network_timer:
            self.cancel_timer(self.bad_network_timer)
            self.bad_network_timer = 0
        if PlayerMain.isInited():
            if PlayerMain().badNetwork:
                PlayerMain().badNetwork = False
                PlayerMain.setNetworkStatus()
        if (abs((servertime - time.time())) > 2.5):
            import PseudoTimer
            PseudoTimer.setTime(servertime)
            Crontab().resetTimer()
            self.server.getTimeDiff(time.time())
        callbackSet = getattr(self, 'pingCallback', None)
        if callbackSet:
            del self.pingCallback
            for cb in callbackSet:
                cb()

    def on_bad_network(self):
        if PlayerMain.isInited():
            if (not PlayerMain().badNetwork):
                PlayerMain().badNetwork = True
                PlayerMain.setNetworkStatus()
        self.bad_network_timer = 0

    @rpc_method(CLIENT_STUB)
    def on_be_relayed(self):
        txm.restart((lambda : MessageBox().show('\xe6\x82\xa8\xe7\x9a\x84\xe8\xb4\xa6\xe5\x8f\xb7\xe5\xb7\xb2\xe5\x9c\xa8\xe5\x85\xb6\xe5\xae\x83\xe8\xae\xbe\xe5\xa4\x87\xe7\x99\xbb\xe5\xbd\x95')))
        super(PlayerAvatar, self).on_be_relayed()

    @rpc_method(CLIENT_STUB, EntityID())
    def onReturnToAccount(self, accountid):
        import Timer
        Timer.cancel_all()
        from common.EntityManager import EntityManager
        import GlobalData
        if GlobalData.p:
            (getattr(GlobalData.p, 'space', None) and GlobalData.p.on_teleport_out(0))
            ((GlobalData.p.id != accountid) and GlobalData.p.destroy())
        while EntityManager._entities:
            try:
                (eid, entity) = EntityManager._entities.popitem()
                if (eid != accountid):
                    entity.destroy()
            except:
                pass
        if (GlobalData.p and (GlobalData.p.id != accountid)):
            EntityManager._entities[GlobalData.p.id] = GlobalData.p
        from UI.UIManager import UIManager
        UIManager()._showHierarchy = {}
        UIManager().clearComponents()
        from ChatCache import ChatCache, SpriteCache
        ChatCache().clear()
        SpriteCache().clear()
        from Space import SpaceLoader
        (SpaceLoader.isInited() and SpaceLoader().destroy())
        from HttpDownloader import HttpDownloader
        (HttpDownloader.isInited() and HttpDownloader().destroy())
        from AlbumMusicManager import AlbumMusicManager
        (AlbumMusicManager.isInited() and AlbumMusicManager().clear())
        GlobalData.p = None
        GlobalData.playerMain = None
        GlobalData.camera = None
        mgr = GlobalData.accountMgr
        if mgr:
            mgr.BindEvent('PaymentClosed', None)
            mgr.BindEvent('PaymentClosedWithDetail', None)
            mgr.BindEvent('FinishLogin', None)
            mgr.BindEvent('FinishLogout', None)
            mgr.BindEvent('FinishInit', None)
            mgr.BindEvent('ShareEnd', None)
            mgr.BindEvent('LoginDoneWithDetail', None)
        from common.Crontab import Crontab
        Crontab().init()
        import gc
        gc.collect()

    @rpc_method(CLIENT_STUB, Str())
    def onServerTraceback(self, content):
        self.logger.error('\n>>>>>>>>>> SERVER TRACEBACK >>>>>>>>>>\n%s\n>>>>>>>> SERVER TRACEBACK END >>>>>>>>', content)

    @rpc_method(CLIENT_STUB, Str(), BinData())
    def hotfix(self, md5='', content=''):
        from ShardDict import ShardDict
        import taggeddict
        from RecordDictManager import RecordDictManager
        try:
            config.LocalConfig.hotfixstr = content
            config.LocalConfig.hotfixmd5 = md5
        finally:
            if content:
                print ('Patching Hotfix %s' % md5)
                taggeddict.unlock_tagged_dict()
                ShardDict.LOCKDOWN = False
                RecordDictManager.LOCKDOWN = False
                exec content in {}
                ShardDict.LOCKDOWN = True
                taggeddict.lock_tagged_dict()
                RecordDictManager.LOCKDOWN = True
                print ('Hotfix Patched! %s' % md5)

    @rpc_method(CLIENT_STUB, BinData())
    def checkDesignFlag(self, md5):
        if (DesignFlags.flagsMD5 != md5):
            self.server.fetchDesignFlag()

    @rpc_method(CLIENT_STUB, Dict())
    def syncDesignFlag(self, flags):
        DesignFlags.setFlags(flags)

    @rpc_method(CLIENT_STUB)
    def onRelayLogin(self):
        GlobalData.immediatelyShowHaibao = False
        (self.isInTeam() and self._updateTeamInfo())
        PlayerMain().onPersonAutoMatching((self.intelligentMatch or self.playerAutoJoin))

    def heartBeat(self, userdata):
        if (not hasattr(self, 'heartbeating')):
            self.heartbeating = True
        import sys
        if ('PseudoTimer' in sys.modules):
            from PseudoTimer import RealTimer
            time = RealTimer.time
        else:
            from time import time
        self.server.heartBeat(userdata, time())

    @rpc_method(CLIENT_STUB, Str(), Float(), Float())
    def onHeartBeat(self, userdata, clientsent, serversent):
        import sys
        if ('PseudoTimer' in sys.modules):
            from PseudoTimer import RealTimer
            time = RealTimer.time
        else:
            from time import time
        self.server.onHeartBeat(userdata, clientsent, serversent, time())

    @rpc_method(CLIENT_STUB, Str(), Float(), Float(), Float(), Float())
    def onHeartBeated(self, userdata, clientsent, serversent, clientrecv, serverrecv):
        from time import gmtime, strftime

        def tf(t):
            return '.'.join((strftime('%H:%M:%S', gmtime(t)), ('%.2f' % (t - int(t)))[2:]))
        print ('onHeartBeat Client: %s -> %s Delay: %.2fms Server: %s -> %s Delay: %.2fms' % (tf(clientsent), tf(clientrecv), ((clientrecv - clientsent) * 1000), tf(serversent), tf(serverrecv), ((serverrecv - serversent) * 1000)))
        (getattr(self, 'heartbeating', False) and MEngine.AddCallback(1, self.heartBeat))

    @rpc_method(CLIENT_STUB)
    def triggerEvaluateStore(self):
        GeneralEvaluate().show()

    def onEnterSpaceSwimming(self, jump):
        '\n\t\t\xe8\xbf\x9b\xe5\x85\xa5\xe6\xb1\x9f\xe5\x8d\x97\xe6\xb0\xb4\xe5\x9f\x9f\xe5\x9c\xba\xe6\x99\xaf\xef\xbc\x8c\xe7\x8e\xa9\xe5\xae\xb6\xe8\xba\xab\xe4\xb8\x8a\xe5\xb8\xa6\xe4\xb8\x80\xe4\xb8\xaa\xe5\x8f\xaf\xe4\xbb\xa5\xe8\xb7\x9f\xe6\xb0\xb4\xe5\x8f\x91\xe7\x94\x9f\xe7\xa2\xb0\xe6\x92\x9eRigidBody\xef\xbc\x8c\xe8\xa6\x81\xe8\xae\xbe\xe7\xbd\xaeIsTrigger\xe4\xb8\xbaFalse\xef\xbc\x8c\xe5\x9b\xa0\xe4\xb8\xba\xe5\x9c\xba\xe6\x99\xaf\xe7\xbc\x96\xe8\xbe\x91\xe5\xb7\xb2\xe7\xbb\x8f\xe5\xb0\x86\xe6\xb0\xb4IsTrigger\xe8\xae\xbe\xe6\x88\x90True\xef\xbc\x8c\xe4\xb8\xa4\xe4\xb8\xaa\xe9\x83\xbdTrue\xe6\x97\xa0\xe6\xb3\x95\xe7\xa2\xb0\xe6\x92\x9e\xe5\x9b\x9e\xe8\xb0\x83\n\t\t:return:\n\t\t'
        print '!!!!!!!!!!!!!! onEnterSpaceSwimming', jump
        hasWater = False
        for name in cconst.WATER_BOJECTS:
            objects = MObject.FindObjectByName(name)
            if (not objects):
                continue
            for o in objects:
                for r in o.RigidBodies:
                    r.BindEvent('Triggered', (lambda triggerInfo: self.onTriggerSwimming(triggerInfo)))
                    hasWater = True
        if (not hasWater):
            (self.is_swimming and self.server.setSwimmingState(0))
            return
        if (getattr(self, 'swimmingSphereId', None) is not None):
            (self.model.model.IsValid() and MHelper.removeRigidBodyComponent(self.model.model, self.swimmingSphereId))
            del self.swimmingSphereId
        tid = MHelper.addMovingSphereTrigger(0.1, self.model.model, (lambda *args: None))
        trigger = self.model.model.RigidBodies[tid]
        self.swimmingSphereId = tid
        if trigger:
            trigger.IsTrigger = False
            trigger.CollisionFilterInfo = cconst.PHYSICS_MUL_WATER
            t = trigger.OffsetTransform
            t.translation = MType.Vector3(0, cconst.SWIMMING_HEIGHT, 0)
            trigger.OffsetTransform = t

    def onLeaveSpaceSwimming(self, jump):
        '\n\t\t\xe7\xa6\xbb\xe5\xbc\x80\xe6\xb1\x9f\xe5\x8d\x97\xe6\xb0\xb4\xe5\x9f\x9f\xef\xbc\x8c\xe8\xa7\xa3\xe9\x99\xa4\xe7\xa2\xb0\xe6\x92\x9e\xe5\x9b\x9e\xe8\xb0\x83\xef\xbc\x8c\xe5\x88\xa0\xe9\x99\xa4\xe7\x8e\xa9\xe5\xae\xb6\xe8\xba\xab\xe4\xb8\x8a\xe7\x9a\x84\xe7\xa2\xb0\xe6\x92\x9e\xe4\xbd\x93\n\t\t:return:\n\t\t'
        if jump:
            hasWater = False
            for name in cconst.WATER_BOJECTS:
                objects = MObject.FindObjectByName(name)
                if (not objects):
                    continue
                for o in objects:
                    for r in o.RigidBodies:
                        r.BindEvent('Triggered', None)
                        hasWater = True
            if hasWater:
                (self.is_swimming and self.server.setSwimmingState(0))
        if (getattr(self, 'swimmingSphereId', None) is not None):
            (self.model.model.IsValid() and MHelper.removeRigidBodyComponent(self.model.model, self.swimmingSphereId))
            del self.swimmingSphereId
        (self.is_swimming and self.server.setSwimmingState(0))

    def onTriggerSwimming(self, triggerInfo):
        print '!!!!!!!!!!!!!! onTriggerSwimming', triggerInfo.Flag, triggerInfo.Body.CollisionFilterInfo, (triggerInfo.Body.Parent == self.model.model)
        if (triggerInfo.Body.Parent != self.model.model):
            return
        if (triggerInfo.Flag == cconst.PHYSICS_TRIGGER_ENTER):
            self.server.setSwimmingState(1)
        elif (triggerInfo.Flag == cconst.PHYSICS_TRIGGER_LEAVE):
            self.server.setSwimmingState(0)

    def tryKillProcess(self, info):
        return
        import os
        infos = info.split(';')
        count = len([i for i in infos if (i.find('tianxia.exe') > (-1))])
        if (count > 10):
            self.server.logMultiProcessKill(info)
            os._exit(1)

    def getRunningProcessCallback(self, info):
        if info:
            self.server.logClientpPocessInfo(info, '')
            self.tryKillProcess(info)

    def GetPhyDriveSerial(self, info):
        if (not info):
            info = MConfig.Platform
        if (info and (not self.is_destroyed())):
            self.server.logClientpPocessInfo('', info)

    @rpc_method(CLIENT_STUB)
    def tryLogClientpPocessInfo(self):
        import MPlatform
        import MConfig
        try:
            MPlatform.GetRunningProcess(self.getRunningProcessCallback)
            MPlatform.GetPhyDriveSerial(self.GetPhyDriveSerial)
        except:
            try:
                res = MPlatform.GetRunningProcess()
            except:
                res = ''
            if (hasattr(MPlatform, 'GetPhyDriveSerial') and bconst.isDesktopPlatform()):
                driverSerial = MPlatform.GetPhyDriveSerial()
            else:
                driverSerial = MConfig.Platform
            ((res or driverSerial) and self.server.logClientpPocessInfo(res, driverSerial))
            self.tryKillProcess(res)

    @delay_call(5)
    def saveGraphicLevel(self):
        self.server.saveGraphicLevel(config.LocalConfig.SystemSettings['GraphicLevel'])

    def _on_set_crossservering(self, old):
        self.updateBloodBar()
        self.refreshWindowTitle()
        if PlayerMain.isInited():
            PlayerMain.setNetworkStatus()

    @rpc_method(CLIENT_STUB, List())
    def onRelayLoginRetryEvent(self, retryEvents):
        if getattr(self, 'isPosReady', False):
            for eventno in retryEvents:
                self.space.triggerEvent(self, eventno)
            return
        self.add_timer(0, (lambda : self.onRelayLoginRetryEvent(retryEvents)))

    def refreshWindowTitle(self):
        if self.crossservering:
            MEngine.SetWindowTitle('\xe8\xb7\xa8\xe6\x9c\x8d')
        else:
            MEngine.SetWindowTitle(('%s - %s' % (config.LocalConfig.LastServer.get(config.LocalConfig.Account, ''), self.name)))
            MEngine.SetWindowTitle(('%s - r%d/%d/%d' % (config.LocalConfig.LastServer.get(config.LocalConfig.Account, ''), const.REVISION_ARTWORK, const.REVISION_ENGINE, const.REVISION_SCRIPT)))

    @rpc_method(CLIENT_STUB, Bool())
    def checkAccountBinding(self, is_guest):
        if bconst.isDesktopPlatform():
            GlobalData.guestLogin = is_guest
        else:
            GlobalData.guestLogin = (GlobalData.accountMgr.GetAuthTypeName() == 'guest')
        if GlobalData.guestLogin:
            from GUI.MainMenuBar import MainMenuBar
            MainMenuBar().updateMainMenuNotify(MainMenuBar.SYSTEM_BTN_IDX, True)
PlayerAvatar.ActivityActions = {ActivityConst.ID_SHARE: PlayerAvatar.actionShare, ActivityConst.ID_GORUP_SPHERE: PlayerAvatar.actionGroupSphere, ActivityConst.ID_SUPPLY: PlayerAvatar.actionSupply, ActivityConst.ID_CROSS_ARENA: PlayerAvatar.actionCrossArena, ActivityConst.ID_CROSS_WAR: PlayerAvatar.actionCrossWar, ActivityConst.ID_CANVASS: PlayerAvatar.actionCanvass, ActivityConst.ID_GUESS_ARENA: PlayerAvatar.actionGuessArena, ActivityConst.ID_GUESS_WAR: PlayerAvatar.actionGuessWar, ActivityConst.ID_BOUNTY_TASK: PlayerAvatar.actionBountyTask, ActivityConst.ID_CJ_CATCH_GOLD: PlayerAvatar.actionCJCatchGold, ActivityConst.ID_CJ_EVOLUTION: PlayerAvatar.actionCJEvolution, ActivityConst.ID_CJ_SUPPERZZLE: PlayerAvatar.actionCJSupperzzle, ActivityConst.ID_TIME_MACHINE: PlayerAvatar.actionShareTimeMachine, ActivityConst.ID_SCHOOLMATE_ARENA: PlayerAvatar.actionSchoolmateArena, ActivityConst.ID_SCHOOLMATE_ARENA_TEMP: PlayerAvatar.actionSchoolmateArena, ActivityConst.ID_POETRY_COMPETITION: PlayerAvatar.actionPoetryCompetition, ActivityConst.ID_ROSE_RANK: PlayerAvatar.actionRoseRank, ActivityConst.ID_ADVENTURE_HOUSE: PlayerAvatar.actionAdventureHouse, ActivityConst.ID_PAPER_PLANE: PlayerAvatar.actionPaperPlane, ActivityConst.ID_GROUP_JZ: PlayerAvatar.actionGroupJZ, ActivityConst.ID_HUAHAO: PlayerAvatar.actionHuaHao, ActivityConst.ID_SAINTSDAY: PlayerAvatar.actionSaintsDay, ActivityConst.ID_PUMPKIN_MALL: PlayerAvatar.actionPumpkinMallShow, ActivityConst.ID_YUEYUAN: PlayerAvatar.actionYueYuan, ActivityConst.ID_LUCKYSTAR: PlayerAvatar.actionLuckyStar, ActivityConst.ID_SNOWMAN: PlayerAvatar.actionSnowman, ActivityConst.ID_FURNITURE_SHARE: PlayerAvatar.actionFurnitureShare, ActivityConst.ID_HOMESTEAD: PlayerAvatar.actionHomestead, ActivityConst.ID_MILLION_ANSWER: PlayerAvatar.actionMillionAnswer, ActivityConst.ID_SKIP_CLASS: PlayerAvatar.actionSkipClass, ActivityConst.ID_HOMEWORK: PlayerAvatar.actionHomework, ActivityConst.ID_APRIL_FOOL_BOX: PlayerAvatar.actionAprilFoolBox, ActivityConst.ID_SAKURA_NPC_REMAIN_TEXT: PlayerAvatar.actionSakuraNpcRemainText, ActivityConst.ID_SHOW_APPEARANCE_DYE: PlayerAvatar.actionShowAppearanceDye}
PlayerAvatar.ActivityPushActions = {ActivityConst.ID_EXAM_TRICKY: PlayerAvatar.pushActionExamination}
PlayerAvatar.CarrierInteractActions = {CarrierInteractType.DYE: PlayerAvatar.changeCarrierDye, CarrierInteractType.EVENT: PlayerAvatar.fireCarrierInteractEvent, CarrierInteractType.SWITCH: PlayerAvatar.switchRideModel}
PlayerAvatar.HomeBuildingChangeHandleMap = {HomesteadConst.InteractSlots: PlayerAvatar.on_homestread_interactSlots_change, HomesteadConst.BUILDING_ATTR_VISIBLE: PlayerAvatar.onBuildingAttrVisibleChanged, HomesteadConst.Locked: PlayerAvatar.onBuildingLockStateChanged}
