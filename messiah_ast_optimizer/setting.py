# -*- coding:utf-8 -*-

import os


# 直接inline的Constant
INLINE_CONST = {
	os.path.normpath('common/const.py'): 'const',
	os.path.normpath('client/cconst.py'): 'cconst',
	os.path.normpath('server/sconst.py'): 'sconst',
}
# 通过打标签形式inline的constant
CONFIG_INLINE_CONST = {

}
CONFIG_TAG = '@inline'
INLINE_CONST_FILES = INLINE_CONST.keys() + CONFIG_INLINE_CONST.keys()
