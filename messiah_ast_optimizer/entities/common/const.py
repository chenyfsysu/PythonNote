# -*- coding: utf-8 -*-

import re

from data import refresh_data
from data import item_data


MAX_ACCOUNT_AVATARS = 10

# 性别
GENDER_UNKNOWN = 0
GENDER_MALE = 1
GENDER_FEMALE = 2
VALID_GENDERS = (GENDER_MALE, GENDER_FEMALE)

try:
	import revision
	REVISION_ARTWORK = revision.REVISION_ARTWORK
	REVISION_ENGINE = revision.REVISION_ENGINE
	REVISION_SCRIPT = revision.REVISION_SCRIPT
except:
	REVISION_ARTWORK = 0
	REVISION_ENGINE = 0
	REVISION_SCRIPT = 0

try:
	REVISION_SHADER = revision.REVISION_SHADER
except:
	REVISION_SHADER = 0


# 门派ID
SCHOOL_ID_HH = 1  # 荒火
SCHOOL_ID_TJ = 2  # 天机
SCHOOL_ID_LY = 3  # 翎羽
SCHOOL_ID_WL = 4  # 魍魉
SCHOOL_ID_TX = 5  # 太虚
SCHOOL_ID_YL = 6  # 云麓
SCHOOL_ID_BX = 7  # 冰心
SCHOOL_ID_YJ = 8  # 弈剑

SCHOOL_ID_LZL = 100  # 乐正绫与洛天依

EXIST_SCHOOLS = [
	SCHOOL_ID_TJ,
	SCHOOL_ID_YL,
	SCHOOL_ID_BX,
	SCHOOL_ID_YJ,
	SCHOOL_ID_TX,
	SCHOOL_ID_WL,
]

ROBOT_SCHOOLS = [
	SCHOOL_ID_TJ,
	SCHOOL_ID_YL,
	SCHOOL_ID_BX,
	SCHOOL_ID_YJ,
]

SCHOOLS = frozenset([SCHOOL_ID_HH, SCHOOL_ID_TJ, SCHOOL_ID_LY, SCHOOL_ID_WL, SCHOOL_ID_TX, SCHOOL_ID_YL, SCHOOL_ID_BX, SCHOOL_ID_YJ, ])

SMALL_BODY_CHAR = [(SCHOOL_ID_TX, 1), (SCHOOL_ID_BX, 0)]  # 小体型角色

PERMIT_SERVERS = frozenset([])
PERMIT_SCHOOLS = frozenset([])
SERVER_PERMITS = frozenset([])

SCHOOL_NAMES = {
	SCHOOL_ID_HH: {'brief': '荒火', 'name': '荒火教', 'abbreviation': 'hh', 'BodyAbbreviation': {0: 'hh', }, 'choosename': {0: '荒火教'}},
	SCHOOL_ID_TJ: {'brief': '天机', 'name': '天机营', 'abbreviation': 'tj', 'BodyAbbreviation': {0: 'tj', }, 'choosename': {0: '天机营'}},
	SCHOOL_ID_LY: {'brief': '翎羽', 'name': '翎羽山庄', 'abbreviation': 'ly', 'BodyAbbreviation': {0: 'ly', }, 'choosename': {0: '翎羽山庄'}},
	SCHOOL_ID_WL: {'brief': '魍魉', 'name': '魍魉', 'abbreviation': 'wl', 'BodyAbbreviation': {0: 'wl', }, 'choosename': {0: '魍魉'}},
	SCHOOL_ID_TX: {'brief': '太虚', 'name': '太虚观', 'abbreviation': 'tx', 'BodyAbbreviation': {0: 'tx', 1: 'xtx'}, 'choosename': {0: '太虚观(男)', 1: '太虚观(正太)'}},
	SCHOOL_ID_YL: {'brief': '云麓', 'name': '云麓仙居', 'abbreviation': 'yl', 'BodyAbbreviation': {0: 'yl', }, 'choosename': {0: '云麓仙居'}},
	SCHOOL_ID_BX: {'brief': '冰心', 'name': '冰心堂', 'abbreviation': 'bx', 'BodyAbbreviation': {0: 'bx', }, 'choosename': {0: '冰心堂'}},
	SCHOOL_ID_YJ: {'brief': '弈剑', 'name': '弈剑听雨阁', 'abbreviation': 'yj', 'BodyAbbreviation': {0: 'yj', }, 'choosename': {0: '弈剑听雨阁'}},
}

EQUIP_SCHOOL_NAMES = {
	SCHOOL_ID_LZL: {'abbreviation': 'lzl', 'BodyAbbreviation': {0: 'lzl', }},
}

SCHOOL_CHOOSE_BODY = {
	SCHOOL_ID_HH: (0, ),
	SCHOOL_ID_TJ: (0, ),
	SCHOOL_ID_LY: (0, ),
	SCHOOL_ID_WL: (0, ),
	SCHOOL_ID_TX: (0, 1, ),
	SCHOOL_ID_YL: (0, ),
	SCHOOL_ID_BX: (0, ),
	SCHOOL_ID_YJ: (0, ),
}

SCHOOL_GENDERS = {
	SCHOOL_ID_YL: GENDER_FEMALE,
	SCHOOL_ID_TJ: GENDER_MALE,
	SCHOOL_ID_BX: GENDER_FEMALE,
	SCHOOL_ID_YJ: GENDER_MALE,
	SCHOOL_ID_TX: GENDER_MALE,
	SCHOOL_ID_WL: GENDER_FEMALE,
}

EQU_PART_NECKLACE = 0		# 项链
EQU_PART_RING = 1			# 戒指
EQU_PART_JADE = 2			# 玉佩
EQU_PART_WEAPON = 3			# 武器
EQU_PART_ARM = 4			# 副手

EQU_PART_HEAD = 5			# 帽子
EQU_PART_SHOULDER = 6		# 肩膀
EQU_PART_SUIT = 7			# 衣服
EQU_PART_PANTS = 8			# 裤子
EQU_PART_BOOTS = 9			# 靴子

EQU_PART_CLOAK = 10         # 披风

EFFECT_WING_EQUIP_NUMBER = 10

EQU_BODYPARTS = frozenset([
	EQU_PART_WEAPON,
	EQU_PART_ARM,
	EQU_PART_HEAD,
	EQU_PART_SHOULDER,
	EQU_PART_SUIT,
	EQU_PART_PANTS,
	EQU_PART_BOOTS,
	EQU_PART_JADE,
	EQU_PART_NECKLACE,
	EQU_PART_RING,
	EQU_PART_CLOAK,
])

EQU_PART_DESC = {
	EQU_PART_NECKLACE: "项链",
	EQU_PART_RING: "戒指",
	EQU_PART_JADE: "玉佩",
	EQU_PART_WEAPON: "武器",
	EQU_PART_ARM: "副手",
	EQU_PART_HEAD: "帽子",
	EQU_PART_SHOULDER: "肩膀",
	EQU_PART_SUIT: "衣服",
	EQU_PART_PANTS: "裤子",
	EQU_PART_BOOTS: "靴子",
	EQU_PART_CLOAK: "披风",
}

# 新建角色进入地图
NEWBIE_SPACE_NO = 100
TEAM_NEWBEE_SPACENO = 363

MAX_TEAM_MEMBERS = 5

# 攻击结果类型
ATTCK_T_NORMAL = 0  # 攻击
ATTCK_T_DODGE = 1  # 闪避
ATTCK_T_BLOCK = 2  # 挡格
ATTCK_T_WSTAND = 3  # 招架
ATTCK_T_HEAL = 4  # 治疗
ATTCK_T_RELIVE = 5  # 复活

ATTCK_T_MSG = {
	ATTCK_T_NORMAL: 'hit!',
	ATTCK_T_DODGE: 'dodge!',
	ATTCK_T_BLOCK: 'block!',
	ATTCK_T_WSTAND: 'withstand!',
}

# 攻击关系
RELATION_ENEMY = 1  # 敌对
RELATION_COMRADE = 2  # 同盟
RELATION_IGNORE = 3  # 忽略

# 地图集群关系
SPACE_TROOP_FREE = 0  # 无
SPACE_TROOP_RED = 1  # 红方
SPACE_TROOP_BLUE = 2  # 蓝方

PLAYER_SPEED = 3.73 * 2 * 0.8
MONSTER_SPPED = 3.73 * 2 * 0.7
MOVE_SPEED = 3.73 * 2
PLAYER_SPEED_UPPER_LIMIT = 7.15  # 武老师钦定

USE_SKILL = "@use_skill_%d"
CANCEL_SKILL = "@cancel_skill_%d"

# SKILL TYPE
SKILL_TYPE_PHYSIC = 1
SKILL_TYPE_MAGIC = 2
SKILL_TYPE_HEAL = 3
SKILL_TYPE_BUFF = 4

# SKILL TARGET CAMP
TGT_CAMP_ENEMY = 1
TGT_CAMP_FRIEND = 2
TGT_CAMP_FRIEND_NOTME = 3
TGT_CAMP_ALL = 4

# SKILL TARGET TYPE
TGT_TYPE_COMBATUNIT = 1
TGT_TYPE_DEADBODY = 2
TGT_TYPE_BUILDING = 3
TGT_TYPE_POSITION = 4
TGT_TYPE_MONSTER = 5

# SKILL AFFECT TARGET CAMP
AFE_TGT_CAMP_ENEMY = 1
AFE_TGT_CAMP_FRIEND = 2
AFE_TGT_CAMP_FRIEND_NOTME = 3
AFE_TGT_CAMP_ME = 4
AFE_TGT_CAMP_ALL = 5

# SKILL AFFECT TARGET TYPE 特效影响阵营
AFE_TGT_TYPE_COMBATUNIT = 1
AFE_TGT_TYPE_DEADBODY = 2
AFE_TGT_TYPE_BUILDING = 3
AFE_TGT_TYPE_POSITION = 4
AFE_TGT_TYPE_MONSTER = 5

# SKILL AFFECT TYPE
AFE_TGT_SELF = 1
AFT_TGT_POKEMON = 2
AFT_TGT_SELF_OWNER = 3
AFT_TGT_OWNER = 4

# SKILL AFFECT ZONE TYPE
AZ_POINT = 1
AZ_CIRCLE = 2
AZ_SQUARE = 3
AZ_CYLINDER = 4

# SKILL AFFECT ZONE CENTER
AZ_CENTER_ATTACKER = 1
AZ_CENTER_TARGETLOCK = 2


# SKILL ATTACK EFFECT TYPE
ATK_EFFECT_TGT_LMT = 101  # 限制目标个数
ATK_EFFECT_DEFROST = 103  # 解封
ATK_EFFECT_PPIERCE = 104  # 破甲
ATK_EFFECT_MPIERCE = 105  # 透魔
ATK_EFFECT_DEMAGIC = 106  # 消魔
ATK_EFFECT_SPRINT = 107  # 模拟法术场
ATK_EFFECT_WUXING = 108  # 五行消除
ATK_EFFECT_FEIYUNDUAN = 109  # 飞云断特殊结构
ATK_EFFECT_CHASE = 110  # 定向冲锋
ATK_EFFECT_FIRSTAID = 111  # 治疗范围X内生命值最小的N个单位
ATK_EFFECT_RAY = 113  # 射线技能
ATK_EFFECT_HEAL = 114  # 优先治疗 1距离 2玩家 3召唤兽
ATK_EFFECT_DRAG = 115  # 拉人技能
#  defined by programmers  #
ATK_EFFECT_FAN = 1000  # 扇形攻击

# skill action move type
SKILL_ACTION_MOVE_BLOCK = 1  # 不穿透
SKILL_ACTION_MOVE_PENETRATE = 2  # 穿透
SKILL_ACTION_MOVE_TARGET_POS = 3  # 目标点
SKILL_ACTION_MOVE_BACKWARD = 4  # 退后
# SKILL_ACTION_MOVE_BUFF = 5  # buff控制
SKILL_ACTION_MOVE_TARGET = 6  # 技能位移到指定目标


