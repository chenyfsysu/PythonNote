# -*- coding:utf-8 -*-

import operator
import ast

BUILTIN_NAME = ('True', 'False', 'None')
UNKNOW = object()


BIN_OPERATOR = {
	ast.Add: operator.add,
	ast.Sub: operator.sub,
	ast.Mult: operator.mul,
	ast.Div: operator.truediv,
	ast.FloorDiv: operator.floordiv,
	ast.Mod: operator.mod,
	ast.Pow: operator.pow,
	ast.LShift: operator.lshift,
	ast.RShift: operator.rshift,
	ast.BitAnd: operator.and_,
	ast.BitOr: operator.or_,
	ast.BitXor: operator.xor,
}

# NameType
NT_LOCAL = 1
NT_GLOBAL_IMPLICIT = 2
NT_GLOBAL_EXPLICIT = 3
NT_FREE = 4
NT_CELL = 5
NT_UNKNOWN = 6

NT_DUMP = {
	NT_LOCAL: 'LOCAL',
	NT_GLOBAL_IMPLICIT: 'GLOBAL_EXPLICIT',
	NT_GLOBAL_EXPLICIT: 'NT_GLOBAL_EXPLICIT',
	NT_FREE: 'FREEVARS',
	NT_CELL: 'CELLVARS',
	NT_UNKNOWN: 'UNKNOW'
}

# ScopeType
ST_MODULE = 1
ST_CLASS = 2
ST_FUNCTION = 3
ST_GENERATOR = 4


NameType = enum(LOCAL=1, GLOBAL_IMPLICIT=2, GLOBAL_EXPLICIT=3, FREE=4, CELL=5, UNKNOW=6)

ScopeType = enum(MODULE=1, CLASS=2, FUNCTION=3, GENERATOR=4)

NameDef = enum(IMPORT=1, IMPORTFROM=2, FUNCTIONDEF=3, CLASSDEF=4, ASSIGN=5, ARGS=6)
