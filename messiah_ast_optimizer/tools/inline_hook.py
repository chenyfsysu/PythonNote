# -*- coding:utf-8 -*-

import os
import sys

try:
	import opcode_chaos as opcode
except:
	import opcode



CALL = ('CALL_FUNCTION', 'CALL_FUNCTION_VAR', 'CALL_FUNCTION_KW', 'CALL_FUNCTION_VAR_KW')
CALL_OP = [opcode.opmap[op] for op in CALL]



class ConsumeAtom(object):
	def __init__(self, consume_cnt, provides):
		self.consumes = []
		self.consume_cnt = consume_cnt
		self.provides = provides

	def push(self, sth):
		self.consumes.append(sth)
		return len(self.consumes) >= self.consume_cnt


class CallTracer(object):
	IGNORE_OP = (
		'STOP_CODE',
		'NOP',
		'SETUP_FINALLY',
		'SETUP_EXCEPT',
		'SETUP_LOOP',
		'DELETE_GLOBAL',
	)

	def __init__(self):
		self.need_cnt = 0
		self.consumers = []
		self.result  = None

	def clear(self):
		self.need_cnt = 0
		self.consumers = []
		self.result  = None

	def trace(self, code, lasti):
		self.clear()

		bytecode, bytename, arguments = self.parseCode(code, lasti)
		self.dispatch(bytecode, bytename, arguments)

		while lasti > 0:
			if self.isOpCode(code.co_code, lasti - 1):
				lasti = lasti - 1
			else:
				lasti = lasti - 3

			bytecode, bytename, arguments = self.parseCode(code, lasti)
			self.dispatch(bytecode, bytename, arguments)

			if not self.consumers:
				return self.result.consumes[-1] if self.result else ''

	def isOpCode(self, code ,lasti):
		if lasti > 1 and ord(code[lasti - 2]) > opcode.HAVE_ARGUMENT:
			return False

		return True

	def parseCode(self, code, lasti):
		bytecode = ord(code.co_code[lasti])
		bytename = opcode.opname[bytecode]

		arg = None
		arguments = []

		if bytecode >= opcode.HAVE_ARGUMENT:
			arg = code.co_code[lasti + 1 : lasti + 3]
			val = ord(arg[0]) + (ord(arg[1]) << 8)

			if  bytename == 'LOAD_FAST_ZERO_LOAD_CONST':
				arguments = [code.co_varnames[0], code.co_consts[val]]
				return bytecode, bytename, arguments

			if bytecode in opcode.hasconst:
				arg = code.co_consts[val]
			elif bytecode in opcode.hasfree:
				if val < len(code.co_cellvars):
					arg = code.co_cellvars[val]
				else:
					var_idx = val - len(code.co_cellvars)
					arg = code.co_freevars[var_idx]
			elif bytecode in opcode.hasname:
				arg = code.co_names[val]
			elif bytecode in opcode.hasjrel:
				arg = lasti + val + 3
			elif bytecode in opcode.hasjabs:
				arg = val
			elif bytecode in opcode.haslocal:
				arg = code.co_varnames[val]
			else:
				arg = val
			arguments = [arg]

		return bytecode, bytename, arguments

	def dispatch(self, bytecode, bytename, arguments):
		if bytename in self.IGNORE_OP:
			return

		if bytecode in opcode.hasjrel or bytecode in opcode.hasjabs:
			self.clear()
			return

		if bytename.startswith('UNARY_'):
			return self.unaryOperation()

		elif bytename.startswith('BINARY_'):
			return self.binaryOperation()

		elif bytename.startswith('INPLACE_'):
			return self.inplaceOperation()

		elif 'SLICE+' in bytename:
			self.sliceOperation(bytename)

		else:
			return getattr(self, bytename)(*arguments)

	def consume(self, consume_cnt, provides):
		self.consumers.append(ConsumeAtom(consume_cnt, provides))

	def provide(self, sth):
		full = self.consumers[-1].push(sth)
		if full:
			consumer = self.consumers.pop()

			if self.consumers:
				map(self.provide, consumer.provides)
			else:
				self.result = consumer

	def unaryOperation(self):
		pass

	def binaryOperation(self):
		self.consume(2, [''])

	def inplaceOperation(self):
		self.consume(2, [''])

	def LOAD_CONST(self, const):
		self.provide(const)

	def POP_TOP(self):
		self.consume(1, [])

	def DUP_TOP(self):
		self.provide('')

	def DUP_TOPX(self, count):
		self.consume(count, [''] * count * 2)

	def ROT_TWO(self):
		self.consume(2, [''] * 2)

	def ROT_THREE(self):
		self.consume(3, [''] * 3)

	def ROT_FOUR(self):
		self.consume(4, [''] * 4)

	def sliceOperation(self, op):
		op, count = op[:-2], int(op[-1])

		if count in (1, 2):
			consume = 2
		elif count  == 3:
			consume = 3
		else:
			consume = 1

		provide = []
		if not op.startswith('STORE_') and not op.startswith('DELETE_'):
			provide = ['']

		self.consume(consume, provide)

	def LOAD_NAME(self, name):
		self.provide(name)

	def STORE_NAME(self, name):
		self.consume(1, [])

	def DELETE_NAME(self, name):
		pass

	def LOAD_FAST(self, name):
		self.provide(name)

	def LOAD_FAST_ZERO_LOAD_CONST(self, fastname, constname):
		self.LOAD_CONST(constname)
		self.LOAD_FAST(fastname)

	def STORE_FAST(self, name):
		self.consume(1, [])

	def DELETE_FAST(self, name):
		pass

	def LOAD_GLOBAL(self, name):
		self.provide(name)

	def STORE_GLOBAL(self, name):
		self.consume(1, [])

	def LOAD_DEREF(self, name):
		self.provide(name)

	def STORE_DEREF(self, name):
		self.consume(1, [])

	def LOAD_LOCALS(self):
		self.provide(name)

	def COMPARE_OP(self, opnum):
		self.consume(2, [''])

	def LOAD_ATTR(self, attr):
		self.consume(1, [attr])

	def STORE_ATTR(self, name):
		self.consume(2, [])

	def DELETE_ATTR(self, name):
		self.consume(1, [])

	def STORE_SUBSCR(self):
		self.consume(3, [])

	def DELETE_SUBSCR(self):
		self.consume(2, [])

	def BUILD_TUPLE(self, count):
		self.consume(count, [''])

	def BUILD_LIST(self, count):
		self.consume(count, [''])

	def BUILD_SET(self, count):
		self.consume(count, [''])

	def BUILD_MAP(self, size):
		self.provide('')

	def STORE_MAP(self):
		self.consume(3, [''])

	def UNPACK_SEQUENCE(self, count):
		pass

	def BUILD_SLICE(self, count):
		self.consume(count, [''])

	def LIST_APPEND(self, count):
		self.consume(1, [])

	def SET_ADD(self, count):
		self.consume(1, [])

	def MAP_ADD(self, count):
		self.consume(2, [])

	def PRINT_EXPR(self):
		self.consume(1, [])

	def PRINT_ITEM(self):
		self.consume(1, [])

	def PRINT_ITEM_TO(self):
		self.consume(2, [])

	def PRINT_NEWLINE(self):
		pass

	def PRINT_NEWLINE_TO(self):
		self.consume(1, [])

	def MAKE_FUNCTION(self, argc):
		self.consume(argc + 1, [''])

	def LOAD_CLOSURE(self, name):
		self.provide(name)

	def MAKE_CLOSURE(self, argc):
		self.consume(argc + 2, [''])

	def CALL_FUNCTION(self, arg):
		return self.call_function(arg, 0)

	def CALL_FUNCTION_VAR(self, arg):
		return self.call_function(arg, 1)

	def CALL_FUNCTION_KW(self, arg):
		return self.call_function(arg, 1)

	def CALL_FUNCTION_VAR_KW(self, arg):
		return self.call_function(arg, 2)

	def call_function(self, arg, consume):
		kw, pos = divmod(arg, 256)
		consume += 2 * kw + pos + 1
		self.consume(consume, [''])

	def RETURN_VALUE(self):
		self.consume(1, [])

	def IMPORT_NAME(self, name):
		self.consume(2, [''])

	def IMPORT_STAR(self):
		self.consume(1, [])

	def IMPORT_FROM(self, name):
		self.provide(name)

	def EXEC_STMT(self):
		self.consume(3, []) # stmt, globs, locs

	def BUILD_CLASS(self):
		self.consume(3, []) # name, bases, methods

	def GET_ITER(self):
		self.consume(1, [''])