# 结束战斗时间
COMBAT_OVER_TIME_FAST = 5
COMBAT_OVER_TIME_SLOW = 30
PVP_COMBAT_OVER_TIME = 10

# 怪物默认视野触发半径
MONSTER_VIEW_ATK_RANGE = 15

# 怪物默认追踪半径
MONSTER_CHASE_RANGE = 45

# 怪物默认视野触发仇恨
VIEW_ATTACK_HATE = 30

# buff type
BUFF_TYPE_BENIGN = 1	  # 良性
BUFF_TYPE_MALIGNANT = 2	  # 不良
BUFF_TYPE_FORMATION = 3	  # 阵法
BUFF_TYPE_HIT = 4   # 特殊受击, 同时只能存在一个，无法被动清除
BUFF_TYPE_SPECIAL = 5	  # 特殊状态，不能被同编号替换, 无法被动清除
BUFF_TYPE_SCH_RESISTANCE = 6  # 受击时门派抵抗, 同时只能存在一个
BUFF_TYPE_SCH_REINFORCE = 7  # 攻击时门派加强, 同时只能存在一个
BUFF_TYPE_CAMP_CHANGE = 8  # 更改单位阵营状态, 同时只能存在一个
BUFF_TYPE_AFFECT_BUFF = 9  # 影响另一个buff，触发fire event
BUFF_TYPE_TRANSFORM_HARM = 10  # 转化伤害，同时只能存在一个
BUFF_TYPE_SPEED_LIMIT = 14  # 速度限制，同时只能存在一个
BUFF_TYPE_BASE_SPEED = 15  # 基础速度，同时只能存在一个
BUFF_TYPE_ATTR_SKILL = 16  # 装备特技状态
BUFF_TYPE_SHAPESHIFT = 17  # 变身, 同时只能存在一个
BUFF_TYPE_CD_COOLER = 18  # 减少指定技能cd，同时只能存在一个
BUFF_TYPE_RIDE_TRANSFORM = 19  # 变身坐骑状态

# buff effect
BUFF_EFFECT_POSITIVE = 1  # 正面
BUFF_EFFECT_NEGATIVE = 2  # 负面

# buff negative type
BUFF_NEG_TYPE_STATIC = 1  # 躯体类
BUFF_NEG_TYPE_MOTION = 2  # 行动类

# type 4,6,7,8
BUFF_STYPE_REPLACEABLE = 1   # 4,6,7,8 可替换
BUFF_STYPE_IRREPLACEABLE = 2  # 4,6,7,8 不可替换
BUFF_STYPE_PART_REPLACEABLE = 3  # 4 特殊阶段可被替换 @todo

# Buff target type
BUFF_TGT_TYPE_OWNER = 1
BUFF_TYT_TYPE_TARGET = 2
BUFF_TYT_TYPE_TARGETALL = 3
BUFF_TYT_TYPE_RANGEPOKEMON = 4

# skill failed code
SKILL_FAILED = 0  # 技能不可用
SKILL_OK = 1  # 技能可用
SKILL_NOT_FOUND = 2  # 技能不存在
SKILL_COOLDOWN = 3  # 技能cd中
SKILL_MP = 4  # 技能所需MP不足
SKILL_DISTANCE = 5  # 超出技能射程
SKILL_CCOOLDOWN = 6  # 技能公共cd中
SKILL_DISABLED = 7  # 技能被禁用
SKILL_NEEDTGT = 8  # 找不到目标
SKILL_SKILLMGR = 9  # 被skillmanager阻碍
SKILL_SPRINT = 10  # 技能辅助冲刺
SKILL_TARGETERR = 11  # 错误的目标
SKILL_STIFFED = 12  # 硬直状态下不允许使用技能
SKILL_NOAPPROACH = 13  # 不向目标靠近
SKILL_SELF_USE = 14  # 对自己使用技能
SKILL_ALIVE = 15  # 使用者死亡
SKILL_SMERR = 16  # 状态指令冲突阻碍
SKILL_STATEERR = 17  # 技能状态不合法
SKILL_REPICK_RANGE = 18  # 重新选择影响范围内的目标并趋近
SKILL_REPICK_SPRINT = 19  # 重新选择影响范围内的目标并冲刺
SKILL_REPICK_OK = 20  # 重新选择影响范围内的目标
SKILL_JUSTUSED = 21  # 原地施放
SKILL_SUBSTITUTE = 22  # 技能被替换
SKILL_ESPRINT_OK = 23  # 特效技能使用成功
SKILL_SP = 24  # 技能所需SP不足
SKILL_HITACTION = 25  # 受击状态
SKILL_TURNTO = 26  # 需要转向
SKILL_CHARGE_TIME = 27  # 蓄力时间不足
SKILL_BUFF_CONFLICT = 28  # buff冲突
SKILL_OBSTACLE = 29  # 障碍物阻挡
SKILL_ANTI_LOCK = 30  # 无法被锁定
SKILL_ENABLE = 31  # 技能未启用
SKILL_HP = 32  # 血量不符合要求
SKILL_BUFF_REQ = 33  # 目标状态不符合要求
SKILL_ONLY_GENERAL = 34  # 仅可施放普通攻击
SKILL_NOT_ENABLE = 35  # 技能未激活
SKILL_TARGET_PROTECT = 36  # 目标处于保护状态
SKILL_SNOWBALL = 37  # 技能所需雪球数不足
SKILL_NEED_REPLACEBUFF = 38  # 技能替换的buff不存在
SKILL_WAIT_INVISIBLE = 39  # 等待隐身模型替换后再使用技能
SKILL_CHOOSE_MODE_ERR = 40  # 选择模式错误

SKILL_USED_STATE = frozenset([SKILL_OK, SKILL_NOAPPROACH, SKILL_JUSTUSED, SKILL_ESPRINT_OK])

SKILL_ERR_MSG = {
	SKILL_DISTANCE: "超出技能射程",
	SKILL_MP: "技能所需技力不足",
	SKILL_NEEDTGT: "请指定攻击目标",
	SKILL_TARGETERR: "错误的目标",
	SKILL_CHARGE_TIME: "蓄力时间不足",
	SKILL_OBSTACLE: "障碍物阻挡",
	SKILL_HP: "血量不符合要求",
	SKILL_SP: "技能所需体力不足",
	SKILL_BUFF_REQ: "目标状态不符合要求",
	SKILL_TARGET_PROTECT: "目标处于保护状态",
	# SKILL_FAILED:			"技能不可用",
	# SKILL_NOT_FOUND:		"技能不存在",
	# SKILL_COOLDOWN:			"技能cd中",
	# SKILL_CCOOLDOWN:		"技能公共cd中",
	# SKILL_DISABLED:			"技能被禁用",
	# SKILL_SKILLMGR:			"被skillmanager阻碍",
	# SKILL_STIFFED:			"硬直状态下不允许使用技能",
	# SKILL_ALIVE:			"使用者死亡",
	# SKILL_SMERR:			"状态指令冲突阻碍",
	# SKILL_HITACTION:		"受击状态",
	# SKILL_TURNTO:			"需要转向",
	# SKILL_BUFF_CONFLICT:	"buff冲突",
	# SKILL_ANTI_LOCK:		"该目标目前无法被锁定",
	# SKILL_ENABLE:			"该技能无法使用",
}

# create on skill failed code
CREATE_S_FAILED = 0
CREATE_S_OK = 1
CREATE_S_NOT_FOUND = 2  # 技能不存在
CREATE_S_NOT_IMP = 3  # 创生类型未实现
CREATE_S_NEEDTGT = 4  # 需要目标
CREATE_SM_NO_FOUND = 5
CREATE_SM_NO_CENTER = 6
CREATE_SM_NO_MOVE = 7
CREATE_SM_NO_DATA = 8
CREATE_SM_NEEDPOS = 9  # 需要点选位置
CREATE_SM_NO_MISC = 10  # misc is None

# create type
CREATE_TYPE_MAGIC_FIELD = 1  # 法术场
CREATE_TYPE_TOTEM = 2  # 图腾
CREATE_TYPE_VIGOR = 3  # 气劲
CREATE_TYPE_FORMATION = 4  # 阵型

# magic field center type
MAGIC_CTYPE_SELF = 1  # 自己
MAGIC_CTYPE_TARGET = 2  # 目标
MAGIC_CTYPE_CHOOSE = 3  # 点选
MAGIC_CTYPE_MAX = 3  # max center type

# magic field move type
MAGIC_MTYPE_STATIC = 1  # 静止
MAGIC_MTYPE_FL_SELF = 2  # 跟随施法者
MAGIC_MTYPE_LINE = 3  # 沿直线前进
MAGIC_MTYPE_FL_TGT = 4  # 跟随目标
MAGIC_MTYPE_MOTOR_TGT = 5  # motor驱动(目标为敌方)
MAGIC_MTYPE_MOTOR_SELF = 6  # motor驱动(目标为自己)
MAGIC_MTYPE_ATTACH = 7  # 跟随骨骼点移动
MAGIC_MTYPE_MAX = 7  # max move type

# magic field calc(damage) type
MAGIC_DTYPE_TIMER = 1  # 定时结算
MAGIC_DTYPE_TOUCH = 2  # 接触结算
MAGIC_DTYPE_CLICK = 3  # 点击结算
MAGIC_DTYPE_MOTOR = 4  # 弹道结算

# magic shape type
MAGIC_STYPE_POINT = 1   # 点
MAGIC_STYPE_CIRCLE = 2  # 圆形
MAGIC_STYPE_RECT = 3    # 矩形
MAGIC_STYPE_FAN = 4     # 扇形
MAGIC_STYPE_ANNULAR = 5  # 环形
MAGIC_STYPE_CYLINDER = 6  # 圆柱

# magic field totem fail code
MAGIC_T_OK = 1
MAGIC_T_NOTTOTEM = 2  # 不是图腾
MAGIC_T_TOTEL_NUM = 3  # 总次数用完
MAGIC_T_PLAYER_NUM = 4  # 个人次数用完
MAGIC_T_COOLDOWN = 5  # cd
MAGIC_T_DISTANCE = 6  # 距离不够
MAGIC_T_NEEDTARGET = 7  # 点击者不存在
MAGIC_T_NOSKILL = 8  # 无技能

# magic field invalid type
MAGIC_ITYPE_DISTANCE = 1  # 施法者脱离法术场范围
MAGIC_ITYPE_USED = 2  # 法术场遇到第一个目标成功结算消失
MAGIC_ITYPE_TOUCHED = 3  # 接触失效

# mfield and AlertEffect躲避规则
AVOID_TYPE_NO = -1
AVOID_TYPE_DEFAULT = 0
AVOID_TYPE_SIDE = 1  # 向两边躲，并且不需要等法术场消失
AVOID_TYPE_ALONG = 2  # 向远离法术场躲，需要等待法术场消失

# skill target assistant
STA_SPRINT_FACE = 1
STA_FACE = 2

# 队长集中控制类型
TEAM_CTRL_NOT_CTRL = 0  # 不被控制
TEAM_CTRL_FOLLOW_LEADER = 1  # 集中
TEAM_CTRL_FOCUS_ATTACK = 2  # 集火
TEAM_CTRL_STRIKE_BACK = 3  # 反击
TEAM_CTRL_AUTO_WAR = 4  # 自动
TEAM_CTRL_ESCAPE_WAR = 5  # 逃跑
TEAM_CTRL_UNDER_CTRL = 6  # 控制

# threat level
THREAT_LEVEL_PROTECT = 0  # 保护状态
THREAT_LEVEL_HARMLESS = 1  # 无害模式
THREAT_LEVEL_KILLING = 2  # 杀戮模式

# SKILL STATES
SKILL_STATE_UNKNOWN = 0  # 发起使用技能请求但结果未知
SKILL_STATE_PRECAST = 1  # 前摇
SKILL_STATE_PROGRESS = 2  # 进行中
SKILL_STATE_POSTCAST = 3  # 后摇
SKILL_STATE_MOVEPOST = 4  # 可移动后摇
SKILL_STATE_END = 5  # 技能使用完毕

