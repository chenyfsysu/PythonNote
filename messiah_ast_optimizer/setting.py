# -*- coding:utf-8 -*-

import logging

"""GLOBAL"""
LOG_LEVEL = logging.DEBUG

IGNORE_DIRS = (
	'entities/client/data', 'entities/antihijack', 'entities/Debug', 'entities/client/InputChecker_Generated', 'entities/client/Offline',
	'entities/server/data', 'entities/server/hotfix', 'entities/server/appplatform', 'entities/server/gmexecutor',
	'entities/common/ai', 'entities/common/remote', 'entities/common/GmCommand', 'entities/common/TreeDBG',
	'entities/bot'
)
IGNORE_FILES = ()

SYS_PATH_ROUTINE = (
	('entities/client', ['', 'entities/client', 'entities/common', 'engine', 'engine/Lib']),
	('entities/server', ['entities/server', 'entities/common', 'engine', 'engine/Lib']),
	('entities/common', ['entities/common', 'engine', 'engine/Lib']),
)


"""CONST OPTIMIZER"""
# 直接inline的Constant
INLINE_CONST = (
	'entities/common/const.py',
	'entities/client/cconst.py',
	'entities/server/sconst.py',
)
# 通过打标签形式inline的constant
CONFIG_INLINE_CONST = (
)
CONST_INLINE_TAG = '@inline'
INLINE_CONST_FILES = INLINE_CONST + CONFIG_INLINE_CONST
CONST_ATTRIBUTES = ('const', 'cconst', 'sconst')  # 只有这些名字的Attribute才会检查，避免每个Attribute都要load出来


"""INLINE OPTIMIZER"""
INLINE_FUNC_TAG = 'inline'