class _InlineHandler():
	def __init__(self):
		self.inlines = {}
		self.tracer = CallTracer()
		self.hook_path = ''

	def setHookPath(self, path):
		self.hook_path = path

	def __call__(self, frame, event, arg):
		if event != 'call' or not frame.f_back:
			return

		ofile = os.path.normpath(frame.f_globals.get('__file__', ''))
		if ofile and not ofile.startswith(self.hook_path):
			return

		file = os.path.normpath(frame.f_back.f_globals['__file__'])
		if not file.startswith(self.hook_path):
			return

		back = frame.f_back
		code = back.f_code
		bytecode = ord(code.co_code[back.f_lasti])

		if bytecode not in CALL_OP:
			return

		if len(code.co_consts) >= 256 or len(code.co_names) >= 256 or len(code.co_varnames) >= 256:
			return

		name = self.tracer.trace(back.f_code, back.f_lasti)
		if name and name in self.inlines and id(frame.f_code) != self.inlines[name]:
			pass
			# raise Exception('inline function call of %s is duplicate with %s, lineno: %d' % (name, file, back.f_lineno))

	def addInline(self, func):
		self.inlines[func.__name__] = id(func.func_code)


InlineHandler = _InlineHandler()


def inline(func):
	if func.func_closure:
		raise RuntimeError('inline function of %s has closure' % func.func_name)

	if func.func_defaults:
		raise RuntimeError('inline function of %s has defaults' % func.func_name)

	InlineHandler.addInline(func)

	return func


def hook(path):
	InlineHandler.setHookPath(path)
	sys.setprofile(InlineHandler)


if __name__ == '__main__':
	import dis
	dis.dis(func.__code__)

	tracer = CallTracer()
	print tracer.trace(func.__code__, 57)