SKILL_DURATION = 1.0  # 非玩家entity使用技能时强制加上的一个执行期长度，单位为秒

# MONSTER
DEFAULT_DESTROY_TIME = 0.8
DEFAULT_COLLECT_TIME = 120.0

# TARGET SWITCH DIST
TARGET_SWITCH_DIST = 50  # 切换目标时，小于此距离才会考虑

TICK_TIME_NO_TICK = 0
TICK_TIME_LOW_FREQUENCY = 1
TICK_TIME_NORMAL_FREQUENCY = .5
TICK_TIME_HIGH_FREQUENCY = .2

# HEAL HATE DIST
HEAL_HATE_DIST = 50

# AI B.T.

AI_DEBUG = True
DAMAGE_DEBUG = False


MAX_PANEL_SKILLS = 4
MAX_SELECT_ESKILLS = 2
MAX_SPACE_ITEM_SKILLS = 2
MAX_CHILD_SKILLS = 1
MAX_AWAKE_SKILLS = 1

STRBUFFID = 70

COMBOHITMAX = 999


BUFF_ID_FLOATINGS = (40, 71, 167)  # 身自在、风腾云、风七雷腾云
BUFF_ID_HOLY_SHIELD = 83
BUFF_ID_RAGE = 598  # 新手本怒气值buff
BUFF_ID_JUMP = 689  # 跳台子
BUFF_ID_HATKING = 5119 # 圣诞帽王

SKILL_ID_HOLY_SHIELD = 0   # 屏蔽百战神盾111
SKILL_ID_THREE_FIRE_SHOOT = 245  # 火三昧发射

# User Data Filter Operations
USER_DATA_FILTER_OP_EQ = 0
USER_DATA_FILTER_OP_NE = 1
USER_DATA_FILTER_OP_GT = 2
USER_DATA_FILTER_OP_GE = 3
USER_DATA_FILTER_OP_LT = 4
USER_DATA_FILTER_OP_LE = 5

# FOCUS EFFECT RADIUS
FOCUS_EFFECT_RADIUS = 1.0

# Target Select Radius
DEFAULT_TGT_SEL_RADIUS = 30.0
SURVIVAL_TGT_SEL_RADIUS = 10.0

# monster weakness type
WEAK_TYPE_HARM_MORE = 1
WEAK_TYPE_HARM_LESS = 2

# DEBUG
SKILL_CD = True

# task category
TASK_CATEGORY_NORMAL = 1  # 常规任务
TASK_CATEGORY_MAIN = 2  # 主线任务
TASK_CATEGORY_FESTIVAL = 3  # 节日任务
TASK_CATEGORY_MAIL = 4  # 收信和接信任务
TASK_MAIL_ACCEPTABLE1 = 1  # 信件可接类型1
TASK_MAIL_ACCEPTABLE2 = 2  # 信件可接类型2
TASK_MAIL_SENDABLE1 = 1  # 信件可达类型1
TASK_MAIL_SENDABLE2 = 2  # 信件可达类型2

# task type
TASK_TYPE_NORMAL = 0  # 常规任务
TASK_TYPE_LOOP = 1  # 循环任务目录
TASK_TYPE_ROUND = 2  # 循环任务中的一环
TASK_TYPE_GROUP_HEADER = 3  # 分组任务中的头任务
TASK_TYPE_GROUP_SUBTASK = 4  # 分组任务中的子任务

# special task
TASK_CLAN_CAPTAIN = 650
TASK_CLAN_CAPTAIN_TASKS = (651, 652, 653)
TASK_SPHERE_DEVIL = 327  # 副本除魔
TASK_DHYW = 1390  # 大荒演武堂

# activity status  完成状态由服务端决定，开启状态在客户端计算即可，服务端进行校验（世界boss结束状态由服务端结算）
ACTIVITY_STATUS_UNCOMPLETE = 0  # 未完成
ACTIVITY_STATUS_COMPLETE = 1  # 已完成
ACTIVITY_STATUS_UNOPEN = 2  # 未开启
ACTIVITY_STATUS_OPEN = 3  # 开启
ACTIVITY_STATUS_CLOSE = 4  # 已结束
ACTIVITY_STATUS_COMING = 5  # 即将开启

# monster interact type
INTERACT_TYPE_NONE = -1  # 中立，都不可交互
INTERACT_TYPE_SELF = 0  # 个人可交互
INTERACT_TYPE_TEAM = 1  # 小组可交互
INTERACT_TYPE_ALL = 2  # 所有人可交互

# refresh hour
REFRESH_SYS_ACTIVITY = 1
REFRESH_SYS_TASK = 2
REFRESH_SYS_AWARD = 3
REFRESH_SYS_SIGN_IN = 4
REFRESH_SYS_EXAM = 5
REFRESH_SYS_TREASURE_STORE = 6
REFRESH_SYS_CLAN = 7
REFRESH_SYS_MALL = 8
REFRESH_SYS_RANK_LIST = 9
REFRESH_SYS_RSM = 10
REFRESH_SYS_ARENA = 11
REFRESH_SYS_POKEMON_ITEM = 12
REFRESH_SYS_CREDIT = 13
REFRESH_SYS_SPACE_RECORD = 14
REFRESH_SYS_ITEM = 15
REFRESH_SYS_TRADE = 16
REFRESH_SYS_SURPLUS_EXP = 17
REFRESH_SYS_LEVEL = 18
REFRESH_SYS_SERVER_LEVEL = 19
REFRESH_SYS_ZONE = 20
REFRESH_SYS_SEND_ITEM = 21
REFRESH_SYS_ZONE_SELF = 22
REFRESH_SYS_PROFIT = 23
REFRESH_SYS_DEMON_TOWER = 24
REFRESH_SYS_MONTH_CARD = 25
REFRESH_SYS_BIWU = 26
REFRESH_CROSS_SUPPORT_ARENA = 27
REFRESH_CROSS_SUPPORT_CLAN = 28
REFRESH_LGGS = 29
REFRESH_TTBATTLE = 30
REFRESH_SYS_CHILD = 31
REFRESH_CLAN_VOICE_ENVELOPE = 32
REFRESH_SB_CONTEST = 36

REFRESH_HOUR_NORMAL = 0  # 0点刷新
_ALL_REFRESH_HOURS = {REFRESH_HOUR_NORMAL}
_ALL_REFRESH_HOURS.update(refresh_data.data.itervalues())
ALL_REFRESH_HOURS = frozenset(_ALL_REFRESH_HOURS)

REFRESH_VER_WEEKDAY = 3  # 版本日

# SYNC POS VALUES (meters)
SYNC_POS_VALUE_IMMEDIATE = 0
SYNC_POS_VALUE_PASSIVE = 0
SYNC_POS_VALUE_INITIATIVE = 0
SYNC_POS_VALUE_TRANSFER = 8  # 超过8米认为是传送
SYNC_POS_VALUE_LEVEL_IGNORE_DIST = 20  # 切Level允许距离
SYNC_POS_VALUE_LEVEL_IGNORE_TIME = 5.0  # 切Level忽略同步时间

# SYNC POS FLAGS
SYNC_POS_FLAG_PASSIVE = 1
SYNC_POS_FLAG_INITIATIVE = 2

# uplevel status
UP_LEVEL_SUCCESS = 0
UP_LEVEL_EXP_LESS = 1
UP_LEVEL_LEVEL_CANNOT_UP = 2
MAX_LV = 100

# monster event
NORMAL_MONSTER_KILLED = 0

# 场景类型
SPACE_TYPE_BIGWORLD = 0
SPACE_TYPE_RAID = 1
SPACE_TYPE_CLINE = 2

BUFF_NO_TELEPORT_TRANSMIT = 1
BUFF_NO_NPC_TRANSMIT = 2
BUFF_NO_CLINE_RETURN = 3
BUFF_LIMIT_TRANSMIT_TYPE = 11


# EDIT GRAPH 是否在角色编辑器
IN_EDIT_GRAPH = False

# 战斗单位基础属性
COMBAT_PROPS_LEVEL_0 = (
	"maxhp",			# 最大生命值
	"maxmp",			# 最大技力值
	"vice_maxhp",		# 最大副生命值
	"hp",				# 生命值
	"mp",          		# 技力值
	"vice_hp",			# 副生命值
)

# 战斗单位一级属性
COMBAT_PROPS_LEVEL_1 = (
	"dex",				# 敏
	"str",				# 力
	"int",				# 魂
	"mind",				# 念
	"dog",				# 疾
	"con",				# 体
)

# 战斗单位二级属性
COMBAT_PROPS_LEVEL_2 = (
	"hit",				# 命中
	"avoid",			# 回避
	"skprt",			# 神明
	"cri",				# 会心
	"pdmg",				# 物理攻击
	"mdmg",				# 法术攻击
	"eff_heal",			# 治疗强度
	"pdef",				# 物理防御
	"mdef",				# 法术防御
	"apdmg",			# 附加物理伤害
	"amdmg",			# 附加法术伤害
	"pptr",				# 物理穿透
	"mptr",				# 法术穿透
	"pdmg_resi",		# 物理抗性
	"mdmg_resi",		# 法术抗性
	"pdmg_sub",			# 物理减伤
	"mdmg_sub",			# 法术减伤
	"cri_a_r",			# 会心一击率	(影响是否会心)
	"cri_d_r",			# 会心抵抗率	(影响是否会心)
	"cri_add",			# 诛心			(影响会心伤害)
	"cri_sub",			# 御心  		(影响会心伤害)
	"raa0",				# 人祸
	"rad0",				# 知彼
	"dmgra1",			# 对怪伤害加成(百分比)
	"dmgrd1",			# 受怪伤害减免(百分比)
	"dmgra2",			# 对召唤兽伤害加成(百分比)
	"dmgrd2",			# 受召唤兽伤害减免(百分比)
	# "pdmga1",			# 对怪物理伤害
	# "mdmga1",			# 对怪法术伤害
	# "dmga1",			# 对怪绝对伤害增加(绝对值)
	# "dmgd1",			# 受怪绝对伤害减免(绝对值)
)

# 战斗单位三级属性
COMBAT_PROPS_LEVEL_3 = (
	"cri_heal",			# 治疗暴击
	"cri_heal_r",		# 治疗暴击率
	"add_heal",			# 治疗加成
	# "add_heal_r",		# 治疗加成率
	"add_beheal",		# 被治疗加成
	"add_criheal",		# 暴击治疗加成
	"sub_criheal",		# 暴击治疗减成
	# "block",			# 挡格
	# "wthstnd",		# 招架
	# "dodge",			# 闪避
	# "d_heart",			# 扰心
	# "p_heart",			# 护心
	# "atblock",			# 破挡格
	# "atwthstnd",		# 破招架
	# "atdodge",			# 破闪避
	# "rblock",			# 挡格率
	# "rwthstnd",			# 招架率
	# "rdodge",			# 闪避率
	# "ratblock",			# 破挡格率
	# "ratwthstnd",		# 破招架率
	# "ratdodge",			# 破闪避率
	"buff_hit",       	# 状态命中力
	"hit_r", 			# 命中率
	"avoid_r", 			# 回避率
	"p_hp_steal", 		# 物理吸血
	"m_hp_steal", 		# 法术吸血
	"speed_a",			# 追电
	# "sm_pp",			# 灵力
	# "luck",				# 幸运值
	"buff_resi_a",		# 坚韧
	"buff_resi_b",		# 身法
	"add_pdmg",			# 物理攻击加成
	"add_mdmg",			# 法术攻击加成
	"add_pdef",			# 物理防御加成
	"add_mdef",			# 法术防御加成
	"pkm_pdmg_dec",		# 召唤兽物理伤害减免
	"pkm_mdmg_dec",		# 召唤兽法术伤害减免
	"pkm_pdmg_dec_ignore",  # 忽视召唤兽物理伤害减免
	"pkm_mdmg_dec_ignore",  # 忽视召唤兽法术伤害减免
)

BASIC_COMBAT_PROPS = COMBAT_PROPS_LEVEL_0 + COMBAT_PROPS_LEVEL_1 + COMBAT_PROPS_LEVEL_2 + COMBAT_PROPS_LEVEL_3

BASIC_VAR_PROPS = (
	"assign_credits",			# 人物潜能点
)

ES_COMBAT_PROPS = (
	# 战斗特技属性
	"es_bwxj",			# 霸王卸甲
	"es_jm",			# 聚溟
	"es_tq",			# 调气
	"es_mys",			# 墨罂粟
	"es_hxqh",			# 会心强化
	"es_xy",			# 心眼
	"es_sczy",			# 射程增远
	"es_fwkd",			# 范围扩大
	"es_zdqh",			# 追电强化
	"es_hx",			# 护心
	"es_smqh",			# 神明强化
	"es_lx",			# 灵犀
	"es_wlctjt",		# 物伤精通
	"es_fsctjt",		# 法伤精通
	"es_ctjt",			# 附伤精通
	"es_wldx",			# 物理抵消
	"es_fsdx",			# 法术抵消
	"es_shdx",			# 附伤抵消
	"es_zstg",			# 咒术透骨
	"es_zsch",			# 咒术缠魂
	"es_tgch",			# 透骨缠魂
	"es_qtfh",			# 躯体防护
	"es_xdfh",			# 行动防护
	"es_ztfh",			# 状态防护
	"es_jtmf",			# 健体妙法
	"es_hcmf",			# 回春妙法
	"es_zsjh",			# 咒术净化
	"es_zsdk",			# 咒术抵抗
	"es_zsfh",			# 咒术防护
	"es_qxsh",			# 驱邪散秽
	"es_jl",			# 精炼
	"es_jy",			# 简易
	"es_wlfh",			# 物理防护
	"es_fsfh",			# 法术防护
	"es_wlhj",			# 物理化解
	"es_fshj",			# 法术化解
	"es_shhj",			# 伤害化解
	"es_qkny",			# 乾坤挪移
	"es_lkdz",			# 离坎斗转
	"es_wy",			# 威扬
	"es_miaoshou",		# 妙手
	"es_mingsi",		# 明思
	"es_jxhq",			# 极限回气
	"es_qx",			# 强袭
	"es_by",			# 混元
	"es_js",			# 疾闪
	"es_dyzh",			# 大禹之护
	"es_tgsw",			# 天国·神威
	"es_tlhg",			# 天籁·和光
	"es_tybr",			# 天音·百忍
	"es_tydd",			# 天逸·涤荡
	"es_tyyt",			# 天逸·元体
	"es_tzjs",			# 天诛·九死
)

EB_COMBAT_PROPS = (
	# 装备特效
	"eb_mg",			# 猛攻
	"eb_kf",			# 狂法
	"eb_js",			# 坚守
	"eb_yf",			# 御法
	"eb_gs",			# 固守
	"eb_ns",			# 修罗
	"eb_yw",			# 藏锋
	# "eb_tj",			# 透甲 暂时屏蔽
	# "eb_zs",			# 铸守 暂时屏蔽
	# "eb_pf",			# 破法 暂时屏蔽
	# "eb_hf",			# 护法 暂时屏蔽
	"eb_tl",			# 天狼
	"eb_sw",			# 神威
	"eb_gl",			# 刚力
	"eb_sy",			# 噬妖
	"eb_yl",			# 御灵
	"eb_hs",			# 化煞
	"eb_mf",			# 妙法
	"eb_bm",			# 不灭
)

V_PERCENTAGE = 1  # 百分比乘以100,使用时需要除以100
V_ABSOLUTE = 2  # 绝对值数值,直接使用
V_FORMULAID = 3  # 公式ID
V_EBREALM = 4  # 装备特效境界结算

ENTITY_TYPE_AVATAR = 1
ENTITY_TYPE_MONSTER = 2
ENTITY_TYPE_POKMON = 3

EB_FML_D1 = 1
EB_FML_D2 = 2
EB_FML_D3 = 3
EB_FML_D4 = 4
EB_FML_A1 = 5
EB_FML_A2 = 6
EB_FML_A3 = 7
EB_FML_A1_1 = 8

EB_CALC_PHY_DMG_FMLS = (
	(('eb_mg', ), ('eb_js', ), (V_FORMULAID, EB_FML_A1)),
	(('eb_mg', ), (), (V_PERCENTAGE, 0.25)),
	((), ('eb_js', ), (V_PERCENTAGE, 0.25)),
	(('eb_mg', ), (), (V_EBREALM, 'eb_mg')),
	((), ('eb_js', ), (V_EBREALM, 'eb_js')),
)

EB_CALC_MAG_DMG_FMLS = (
	(('eb_kf', ), ('eb_yf', ), (V_FORMULAID, EB_FML_A1)),
	(('eb_kf', ), (), (V_PERCENTAGE, 0.25)),
	((), ('eb_yf', ), (V_PERCENTAGE, 0.25)),
	(('eb_kf', ), (), (V_EBREALM, 'eb_kf')),
	((), ('eb_yf', ), (V_EBREALM, 'eb_yf')),
)

EB_CALC_DAMAGE_MAP = {
	(ENTITY_TYPE_AVATAR, ENTITY_TYPE_MONSTER): (
		(('eb_tl', ), (), (V_FORMULAID, EB_FML_A3)),
		(('eb_tl', ), (), (V_PERCENTAGE, 0.5)),
		(('eb_tl', ), (), (V_EBREALM, 'eb_tl')),
	),
	(ENTITY_TYPE_AVATAR, ENTITY_TYPE_POKMON): (
		(('eb_yl', ), (), (V_FORMULAID, EB_FML_A2)),
		(('eb_yl', ), (), (V_PERCENTAGE, 0.5)),
		(('eb_yl', ), (), (V_EBREALM, 'eb_yl')),
	),
	(ENTITY_TYPE_MONSTER, ENTITY_TYPE_AVATAR): (
		((), ('eb_sw', ), (V_FORMULAID, EB_FML_A3)),
		((), ('eb_sw', ), (V_PERCENTAGE, 0.5)),
		((), ('eb_sw', ), (V_EBREALM, 'eb_sw')),
	),
	(ENTITY_TYPE_POKMON, ENTITY_TYPE_AVATAR): (
		((), ('eb_hs', ), (V_FORMULAID, EB_FML_A2)),
		((), ('eb_hs', ), (V_PERCENTAGE, 0.5)),
		((), ('eb_hs', ), (V_EBREALM, 'eb_hs')),
	),
}

EB_CALC_PDMG_MAP = {
	(ENTITY_TYPE_AVATAR, ENTITY_TYPE_MONSTER): (
		(('eb_gl', ), (), (V_FORMULAID, EB_FML_A3)),
		(('eb_gl', ), (), (V_PERCENTAGE, 0.75)),
		(('eb_gl', ), (), (V_EBREALM, 'eb_gl')),
	),
}

EB_CALC_MDMG_MAP = {
	(ENTITY_TYPE_AVATAR, ENTITY_TYPE_MONSTER): (
		(('eb_sy', ), (), (V_FORMULAID, EB_FML_A3)),
		(('eb_sy', ), (), (V_PERCENTAGE, 0.75)),
		(('eb_sy', ), (), (V_EBREALM, 'eb_sy')),
	),
}

EB_CALC_CRIR_FMLS = (
	(('eb_ns', ), ('eb_yw', ), (V_FORMULAID, EB_FML_A2)),
	(('eb_ns', ), (), (V_PERCENTAGE, 0.5)),
	((), ('eb_yw', ), (V_PERCENTAGE, 0.5)),
	(('eb_ns', ), (), (V_EBREALM, 'eb_ns')),
	((), ('eb_yw', ), (V_EBREALM, 'eb_yw')),
)

EB_CALC_HEAL_RATE = (
	(('eb_mf', ), (), (V_FORMULAID, EB_FML_A1_1)),
	(('eb_mf', ), (), (V_PERCENTAGE, 1.0)),
	(('eb_mf', ), (), (V_EBREALM, 'eb_mf')),
)

EB_CALC_BEHEAL_RATE = (
	((), ('eb_bm', ), (V_FORMULAID, EB_FML_A1_1)),
	((), ('eb_bm', ), (V_PERCENTAGE, 1.0)),
	((), ('eb_bm', ), (V_EBREALM, 'eb_bm')),
)

EB_CALC_MAP = {
	"eb_gs": (
		{  # 1
			"eb_js": (V_ABSOLUTE, 1),
			"eb_yf": (V_ABSOLUTE, 1),
		}, {  # 2
		}, {  # 3
		}),
}

EB_TIPS_MAP = {
	'eb_mf': EB_CALC_HEAL_RATE,
}

MSS_COMBAT_PROPS = (
	# 冥思术属性
	"mss_add_cri",		# 冥思术会心加成
	"mss_add_skprt",		# 冥思术神明加成
	"mss_add_hit",		# 冥思术命中加成
	"mss_add_avoid",		# 冥思术回避加成
)

EQU_VAR_PROPS = (
	"useLevel",			# 使用等级
	"epigraphs",		# 铭文
	"attrIncRate",		# 固定属性修正比例
	"noTrading",		# 禁交易标识
)

# 战斗状态
USE_SKILL_EVENT = 1  # 使用技能
ON_DAMAGE_EVENT = 2  # 受击
ON_HIT_EVENT = 3  # 攻击
ON_DEAD_EVENT = 4  # 被击杀
ON_VERTIGO_EVENT = 5  # 被眩晕
ON_ADD_BUFF = 6  # 移除buff
ON_REMOVE_BUFF = 7  # 加buff
ON_MONSTER_SHAPESHIFT = 8  # 进入变身
ON_REMOVE_MONSTER_SHAPESHIFT = 9  # 退出变身
ON_ENTER_COMBAT = 10  # 进入战斗
ON_LEAVE_COMBAT = 11  # 退出战斗


# 属性刷新相关
REFRESH_TYPE_EQUIP = 0x1 << 0
REFRESH_TYPE_RIDESOULS = 0x1 << 1
REFRESH_TYPE_RIDE = 0x1 << 2
REFRESH_TYPE_ACHVENHANCE = 0x1 << 3
REFRESH_TYPE_CHILD = 0x1 << 4
REFRESH_TYPE_AWAKE = 0x1 << 5
REFRESH_TYPE_OTHER = 0x1 << 6


# 神祝符相关属性
SZF_PROPS = (
	"pdmg",  # 物理攻击",
	"mdmg",  # 法术攻击",
	"eff_heal",  # 治疗强度",
	"hp",  # 生命值",
	"mp",  # 技力值",
	"pdef",  # 物理防御",
	"mdef",  # 法术防御",
	"p_hp_steal",  # 物理吸血",
	"m_hp_steal",  # 法术吸血",
	"apdmg",  # 附加物理伤害",
	"amdmg",  # 附加法术伤害",
	"pptr",  # 物理穿透",
	"mptr",  # 法术穿透",
	"cri",  # 会心",
	"skprt",  # 神明",
	"hit",  # 命中",
	"avoid",  # 回避",
	"speed_a",  # 追电",
)

# 披风影响的属性
CLOAK_PROPS = (
	"str",
	"dex",
	"int",
	"mind",
	"dog",
	"con",
	"pdmg",
	"mdmg",
	"eff_heal",
	"maxhp",
	"maxmp",
	"pdef",
	"mdef",
	"p_hp_steal",
	"m_hp_steal",
	"apdmg",
	"amdmg",
	"pptr",
	"mptr",
	"hit",
	"avoid",
	"cri",
	"skprt",
	"cri_add",
	"cri_sub",
	"raa0",
	"rad0",
	"speed_a",
	"buff_hit",
	"buff_resi_b",
	"buff_resi_a",
	"pdmg_sub",
	"mdmg_sub",
	'cri_heal',
	"pdmg_resi",
	"mdmg_resi",
)

GEM_ITEM_IDS = range(41101, 41138)

def gemItemIdToNo(number):
	return number - 41100
def gemNoToItemId(number):
	return number + 41100

ENABLE_CLOAK_FORGE = True


# 驭兽符相关属性，和神祝符
YSF_PROPS = SZF_PROPS

EQUIP_COMBAT_PROPS = ES_COMBAT_PROPS + EB_COMBAT_PROPS

EQUIP_PROPS = BASIC_COMBAT_PROPS + EQUIP_COMBAT_PROPS

EQUIP_PROPS_INX_LIST = list(EQUIP_PROPS)

COMBAT_PROPS = EQUIP_PROPS + MSS_COMBAT_PROPS

COMBAT_PROPS_INX_LIST = list(COMBAT_PROPS)

EQUIP_PROPS_SET = frozenset(EQUIP_PROPS)

COMBAT_PROPS_SET = frozenset(COMBAT_PROPS)

# [DEBUG]
tlist = list(COMBAT_PROPS)
for attr in tlist:
	if tlist.count(attr) > 1:
		raise Exception('[const] check duplicated attr %s is duplicated' % attr)
# [DEBUG]

SPACE_TAG_SAFE = 1
SPACE_TAG_FORBID_FLY = 2
SPACE_TOTAL_TAGS = 8  # 暂时划定的区域总共只有8个，如果超过要修改这个值

# pk玩法最低等级
KILLING_READY_TIME = 5
# 玩家身份标识
ROLE_CIVILIAN = 0  # 平民
ROLE_VIOLENT = 1   # 枭雄
ROLE_COP = 2  # 巡捕
ROLE_COP_TMP = 3  # 临时巡捕

# 玩家攻击模式
PATTERN_PEACE = 0  # 和平模式
PATTERN_SCHOOL = 1  # 门派模式
PATTERN_CLAN = 2  # 势力模式
PATTERN_TEAM = 3  # 队伍模式
PATTERN_VIOLENT = 4  # 杀戮模式
PATTERN_JUSTICE = 5  # 侠义模式
PATTERN_ENEMY = 6  # 敌对模式

pvp_pattern_name = {
	PATTERN_PEACE: ("和平模式", "和平"),
	PATTERN_SCHOOL: ("门派模式", "门派"),
	PATTERN_CLAN: ("势力模式", "势力"),
	PATTERN_TEAM: ("队伍模式", "队伍"),
	PATTERN_VIOLENT: ("乱斗模式", "乱斗"),
	PATTERN_JUSTICE: ("侠义模式", "侠义"),
	PATTERN_ENEMY: ("敌对模式", "敌对"),
}

'''
不同身份可以用的攻击模式，列表第一个为默认模式
'''
ROLE_PATTERN_DICT = {
	ROLE_CIVILIAN: [PATTERN_PEACE, PATTERN_SCHOOL, PATTERN_CLAN, PATTERN_TEAM, PATTERN_ENEMY],
	ROLE_VIOLENT: [PATTERN_VIOLENT, PATTERN_SCHOOL, PATTERN_CLAN, PATTERN_TEAM, PATTERN_ENEMY],
	ROLE_COP: [PATTERN_JUSTICE, PATTERN_PEACE, PATTERN_SCHOOL, PATTERN_CLAN, PATTERN_TEAM, PATTERN_ENEMY],
	ROLE_COP_TMP: [PATTERN_JUSTICE, PATTERN_PEACE, PATTERN_SCHOOL, PATTERN_CLAN, PATTERN_TEAM, PATTERN_ENEMY],
}

EXCHANGE_GOLD_MILITARY = 100
EXCHANGE_GOLD_MONEY = 10000
EXCHANGE_MILITARY_MONEY = EXCHANGE_GOLD_MONEY / EXCHANGE_GOLD_MILITARY
EXCHANGE_GOLD_ACTIVE = 15
EXCHANGE_GOLD_NOTE = 1
EXCHANGE_GOLD_MILITARY_LIMIT = 50000  # 每天限制50000兑换
EXCHANGE_GOLD_TOKEN_ITEM = 1

NORMAL_WXP_ID = 5521
ADVANCED_WXP_ID = 5522
FQ_WXP_ID = 24642

WXP_EVENT_LOCAL_MONSTER = 1
WXP_EVENT_REMOTE_MONSTER = 2
WXP_EVENT_GAIN_MONEY = 3
WXP_EVENT_GAIN_ITEM = 4
WXP_EVENT_MONSTER_KING = 5

AWARD_POINT_ITEM_ID = 9003

TEAM_STATUS_NORMAL = 1
TEAM_STATUS_ON_CTRL = 2
TEAM_STATUS_FOLLOW = 3
TEAM_STATUS_CLIENT_LOST = 4
TEAM_STATUS_OFFLINE = 5
TEAM_STATUS_FISHING = 8
TEAM_STATUS_ONLINE_SET = (TEAM_STATUS_NORMAL, TEAM_STATUS_ON_CTRL, TEAM_STATUS_FOLLOW, TEAM_STATUS_FISHING)
TEAM_STATUS_OFFLINE_SET = (TEAM_STATUS_CLIENT_LOST, TEAM_STATUS_OFFLINE)
TEAM_STATUS_CTRL_SET = (TEAM_STATUS_ON_CTRL, TEAM_STATUS_FOLLOW)
TEAM_STATUS_NO_COMMAND_SET = (TEAM_STATUS_FOLLOW, TEAM_STATUS_CLIENT_LOST, TEAM_STATUS_OFFLINE, TEAM_STATUS_FISHING)
TEAM_STATUS_NO_LEADER_SET = TEAM_STATUS_CTRL_SET + TEAM_STATUS_OFFLINE_SET
TEAM_STATUS_ACTIVE_SET = TEAM_STATUS_ONLINE_SET + (TEAM_STATUS_CLIENT_LOST, )

# 弱点区域与角度映射，单位是pi
WEAK_AREA_ANGULE = {
	1: (1.0, 1.25),
	2: (1.25, 1.5),
	3: (1.5, 1.75),
	4: (1.75, 2),
	5: (0, 0.25),
	6: (0.25, 0.5),
	7: (0.5, 0.75),
	8: (0.75, 1),
}

# UI 显示用
TEAM_STATUS_DEAD = 6
TEAM_STATUS_FAR_AWAY = 7
# 判断人是否过远的阈值
FAR_AWAY_THRESHOLD = 20

# 寻路碰撞

NAVIGATE_DEFAULT = 0
NAVIGATE_NONOBSTACLE = 1
NAVIGATE_AVATAR = 2
NAVIGATE_MONSTER = 3
NAVIGATE_TEAM = 5

NPC_RANK = 10

# 行為樹debug
BTREE_NODE_IGNORE = -2

# 目标选择方式
TGT_SEL_STYLE_OLD = 1
TGT_SEL_STYLE_NEW = 2

# 课程表推送类型
PUSH_TYPE_ONE = 1
PUSH_TYPE_EVER = 4
PUSH_TYPE_TWO = 2
PUSH_TYPE_THREE = 3
PUSH_TYPE_MANUAL = 5    # 由程序控制推送效果
PUSH_TIME = {
	PUSH_TYPE_TWO: (600, ),
	PUSH_TYPE_THREE: (1800, 600,),
}

# Solo状态
SOLO_STATE_NONE = 0             # 无solo状态
SOLO_STATE_ASKING = 1           # 正在邀请别人
SOLO_STATE_BEING_ASKING = 2     # 正在被别人邀请
SOLO_STATE_PREPARE = 3          # solo准备阶段
SOLO_STATE_SOLO = 4             # 正在solo打架

ARENA_TYPE_1V1 = 1
ARENA_TYPE_3V3 = 3
ARENA_TYPE_5V5 = 5

SPACENO_DICT = {
	1: 206,
	2: 206,
	3: 206,
	4: 206,
}

# 竞技场申请失败
ARENA_SUCCESS = 0
ARENA_FAIL_OTHER = 1
ARENA_FAIL_ALREADYIN = 2
ARENA_FAIL_VIOLENT = 3
ARENA_IS_CONFIRMING = 4
ARENA_NOT_OPEN = 5
ARENA_MATCHED_NOT_IN = 6  # 上一次匹配的竞技场还未进入
ARENA_FAIL_LV = 7  # 等级不够
ARENA_SHUTDOWN = 8  # 竞技场玩法关闭

ARENA_FAIL_MSG = {
	ARENA_FAIL_ALREADYIN: '您已经申请',
	ARENA_FAIL_OTHER: '原因未明',
	ARENA_FAIL_VIOLENT: '枭雄不能参加竞技场',
	ARENA_IS_CONFIRMING: '您处于确认阶段，不能重复申请',
	ARENA_NOT_OPEN: "现在非竞技场比赛时间",
	ARENA_FAIL_LV: "您的等级太低",
	ARENA_SHUTDOWN: "竞技场玩法暂时关闭",
}

# ARENA_SIDE_BLUE = 1
# ARENA_SIDE_RED = 2

ARENA_SIDE_BLUE = 1
ARENA_SIDE_RED = 2

ARENA_RES_WIN = 1
ARENA_RES_LOSE = 2
ARENA_RES_TIE = 3
ARENA_RES_NO_ONE = 4  # 未进行此局

ARENA_CONFIRM_TIME = 15
ARENA_AGREE_INVITE_TIME = 30

ARENA_INVITE_SUCC = 0
ARENA_INVITE_FAIL_OFFLINE = 1
ARENA_INVITE_FAIL_ALREADY_INVITED = 2
ARENA_INVITE_FAIL_ALREADY_IN_ARENA = 3
ARENA_INVITE_FAIL_SCHOOL_DUPLICATE = 4
ARENA_INVITE_FAIL_DISAGREE = 5
ARENA_INVITE_FAIL_ALREADY_IN_TEAM = 6
ARENA_INVITE_FAIL_LV = 7
ARENA_INVITE_FAIL_STATE = 8
ARENA_INVITE_FAIL_PKROLE = 9
ARENA_INVITE_FAIL_TIMES = 10
ARENA_INVITE_FAIL_LVDAN = 11
ARENA_INVITE_FAIL_REPORT = 12
ARENA_INVITE_FAIL_CJ = 13
ARENA_INVITE_FAIL_PVP = 14

# Assign Credits
ASSIGN_BASIC_PROPS = ('dex', 'str', 'int', 'mind', 'dog', 'con')

# 属性前缀
ATTR_FIX = 'fix'  # 装备固定属性
ATTR_RANDOM = 'rnd'  # 装备随机属性
ATTR_SKILL = 'skl'  # 装备特技属性数值 + 装备特效属性数值
ATTR_GHOST = 'ghost' # 装备魂刻属性
ATTR_EQUIP = 'equ'  # 装备属性对属性加成
ATTR_EBUFF = 'ebf'  # 装备特效对属性加成
ATTR_APPRAISAL = 'appr'  # 装备鉴定属性
ATTR_INLAY = 'inlay'  # 装备炼化属性
ATTR_NEW_INLAY = 'new_inlay'  # 装备炼化属性（尚未替换）
ATTR_EPIGRAPHS = 'epigraphs'
ATTR_SZF = 'szf'  # 神祝符属性加成
ATTR_YSF = 'ysf'  # 驭兽符属性加成
ATTR_ACTIVATE_RND = 'frnd'  # 属性激活标记·随机属性
ATTR_ACTIVATE_ES = 'fes'  # 属性激活标记·装备特技
ATTR_ACTIVATE_EB = 'feb'  # 属性激活标记·装备特效
ATTR_APTITUDE = 'apt'  # 对天资和资质加成
ATTR_FW_SKILL_CD = 'fwsklcd'  # 符文对技能CD的加成
ATTR_FW_SKILL_DURATION = 'fwskldur'  # 符文对技能持续时间的加成
ATTR_FW_SKILL_POWER = 'fwsklpwr'  # 符文对技能威力加成
ATTR_NEW_RANDOM = 'new_' + ATTR_RANDOM
ATTR_NEW_SKILL = 'new_' + ATTR_SKILL
ATTR_NEW_APTITUDE = 'new_' + ATTR_APTITUDE
ATTR_NEW_FW_SKILL_CD = 'new_' + ATTR_FW_SKILL_CD
ATTR_NEW_FW_SKILL_DURATION = 'new_' + ATTR_FW_SKILL_DURATION
ATTR_NEW_FW_SKILL_POWER = 'new_' + ATTR_FW_SKILL_POWER
ATTR_CLOAK_ACTIVATE = 'cloak_activate_' # 披风激活数据前缀 cloak_attr_x_y_name 表示 第x层激活中（x = 1,2,3）, 第y列激活的属性（y = 1,2） 为name
ATTR_NEW_CLOAK_ACTIVATE = 'new_' + ATTR_CLOAK_ACTIVATE
ATTR_GEM_MOSAIC = "gem"
ATTR_CLOAK_ACTIVATE_NEW_EB = 'newcleb_'

ATTR_PREFIXS = [
	ATTR_FIX, ATTR_RANDOM, ATTR_SKILL, ATTR_EQUIP, ATTR_EPIGRAPHS, ATTR_SZF, ATTR_APPRAISAL, ATTR_INLAY, ATTR_NEW_INLAY,
	ATTR_APTITUDE, ATTR_FW_SKILL_CD, ATTR_FW_SKILL_DURATION, ATTR_FW_SKILL_POWER,
	ATTR_NEW_RANDOM, ATTR_NEW_SKILL, ATTR_NEW_APTITUDE, ATTR_NEW_FW_SKILL_CD, ATTR_NEW_FW_SKILL_DURATION, ATTR_NEW_FW_SKILL_POWER,
	ATTR_YSF, ATTR_GHOST, ATTR_CLOAK_ACTIVATE, ATTR_NEW_CLOAK_ACTIVATE, ATTR_GEM_MOSAIC, ATTR_CLOAK_ACTIVATE_NEW_EB,
]

ATTR_PREFIX_PATTERN = '|'.join(ATTR_PREFIXS)
ATTR_PREFIXS = frozenset(ATTR_PREFIXS)
RE_ATTR_FILTER = re.compile(r"(?P<prefix>(((_)?(%s)(_))(_)?))(((?P<index>((\d)*))(_))((?P<lib>((\d)*))(_))?)(?P<attrname>([A-Za-z]+(_?[A-Za-z0-9]+)+))_?" % ATTR_PREFIX_PATTERN)
RE_ATTR_ACTIVATE_FILTER = re.compile(r"(?P<prefix>(frnd|fes|feb))(_)(?P<lib>((\d)*))")

ATTR_GEN_APPR = frozenset([ATTR_FIX, ATTR_RANDOM])

ATTR_NONEQUIP_PREFIXS = frozenset([
	ATTR_APTITUDE, ATTR_FW_SKILL_CD, ATTR_FW_SKILL_DURATION, ATTR_FW_SKILL_POWER,
	ATTR_NEW_APTITUDE, ATTR_NEW_FW_SKILL_CD, ATTR_NEW_FW_SKILL_DURATION, ATTR_NEW_FW_SKILL_POWER,
])

ATTR_CHILD_RUNE_PREFIXS = frozenset([
	ATTR_RANDOM, ATTR_SKILL, ATTR_APTITUDE, ATTR_FW_SKILL_CD, ATTR_FW_SKILL_DURATION, ATTR_FW_SKILL_POWER
])

# Attr Affect Rules

ATTR_AFFECT_RULES = {
	"str": {"pdmg": 1, },  # 力
	"dex": {"cri": 0.75, "hit": 1, "cri_heal": 0.5, },  # 敏
	"int": {"mdmg": 1, },  # 魂
	"mind": {"mdef": 1.5, "eff_heal": 0.2, "maxmp": 5, },  # 念
	"dog": {"avoid": 1.5, "skprt": 0.5, },  # 疾
	"con": {"maxhp": 5, "pdef": 1, },  # 体
}


ATTR_AFFECT_ATTRS = ("maxhp", "maxmp", "pdmg", "mdmg", "eff_heal", "pdef", "mdef", "hit", "avoid", "cri", "skprt", "cri_heal")
# for k, v in ATTR_AFFECT_RULES.iteritems():
# 	ATTR_AFFECT_ATTRS.extend(v.keys())
# ATTR_AFFECT_ATTRS = tuple(ATTR_AFFECT_ATTRS)

# 临时按钮类型
TEMP_BTN_TEMPBAG = 1
TEMP_BTN_EXIT_DUNGEON = 2
TEMP_BTN_RELIVE = 3

# ATK_RESULT_TYPE
ATK_RESULT_NORMAL = 0  # 普通命中

ATK_RESULT_CRITICAL = 0x1  # 会心命中
ATK_RESULT_NOTHIT = 0x2  # 划过命中
ATK_RESULT_VULNERABLE = 0x4  # 弱点buff，伤害加深

# Primary Attr Rules
PRIMARY_ATTR_RULES = {
	SCHOOL_ID_HH: ["con", "str", "dog", "dex", "mind", "int", ],
	SCHOOL_ID_TJ: ["con", "dog", "str", "dex", "mind", "int", ],
	SCHOOL_ID_LY: ["str", "dex", "con", "dog", "mind", "int", ],
	SCHOOL_ID_WL: ["str", "dex", "con", "int", "dog", "mind", ],
	SCHOOL_ID_TX: ["int", "dex", "con", "mind", "dog", "str", ],
	SCHOOL_ID_YL: ["int", "dex", "con", "mind", "dog", "str", ],
	SCHOOL_ID_BX: ["int", "mind", "dex", "con", "dog", "str", ],
	SCHOOL_ID_YJ: ["str", "dex", "int", "con", "dog", "mind", ],
}

NPC_NO_CLAN_MANAGER = 2401
NPC_NO_ROYAL_SECRET_AGENT = 1001

# 网络连接状态:
NET_NO_REACH = -1  # 无连接
NET_WWAM = 0  # 其他
NET_WIFI = 1  # wifi

# Equip Halo Range
EQU_HALO_RANGE = 24

# Level up skills
LVUP_SKILL_FAILED = 0
LVUP_SKILL_OK = 1
LVUP_SKILL_MONEY = 2
LVUP_SKILL_MILITARY = 3
LVUP_SKILL_LEVELMAX = 4
LVUP_SKILL_ENABLE = 5
LVUP_SKILL_NOT_FOUND = 6
LVUP_SKILL_MILITARY_FREEZE = 7
LVUP_SKILL_MONEY_FREEZE = 8
LVUP_SKILL_SERVERCROSSING = 9
LVUP_SKILL_ERRPLAYERLEVEL = 10
LVUP_SKILL_ERRPRESKILLEVEL = 11

LVUP_SKILL_ERR = frozenset([LVUP_SKILL_MONEY, LVUP_SKILL_MILITARY, LVUP_SKILL_FAILED])

# SKILL SOURCES
SKILL_SRC_UNKNOWN = -1		# 未知
SKILL_SRC_ORIGIN = 0		# 原生
SKILL_SRC_EQUIP = 1			# 装备附加
SKILL_SRC_SHAPESHIFT = 2		# 变身附加
SKILL_SRC_CLANSKILL = 3		# 势力技能附加
SKILL_SRC_TITLE = 4			# 称谓附加
SKILL_SRC_XUANXIU = 5			# 玄修附加
SKILL_SRC_SPACE_ITEM = 6   # 副本道具附加
SKILL_SRC_POKEMON_MERGE = 7   # 召唤兽合体附加
SKILL_SRC_AWAKE = 8   # 觉醒
SKILL_SRC_CHILD = 9  # 孩子附加
SKILL_SRC_GHOST = 10  # 魂刻被动技能
SKILL_SRC_GEM_MOSAIC = 11		# 镶嵌辉曜之尘的被动技能
SKILL_SRC_CLOAK_ACTIVATE = 12		# 披风激活获得的被动技能
SKILL_SRC_ANTIQUE = 13   # 古董

NORMAL_IGNORE_SKILLS = [SKILL_SRC_SHAPESHIFT, ]

# 副本特殊物品槽数
SPACE_ITEM_MAX_SLOTS = 2

# PlayerMain 右上角button
AIP_BTN_BAG = 0
AIP_BTN_SIGNIN = 1
AIP_BTN_SCHEDULE = 2
AIP_BTN_SHOP = 3
AIP_BTN_RANK = 4
AIP_BTN_ACHIEVE = 5
AIP_BTN_PRESTIGE = 6

FORMATION_SKILL = {
	1: 10001,  # 地载阵
	2: 10002,  # 鸟翔阵
	3: 10003,  # 龙飞阵
}

CLOAK_LEVEL = 9999

# 披风的重铸，打造公式列表
CLOAK_FOMULAR_LIST = [3077, 3078, 3079, 3080, 3081, 3082, 3083, 3084, 3085, 3086, 3087, 3088, 3089, 3090, 3091, 3092, 3093, 3094]

# 披风装备列表，屏蔽五代披风
ALL_CLOAK_ITEM_ID_LIST = [3300, 3301, 3302, 3303, 3304, 3305, 3306, 3307, 3308, 3309]
CLOAK_ITEM_ID_LIST = [3300, 3301, 3302, 3303, 3305, 3306, 3307, 3308]

NEXT_CLOAK = {
	3300: 3301,
	3301: 3302,
	3302: 3303,
	3305: 3306,
	3306: 3307,
	3307: 3308,
}

# 可以打造的披风公式列表，屏蔽五代披风
# CLOAK_CAN_FORGE_FOMULAR_LIST = [3078, 3079, 3080, 3081, 3087, 3088, 3089, 3090]
CLOAK_CAN_FORGE_FOMULAR_LIST = [3078, 3079, 3080, 3087, 3088, 3089]

MEN_CLOAK_CAN_FORGE_FOMULAR_LIST = [3078, 3079, 3080]
WOMEN_CLOAK_CAN_FORGE_FOMULAR_LIST = [3087, 3088, 3089]

SCHOOL_CAN_FORGE_CLOAK_DICT = {
	SCHOOL_ID_YL: WOMEN_CLOAK_CAN_FORGE_FOMULAR_LIST,
	SCHOOL_ID_TJ: MEN_CLOAK_CAN_FORGE_FOMULAR_LIST,
	SCHOOL_ID_BX: WOMEN_CLOAK_CAN_FORGE_FOMULAR_LIST,
	SCHOOL_ID_YJ: MEN_CLOAK_CAN_FORGE_FOMULAR_LIST,
	SCHOOL_ID_TX: MEN_CLOAK_CAN_FORGE_FOMULAR_LIST,
	SCHOOL_ID_WL: WOMEN_CLOAK_CAN_FORGE_FOMULAR_LIST,
}

SCHOOL_CAN_FORGE_CLOAK = {
	2:  CLOAK_FOMULAR_LIST,
	5:  CLOAK_FOMULAR_LIST,
	8:  CLOAK_FOMULAR_LIST,
	4:  CLOAK_FOMULAR_LIST,
	6:  CLOAK_FOMULAR_LIST,
	7:  CLOAK_FOMULAR_LIST,
}

CLOAK_EQUIPTYPE = 16

# 披风id -> 披风代数
CLOAK_ID_TO_DAI= {
	3300: 1,
	3301: 2,
	3302: 3,
	3303: 4,
	3304: 5,
	3305: 1,
	3306: 2,
	3307: 3,
	3308: 4,
	3309: 5,
}

# 披风代数 -> 披风id
MAN_CLOAK_DAI_ID = {
	1: 3300,
	2: 3301,
	3: 3302,
	4: 3303,
	5: 3304,
}

WOMAN_CLOAK_DAI_ID = {
	1: 3305,
	2: 3306,
	3: 3307,
	4: 3308,
	5: 3309,
}

SCHOOL_CLOAK_DAI_TO_ID = {
	SCHOOL_ID_YL: WOMAN_CLOAK_DAI_ID,
	SCHOOL_ID_TJ: MAN_CLOAK_DAI_ID,
	SCHOOL_ID_BX: WOMAN_CLOAK_DAI_ID,
	SCHOOL_ID_YJ: MAN_CLOAK_DAI_ID,
	SCHOOL_ID_TX: MAN_CLOAK_DAI_ID,
	SCHOOL_ID_WL: WOMAN_CLOAK_DAI_ID,
}

GEM_LEVELUP_EXTRA_ITEM = [41138, 41139, 41140]

boyCloakAchi = {3300:1511, 3301:1512, 3302:1513, 3303:1514}
girlCloakAchi = {3305:1518, 3306:1519, 3307:1520, 3308:1521}

# 需要进行挂接缩放的时装
PANDA_DRESSING_LIST = [
	330,
	334,
	342,
	4,
	8,
	68,
]
PANDA_DRESSING_MODEL_LIST = [
	'Char/fash/2001/fash_body_2001',
	'Char/fash/6001/fash_body_6001',
	'Char/fash/5001/fash_body_5001',
	'Char/fash/1001/fash_body_1001',
]


SKILL_FORMATION = {
	v: k for k, v in FORMATION_SKILL.iteritems()
}

MAX_SKILL_LV = 100      # 技能最高等级

# 状态结束条件
BUFF_DEL_COND_PADMG_CRI = 1  # 下一次攻击造成物理附伤暴击后状态消失
BUFF_DEL_COND_MADMG_CRI = 2  # 下一次攻击造成法术附伤暴击后状态消失
BUFF_DEL_COND_ADMG_CRI = 3  # 下一次攻击造成的附伤暴击后状态消失
BUFF_DEL_COND_CRI = 4  # 下次攻击出现会心后状态消失
BUFF_DEL_COND_HIT_NEG_BUFF = 5  # 下次不良状态命中后状态消失
BUFF_DEL_COND_HIT_POS_BUFF = 6  # 下次正面状态命中后状态消失
BUFF_DEL_COND_USE_HEAL = 7  # 下次施展治疗技能后状态结束
BUFF_DEL_COND_GET_PADMG = 8  # 下次受到物理附伤攻击后状态消失
BUFF_DEL_COND_GET_MADMG = 9  # 下次受到法术附伤攻击后状态消失
BUFF_DEL_COND_GET_ADMG = 10  # 下次受到附伤攻击后状态消失
BUFF_DEL_COND_GET_STATIC_BUFF = 11  # 受到躯体类状态攻击后状态消失
BUFF_DEL_COND_GET_MOTION_BUFF = 12  # 受到行动类状态攻击后状态消失
BUFF_DEL_COND_GET_NEG_BUFF = 13  # 受到躯体或行动类状态(即负面状态)攻击后状态消失
BUFF_DEL_COND_GET_PNDMG = 14  # 受到普通物理攻击后状态消失
BUFF_DEL_COND_GET_MNDMG = 15  # 受到普通法术攻击后状态消失
BUFF_DEL_COND_GET_NDMG = 16  # 受到普通攻击后状态消失
BUFF_DEL_COND_USE_SKILL = 17  # 使用非普通攻击技能后状态消失
BUFF_DEL_COND_GET_DAMAGE_CNT = 18  # 受到N次伤害后状态消失
BUFF_DEL_COND_GET_DAMAGE_VAL = 19   # 受到N伤害后状态消失
BUFF_DEL_COND_USE_NONE_HEAL = 20   # 使用非治疗法术场结算类技能后状态消失

RELIVE_PROTECT_BUFF = 371
RELIVE_ITEM_NO = 9002
RELIVE_GREENHAND_LV = 30

GeneralLogInfo = frozenset([
	"device_model", "os_name", "os_ver", "mac_addr", "udid", "app_ver", "device_height",
	"device_width", "network", "nation", "isp", "adv_udid", "package_version", "engine_version",
	"engine_driver",
])

SAFE_BIT = 0x1
UNSAFE_BIT = 0x2
FLY_BIT = 0x4
UNFLY_BIT = 0x8

# 卡住脱离CD
FORCE_RESET_POS_CD = 300

# 组队跟随跳转至队长距离
TEAM_FOLLOW_DISTANCE = 40

# 寻路终点范围
DISTANCE_TO_NPC = 2.0
DISTANCE_TO_CHEST = 0.5


# 特殊技能类型编号
SCHOOL_SKILL_TYPE_PASSIVE = 1  # 被动
SCHOOL_SKILL_TYPE_NORMAL = 2   # 普攻
SCHOOL_SKILL_TYPE_INITIATE = 3  # 主动技能
SCHOOL_SKILL_TYPE_SPECIAL = 4  # 特殊

MAP_ENTITY_TYPE_FRIEND = 1  # 友方玩家
MAP_ENTITY_TYPE_FLAG = 2  # 战场旗帜
MAP_ENTITY_TYPE_TEAMMATE = 3  # 战场队友
MAP_ENTITY_TYPE_WAR_STATION = 4
MAP_ENTITY_TYPE_SNOW_BATTLE_FLAG = 5  # 雪地战场旗帜
MAP_ENTITY_TYPE_XSFLAG = 6  # 玄素旗

MAP_ENTITY_TYPE_FIXED = {MAP_ENTITY_TYPE_FLAG, MAP_ENTITY_TYPE_WAR_STATION, MAP_ENTITY_TYPE_SNOW_BATTLE_FLAG}  # 固定位置的Entity

# 订单的客户端支付结果
PAY_PRPARING = 0
PAY_SDK_CHECKING = 1
PAY_SDK_CHECK_OK = 2


# 排队结果
WAIT_PASS = 0  # 不需排队，或者排到位置
WAIT_INLINE = 1  # 需要排队，进入队列
WAIT_OUTLINE = 2  # 超过人数上限，不能排队
WAIT_RELAY = 3  # 排队过程中被顶号


# 同门弟子情，最长挑战时长
MAX_SM_DURATION = 2 ** 20

# 捉迷藏最长时间
MAX_HS_TIME = 2 ** 20

# 特效LOD
SFX_LOD_KEY = 'sfx_lod'
SFX_LOD_DEFAULT = 1

TAGS = (
	'IsAvatar',
	'IsAvatarCombat',
	'IsPlayerAvatar',
	'IsCombatUnit',
	'IsPokemon',
	'IsAvatarPokemon',
	'IsMonster',
	'IsMonsterGroup',
	'IsMagicField',
	'IsNPC',
	'IsEvilOgre',
	'IsSpaceWall',
	'IsSphereMarker',
	'IsSpaceSnare',
	'IsTreasure',
	'IsChest',
	'IsLuckyBead',
	'IsShowTestModel',
	'IsSoloFlag',
	'IsPersonalSpaceSnare',
	'IsServerRobot',
	'IsServerPokemon',
	'IsClickIndicator',
	'IsAvatarMonster',
	'IsHomeTree',
	'IsClanTree',
	'IsWildHorse',
	'IsBrideSphereMarker',
	'IsBrideHomeSnare',
	'IsCJFlagMarker',
	'IsPartner',
	'IsChild',
	'IsWatermelon',
	'IsSecuricar',
	'IsLotus',
	"IsPumpkin",
	'IsSurvivalItem',
	'IsSurvivalHideBody',
	'IsHorse',
	'IsHomeBuilding',
	'IsRetainer',
	'IsSimplePokemon',
	'IsDinnerItem',
	'IsFollower',
)

# CombatUnit类型
COMBATUNIT_TYPE_UNK = 0  # 未知
COMBATUNIT_TYPE_AVT = 1  # 人
COMBATUNIT_TYPE_PKM = 2  # 召唤兽
COMBATUNIT_TYPE_MST = 3  # 怪物
COMBATUNIT_TYPE_AVTMST = 4  # 人形怪
COMBATUNIT_TYPE_PKMMST = 5  # 召唤兽形怪
COMBATUNIT_TYPE_AVTROBOT = 6  # 人形怪（炮灰）

COMBATTYPE_DMGRATES = {
	(COMBATUNIT_TYPE_AVT, COMBATUNIT_TYPE_AVT): 0.5,
	(COMBATUNIT_TYPE_AVT, COMBATUNIT_TYPE_PKM): 0.5,
	(COMBATUNIT_TYPE_PKM, COMBATUNIT_TYPE_AVT): 0.4,
	(COMBATUNIT_TYPE_PKM, COMBATUNIT_TYPE_PKM): 0.5,
	(COMBATUNIT_TYPE_AVT, COMBATUNIT_TYPE_AVTMST): 0.5,
	(COMBATUNIT_TYPE_AVTMST, COMBATUNIT_TYPE_AVT): 0.5,
	(COMBATUNIT_TYPE_AVT, COMBATUNIT_TYPE_PKMMST): 0.5,
	(COMBATUNIT_TYPE_PKMMST, COMBATUNIT_TYPE_AVT): 0.4,
	(COMBATUNIT_TYPE_PKM, COMBATUNIT_TYPE_PKMMST): 0.5,
	(COMBATUNIT_TYPE_PKMMST, COMBATUNIT_TYPE_PKM): 0.5,
	(COMBATUNIT_TYPE_PKM, COMBATUNIT_TYPE_AVTMST): 0.4,
	(COMBATUNIT_TYPE_AVTMST, COMBATUNIT_TYPE_PKM): 0.5,
	(COMBATUNIT_TYPE_AVTROBOT, COMBATUNIT_TYPE_AVT): 0.1,
	(COMBATUNIT_TYPE_AVT, COMBATUNIT_TYPE_AVTROBOT): 0.5,
}

# 装备特效境界上限
EQUIP_BUFF_REALM_MAX = 9

GRAPHICS_LEVEL_LOW = 0
GRAPHICS_LEVEL_MEDIUM = 1
GRAPHICS_LEVEL_HIGH = 2
# GRAPHICS_LEVEL 对应 AOI范围
AOI_LEVELS = [30, 40, 45]

# RESET ASSIGNED POINTS
RESET_POINTS_ITEM = 5121


# 天下号令
ORDER_ITEMID = 9510
SORDER_ITEMID = 9511


# 技能-状态 已有表头伤害加成
# 增加表头 伤害加成类型
# 填1 代表伤害加成仅对人物生效
# 填2 代表伤害加成仅对召唤兽生效
# 填3 代表伤害加成仅对怪物生效
# 填0或者不填 代表对所有单位生效
IDR_ALL = 0
IDR_AVATAR = 1
IDR_POKEMON = 2
IDR_MONSTER = 3

# DOUBLE RIDE
DR_SIDE_BASE = 1  # 同骑主骑
DR_SIDE_ATTACH = 2  # 同骑副骑

DR_TYPE_FRIEND = 1  # 双人互动
DR_TYPE_COMRADE = 2  # 同袍互动
DR_TYPE_TRANSFORM = 3  # 变身小宠互动

DR_TYPES = {DR_TYPE_FRIEND, DR_TYPE_COMRADE, DR_TYPE_TRANSFORM}

# MISC AWARD
MISC_AWARD_ID_RELATED_PHONE = 1
MISC_AWARD_ID_TX3_PAYBACK = 3
MISC_AWARD_ID_ANDROID_PAYBACK = 4
MISC_AWARD_ID_CDKEY = 5
MISC_AWARD_ID_PC = 6
MISC_AWARD_IDS_SCHOLARSHIP = (7, 8, 9)
MISC_AWARD_ID_LOVE_INSURANCE = 10
MISC_AWARD_ID_SUPPORT_SHARE = 11
MISC_AWARD_ID_RETURN = 14
MISC_AWARD_ID_MERGESERVER = (16, 17, 18, 21, 25, 26, 28)
MISC_AWARD_ID_OPENING_SHARE = 15
MISC_AWARD_ID_SPRING_PRAY = 19
MISC_AWARD_ID_VOICE_SHARE = 20
MISC_AWARD_ID_AUTH = 22
MISC_AWARD_ID_CLANPOPULARITY_SHARE = 23
MISC_AWARD_ID_ENGINE_UPGRADE = 24
MISC_AWARD_ID_COMRADE_INSURANCE = 27

MISC_AWARD_SCHOLARSHIP_LIMIT = 90
MISC_AWARD_SCHOLARSHIP_INTERVAL = 30

# 收益记录类型
PROFIT_MONEY = 1
PROFIT_MILITARY = 2

PROFIT_OTHER = 0
PROFIT_EXCHANGE = 1
PROFIT_STORE = 2

# 限时特惠货币
SPECIAL_OFFER_GOLD = 1
SPECIAL_OFFER_MILITARY = 2
SPECIAL_OFFER_MONEY = 3

SPECIAL_OFFER_CURRENCY = {
	SPECIAL_OFFER_GOLD: ('gold', '元宝'),
	SPECIAL_OFFER_MILITARY: ('military', '军资'),
	SPECIAL_OFFER_MONEY: ('money', '金币'),
}

# 端游返利
TX3_MAX_PAYBACK = 20000
TX3_PAY_POINT_RATIO = 0.1

# 双人同骑需要好感度
DRIDE_DEGREE = 120

# 声望道具编号
CREDIT_ITEM_ID = 2001

# 属性转换类型
ATTR_CONVERT_TYPE_UPP = 1  # 按上限转换
ATTR_CONVERT_TYPE_PER = 2  # 按比例转换

# 不显示的队伍
TEAM_TYPE_TEMP = 4
TEAM_TARGET_TEMP = 4001

# 触发引导玩家去评论的天数
COMMENT_TRIGGER_DAYS = 7

# CLAN FIGHT
CLAN_FIGHT_BLUE = 1
CLAN_FIGHT_RED = 2

# CLAN SKILL TYPE
CLAN_SKILL_PLAYER = 1
CLAN_SKILL_POKEMON = 2

CLAN_FIGHT_SIDES = {
	CLAN_FIGHT_BLUE: 'BLUE',
	CLAN_FIGHT_RED: 'RED',
}

TIMER_MAX_DELAY = 14 * 86400  # Timer最长时间14天
TITLE_EXPIRE_FLAG = -1        # 称谓被动技能失效标记

MAX_ITEM_EFFECTS = 10

YMFG_ERRNO_SUCCESS = 0
YMFG_ERRNO_SHIELD = 1
YMFG_ERRNO_NOT_OPEN = 2
YMFG_ERRNO_INVALID = 3
YMFG_ERRNO_NOT_OCCUPY = 4
YMFG_ERRNO_LV = 5
YMFG_ERRNO_FULL = 6
YMFG_ERRNO_FINISHED = 7
YMFG_ERRNO_REPEAT = 8

YMFG_MSG = {
	YMFG_ERRNO_SUCCESS: "",
	YMFG_ERRNO_SHIELD: "该玩法将于近期开放，敬请期待",
	YMFG_ERRNO_NOT_OPEN: "不在妖魔反攻玩法开放时间内，无法进入",
	YMFG_ERRNO_INVALID: "台子不存在，无法进入",
	YMFG_ERRNO_NOT_OCCUPY: "您所在的势力未占领该祭天台",
	YMFG_ERRNO_LV: "你的等级不满足要求",
	YMFG_ERRNO_FULL: "当前场景人数已达上限",
	YMFG_ERRNO_FINISHED: "妖魔反攻已结束，无法进入",
	YMFG_ERRNO_REPEAT: "您当前已在妖魔反攻场景内，请退出后再试",
}

IDLE_TIME = 60 * 3

SPECIAL_SKILL_DELAY = 0.2

LIUGUANG_SPACENO = 321
SHOWROOM_SPACENO = 712

EQUIPSDETAIL_ATTRS = [
	'name',
	'body',
	'school',
	'dressing',
	'view_dressing',
	'view_dressing_color',
	'equip_halo_lv',
	'select_wings_lv',
	'equip_halo_enhance',
	'equip_halo_total_enhance',
	'experient_halo_time',
	'experient_halo_id',
	'select_wings_enhance',
	'select_wings_lv',
	'useExperienceWings',
	'wingOnShift',
	'school_shapeshift',
	'monster_shapeshift',
	'model_shapeshift',
	'rubbing',
	'enableCloakShow',
	'cloakModelChoose',
]

MJXX_RANK_LISTS = range(133, 148) + range(205, 208)

# getESRealm 检查类型

CHECK_TYPE_ROLE = 1
CHECK_TYPE_ITEM = 2

# 天域武器编号池
TIANYU_EQUIPS = frozenset([
	1018,  # 天籁梵音
	1015,  # 天国王朝
	1021,  # 天音无相
	1024,  # 天逸云舒
	1160,  # 天逸霞光
])

# SPACE_NO_SKILL_ACT_BROADCAST
SPACE_TYPE_NO_SKILL_ACT_BROADCAST = frozenset([
	11,  # 势力战
])

# CHANGE_SCHOOL_CONDITIONS
CH_SCH_NEED_EXP = 1  # 转职条件之一：消耗玩家5千万的当前经验
CH_SCH_NEED_PLV = 2  # 转职条件之一：等级要求
CH_SCH_NO_EQUIP = 3  # 转职条件之一：取下身上所有装备
CH_SCH_MARRIAGE = 4  # 转职条件之一：解除情缘关系
CH_SCH_NPC = 5  # 转职条件之一：并非本周门派首席
CH_SCH_SCH_TASK = 6  # 转职条件之一：没有进行中的门派相关任务
CH_SCH_RND_TASK = 7  # 转职条件之一：没有进行中的循环任务
CH_SCH_RND_ARENA_PLAYOFF = 8  # 转职条件之一：不处于单服和跨服季后赛
CH_SCH_NEED_ITEM = 9  # 转职条件之一：收取道具幽明易谷丹
CH_SCH_COMRADE = 10  # 转职条件之一：解除同袍关系

CH_SCH_CONDITIONS = (
	CH_SCH_NEED_PLV,
	CH_SCH_NEED_ITEM,
	CH_SCH_NEED_EXP,
	CH_SCH_NO_EQUIP,
	CH_SCH_MARRIAGE,
	CH_SCH_SCH_TASK,
	CH_SCH_RND_TASK,
	CH_SCH_RND_ARENA_PLAYOFF,
	CH_SCH_COMRADE,
)

CH_SCH_EXP = 50000000
CH_SCH_PLV = 69
CH_SCH_ITEM = 6140

CH_SCH_DESC = {
	CH_SCH_NEED_EXP: '消耗%d当前经验' % CH_SCH_EXP,
	CH_SCH_NEED_PLV: '等级要求%d' % CH_SCH_PLV,
	CH_SCH_NO_EQUIP: '取下身上所有装备',
	CH_SCH_MARRIAGE: '解除情缘关系',
	CH_SCH_COMRADE: '解除同袍关系',
	CH_SCH_SCH_TASK: '没有进行中的门派任务',
	CH_SCH_RND_TASK: '没有进行中的循环任务',
	CH_SCH_RND_ARENA_PLAYOFF: "不能处于季后赛或者跨服季后赛",
	CH_SCH_NEED_ITEM: '包裹栏里有道具%s' % item_data.data.get(CH_SCH_ITEM, {}).get('Name', CH_SCH_ITEM)
}

SUPPORT_SHARE_ITEM = 30001

OPENING_SHARE_RATIO = 20
OPENING_SHARE_ITEM = 5263
OPENING_CREDIT_ID = 30
OPENING_MAIL = 10106

OPENING_AWARDS = (
	(30118, 60),
	(30117, 20),
	(30116, 5),
)

MERGE_FRIEND_LIMIT = 10
MERGE_FRIEND_ITEM = 30002
MERGE_FRIEND_CD = 60
MERGE_ADD_INTERVAL = 7
MERGE_AWARD_INTERVAL = 30

RETURN_FRIEND_LIMIT = 10
RETURN_FRIEND_ITEM = 30003
RETURN_FRIEND_CD = 60

RETURN_FLAG_LIFETIME = 15  # 回流标识时长为15天

ALARM_REVIEWER_LOGIN_ACCOUNTS = {
	"txsytest1@163.com",
	"txsytest2@163.com",
	"txsytest3@163.com",
	"txsytest4@163.com",
	"txsytest5@163.com",
	"txsytest6@163.com",
	"txsytest7@163.com",
	"txsytest8@163.com",
	"txsytest9@163.com",
}

# 客户端等待隐身模型替换状态
SKILL_WAIT_UNKNOWN = 0
SKILL_WAIT_MODEL = 1
SKILL_WAIT_READY = 2
SKILL_WAIT_OK = 3

LOCK_REASON = {
	'xxjy': '因线下交易已被冻结',
	'dsf': '因使用第三方辅助软件已被冻结',
	'sjyc': '因数据异常被临时冻结',
	'wgxx': '因发布违规信息被冻结',
	'wlyc': '当前网络不可用，请检查网络是否正常连接',
}

SKILL_SOURCE_TYPE_UNKNOWN = 0
SKILL_SOURCE_TYPE_NORMAL = 1

TOKEN_ITEM_ID = 12919
TOKEN_ITEM_TEXTURE = 'ui_5106.png'

# 盈福经验上限奖励编号
SURPLUS_MAX_EXP_AWARD_NO = 3002050
SURPLUS_DAY_EXP_AWARD_NO = 3002082

# 好友召回
RECALL_STATE_NONE = 0
RECALL_STATE_IN = 1
RECALL_STATE_DONE = 2

# 实名认证
AUTH_AWARD_MAIL_ID = 10148

# 免流月卡开放渠道
FREE_FLOW_OPEN_CHANNELS = (
	'pc-messiah', 'pc',
	'netease', 'huawei', 'nearme_vivo', 'oppo', 'xiaomi_app',
	'360_assistant', 'uc_platform',
	'lenovo_open', 'gionee', 'yixin', 'letv_sdk', 'wandoujia',
	'flyme', 'baidu', 'coolpad_sdk', 'nubia',
)

RANDOM_RIDECARRIER_OPEN_LV = 50

# 新手战场任务奖励直接使用
NEWBEE_BATTLE_TASK_AWARDNO = 3004607


# 组队推送
InitiateTeamMessage = 1
SeekTeamMessage = 2

GhostColorDescMap = {
	1: '鬼',
	2: '人',
	3: '地',
	4: '神',
}

# 七夕节邮件ID
ROSE_MAIL_NO = 172
BLUE_ROSE_MAIL_NO = 213

# 聊天消息的背景
ROSE_WORLD_BG = 3  # 玩家赠送玫瑰的时候，发送的消息背景
# 万圣节聊天背景
HALLOWMAS_MSG_BG = 4  # 万圣节聊天的消息背景
# 绝地逃杀背景
SURVIVAL_MSG_BG = 5
SURVIVAL_BEST_MSG_BG = 6

SHORTMSG_MSG_BGS = frozenset([HALLOWMAS_MSG_BG, SURVIVAL_MSG_BG, SURVIVAL_BEST_MSG_BG])

RIGHTMSG_MSG_BGS = frozenset([SURVIVAL_MSG_BG, 7, 8])

VALENTINES_ROSE_WORLD_BG = 9	# 情人节送玫瑰世界通告背景

# 最长冻结时间
LOCK_MAX_TIME = 864000 * 365

# 新版hotfix开关
START_NEW_HOTFIX = True

# 引擎强更版本
ENGINE_FORCE_UPGRADE_FLAG = True
ENGINE_FORCE_UPGRADE_VERSION = {  # 目标版本
	'ios': 400278,
	'android': 400278,
	'windows': 400278,
}
ENGINE_FORCE_UPGRADE_VERSION_MIN = {  # 最小可登陆版本
	'ios': 400278,
	'android': 400278,
	'windows': 373172,
}
ENGINE_FORCE_UP_AWARD_MAIL_ID = 10349
ENGINE_FORCE_UP_NOTIFY_MAIL_ID = 10350
ENGINE_FORCE_UP_NOTIFY_MAIL_ID_201803 = 10387
