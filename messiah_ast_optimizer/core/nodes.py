# -*- coding:utf-8 -*-


class INode(object):
	def __init__(self, parent):
		self.parent = parent


class alias(INode):
	_fields = ('name', 'asname')

	def __init__(self, parent=None):
		super(alias, self).__init__(parent)

	def postinit(self, name, asname):
		self.name = name
		self.asname = asname


class arguments(INode):
	_fields = ('args', 'vararg', 'kwarg', 'defaults')

	def __init__(self, parent=None):
		super(arguments, self).__init__(parent)

	def postinit(self, args, vararg, kwarg, defaults):
		self.args = args
		self.vararg = vararg
		self.kwarg = kwarg
		self.defaults = defaults


class boolop(INode):
	_fields = ()

	def __init__(self, parent=None):
		super(boolop, self).__init__(parent)

	def postinit(self):
		pass


class cmpop(INode):
	_fields = ()

	def __init__(self, parent=None):
		super(cmpop, self).__init__(parent)

	def postinit(self):
		pass


class comprehension(INode):
	_fields = ('target', 'iter', 'ifs')

	def __init__(self, parent=None):
		super(comprehension, self).__init__(parent)

	def postinit(self, target, iter, ifs):
		self.target = target
		self.iter = iter
		self.ifs = ifs


class excepthandler(INode):
	_fields = ()

	def __init__(self, parent=None):
		super(excepthandler, self).__init__(parent)

	def postinit(self):
		pass


class expr(INode):
	_fields = ()

	def __init__(self, parent=None):
		super(expr, self).__init__(parent)

	def postinit(self):
		pass


class expr_context(INode):
	_fields = ()

	def __init__(self, parent=None):
		super(expr_context, self).__init__(parent)

	def postinit(self):
		pass


class keyword(INode):
	_fields = ('arg', 'value')

	def __init__(self, parent=None):
		super(keyword, self).__init__(parent)

	def postinit(self, arg, value):
		self.arg = arg
		self.value = value


class mod(INode):
	_fields = ()

	def __init__(self, parent=None):
		super(mod, self).__init__(parent)

	def postinit(self):
		pass


class operator(INode):
	_fields = ()

	def __init__(self, parent=None):
		super(operator, self).__init__(parent)

	def postinit(self):
		pass


class slice(INode):
	_fields = ()

	def __init__(self, parent=None):
		super(slice, self).__init__(parent)

	def postinit(self):
		pass


class stmt(INode):
	_fields = ()

	def __init__(self, parent=None):
		super(stmt, self).__init__(parent)

	def postinit(self):
		pass


class unaryop(INode):
	_fields = ()

	def __init__(self, parent=None):
		super(unaryop, self).__init__(parent)

	def postinit(self):
		pass


class Add(operator):
	_fields = ()

	def __init__(self, parent=None):
		super(Add, self).__init__(parent)

	def postinit(self):
		pass


class And(boolop):
	_fields = ()

	def __init__(self, parent=None):
		super(And, self).__init__(parent)

	def postinit(self):
		pass


class Assert(stmt):
	_fields = ('test', 'msg')

	def __init__(self, parent=None):
		super(Assert, self).__init__(parent)

	def postinit(self, test, msg):
		self.test = test
		self.msg = msg


class Assign(stmt):
	_fields = ('targets', 'value')

	def __init__(self, parent=None):
		super(Assign, self).__init__(parent)

	def postinit(self, targets, value):
		self.targets = targets
		self.value = value


class Attribute(expr):
	_fields = ('value', 'attr', 'ctx')

	def __init__(self, parent=None):
		super(Attribute, self).__init__(parent)

	def postinit(self, value, attr, ctx):
		self.value = value
		self.attr = attr
		self.ctx = ctx


class AugAssign(stmt):
	_fields = ('target', 'op', 'value')

	def __init__(self, parent=None):
		super(AugAssign, self).__init__(parent)

	def postinit(self, target, op, value):
		self.target = target
		self.op = op
		self.value = value


class AugLoad(expr_context):
	_fields = ()

	def __init__(self, parent=None):
		super(AugLoad, self).__init__(parent)

	def postinit(self):
		pass


class AugStore(expr_context):
	_fields = ()

	def __init__(self, parent=None):
		super(AugStore, self).__init__(parent)

	def postinit(self):
		pass


class BinOp(expr):
	_fields = ('left', 'op', 'right')

	def __init__(self, parent=None):
		super(BinOp, self).__init__(parent)

	def postinit(self, left, op, right):
		self.left = left
		self.op = op
		self.right = right


class BitAnd(operator):
	_fields = ()

	def __init__(self, parent=None):
		super(BitAnd, self).__init__(parent)

	def postinit(self):
		pass


class BitOr(operator):
	_fields = ()

	def __init__(self, parent=None):
		super(BitOr, self).__init__(parent)

	def postinit(self):
		pass


class BitXor(operator):
	_fields = ()

	def __init__(self, parent=None):
		super(BitXor, self).__init__(parent)

	def postinit(self):
		pass


class BoolOp(expr):
	_fields = ('op', 'values')

	def __init__(self, parent=None):
		super(BoolOp, self).__init__(parent)

	def postinit(self, op, values):
		self.op = op
		self.values = values


class Break(stmt):
	_fields = ()

	def __init__(self, parent=None):
		super(Break, self).__init__(parent)

	def postinit(self):
		pass


class Call(expr):
	_fields = ('func', 'args', 'keywords', 'starargs', 'kwargs')

	def __init__(self, parent=None):
		super(Call, self).__init__(parent)

	def postinit(self, func, args, keywords, starargs, kwargs):
		self.func = func
		self.args = args
		self.keywords = keywords
		self.starargs = starargs
		self.kwargs = kwargs


class ClassDef(stmt):
	_fields = ('name', 'bases', 'body', 'decorator_list')

	def __init__(self, parent=None):
		super(ClassDef, self).__init__(parent)

	def postinit(self, name, bases, body, decorator_list):
		self.name = name
		self.bases = bases
		self.body = body
		self.decorator_list = decorator_list


class Compare(expr):
	_fields = ('left', 'ops', 'comparators')

	def __init__(self, parent=None):
		super(Compare, self).__init__(parent)

	def postinit(self, left, ops, comparators):
		self.left = left
		self.ops = ops
		self.comparators = comparators


class Continue(stmt):
	_fields = ()

	def __init__(self, parent=None):
		super(Continue, self).__init__(parent)

	def postinit(self):
		pass


class Del(expr_context):
	_fields = ()

	def __init__(self, parent=None):
		super(Del, self).__init__(parent)

	def postinit(self):
		pass


class Delete(stmt):
	_fields = ('targets',)

	def __init__(self, parent=None):
		super(Delete, self).__init__(parent)

	def postinit(self, targets):
		self.targets = targets


class Dict(expr):
	_fields = ('keys', 'values')

	def __init__(self, parent=None):
		super(Dict, self).__init__(parent)

	def postinit(self, keys, values):
		self.keys = keys
		self.values = values


class DictComp(expr):
	_fields = ('key', 'value', 'generators')

	def __init__(self, parent=None):
		super(DictComp, self).__init__(parent)

	def postinit(self, key, value, generators):
		self.key = key
		self.value = value
		self.generators = generators


class Div(operator):
	_fields = ()

	def __init__(self, parent=None):
		super(Div, self).__init__(parent)

	def postinit(self):
		pass


class Ellipsis(slice):
	_fields = ()

	def __init__(self, parent=None):
		super(Ellipsis, self).__init__(parent)

	def postinit(self):
		pass


class Eq(cmpop):
	_fields = ()

	def __init__(self, parent=None):
		super(Eq, self).__init__(parent)

	def postinit(self):
		pass


class ExceptHandler(excepthandler):
	_fields = ('type', 'name', 'body')

	def __init__(self, parent=None):
		super(ExceptHandler, self).__init__(parent)

	def postinit(self, type, name, body):
		self.type = type
		self.name = name
		self.body = body


class Exec(stmt):
	_fields = ('body', 'globals', 'locals')

	def __init__(self, parent=None):
		super(Exec, self).__init__(parent)

	def postinit(self, body, globals, locals):
		self.body = body
		self.globals = globals
		self.locals = locals


class Expr(stmt):
	_fields = ('value',)

	def __init__(self, parent=None):
		super(Expr, self).__init__(parent)

	def postinit(self, value):
		self.value = value


class Expression(mod):
	_fields = ('body',)

	def __init__(self, parent=None):
		super(Expression, self).__init__(parent)

	def postinit(self, body):
		self.body = body


class ExtSlice(slice):
	_fields = ('dims',)

	def __init__(self, parent=None):
		super(ExtSlice, self).__init__(parent)

	def postinit(self, dims):
		self.dims = dims


class FloorDiv(operator):
	_fields = ()

	def __init__(self, parent=None):
		super(FloorDiv, self).__init__(parent)

	def postinit(self):
		pass


class For(stmt):
	_fields = ('target', 'iter', 'body', 'orelse')

	def __init__(self, parent=None):
		super(For, self).__init__(parent)

	def postinit(self, target, iter, body, orelse):
		self.target = target
		self.iter = iter
		self.body = body
		self.orelse = orelse


class FunctionDef(stmt):
	_fields = ('name', 'args', 'body', 'decorator_list')

	def __init__(self, parent=None):
		super(FunctionDef, self).__init__(parent)

	def postinit(self, name, args, body, decorator_list):
		self.name = name
		self.args = args
		self.body = body
		self.decorator_list = decorator_list


class GeneratorExp(expr):
	_fields = ('elt', 'generators')

	def __init__(self, parent=None):
		super(GeneratorExp, self).__init__(parent)

	def postinit(self, elt, generators):
		self.elt = elt
		self.generators = generators


class Global(stmt):
	_fields = ('names',)

	def __init__(self, parent=None):
		super(Global, self).__init__(parent)

	def postinit(self, names):
		self.names = names


class Gt(cmpop):
	_fields = ()

	def __init__(self, parent=None):
		super(Gt, self).__init__(parent)

	def postinit(self):
		pass


class GtE(cmpop):
	_fields = ()

	def __init__(self, parent=None):
		super(GtE, self).__init__(parent)

	def postinit(self):
		pass


class If(stmt):
	_fields = ('test', 'body', 'orelse')

	def __init__(self, parent=None):
		super(If, self).__init__(parent)

	def postinit(self, test, body, orelse):
		self.test = test
		self.body = body
		self.orelse = orelse


class IfExp(expr):
	_fields = ('test', 'body', 'orelse')

	def __init__(self, parent=None):
		super(IfExp, self).__init__(parent)

	def postinit(self, test, body, orelse):
		self.test = test
		self.body = body
		self.orelse = orelse


class Import(stmt):
	_fields = ('names',)

	def __init__(self, parent=None):
		super(Import, self).__init__(parent)

	def postinit(self, names):
		self.names = names


class ImportFrom(stmt):
	_fields = ('module', 'names', 'level')

	def __init__(self, parent=None):
		super(ImportFrom, self).__init__(parent)

	def postinit(self, module, names, level):
		self.module = module
		self.names = names
		self.level = level


class In(cmpop):
	_fields = ()

	def __init__(self, parent=None):
		super(In, self).__init__(parent)

	def postinit(self):
		pass


class Index(slice):
	_fields = ('value',)

	def __init__(self, parent=None):
		super(Index, self).__init__(parent)

	def postinit(self, value):
		self.value = value


class Interactive(mod):
	_fields = ('body',)

	def __init__(self, parent=None):
		super(Interactive, self).__init__(parent)

	def postinit(self, body):
		self.body = body


class Invert(unaryop):
	_fields = ()

	def __init__(self, parent=None):
		super(Invert, self).__init__(parent)

	def postinit(self):
		pass


class Is(cmpop):
	_fields = ()

	def __init__(self, parent=None):
		super(Is, self).__init__(parent)

	def postinit(self):
		pass


class IsNot(cmpop):
	_fields = ()

	def __init__(self, parent=None):
		super(IsNot, self).__init__(parent)

	def postinit(self):
		pass


class LShift(operator):
	_fields = ()

	def __init__(self, parent=None):
		super(LShift, self).__init__(parent)

	def postinit(self):
		pass


class Lambda(expr):
	_fields = ('args', 'body')

	def __init__(self, parent=None):
		super(Lambda, self).__init__(parent)

	def postinit(self, args, body):
		self.args = args
		self.body = body


class List(expr):
	_fields = ('elts', 'ctx')

	def __init__(self, parent=None):
		super(List, self).__init__(parent)

	def postinit(self, elts, ctx):
		self.elts = elts
		self.ctx = ctx


class ListComp(expr):
	_fields = ('elt', 'generators')

	def __init__(self, parent=None):
		super(ListComp, self).__init__(parent)

	def postinit(self, elt, generators):
		self.elt = elt
		self.generators = generators


class Load(expr_context):
	_fields = ()

	def __init__(self, parent=None):
		super(Load, self).__init__(parent)

	def postinit(self):
		pass


class Lt(cmpop):
	_fields = ()

	def __init__(self, parent=None):
		super(Lt, self).__init__(parent)

	def postinit(self):
		pass


class LtE(cmpop):
	_fields = ()

	def __init__(self, parent=None):
		super(LtE, self).__init__(parent)

	def postinit(self):
		pass


class Mod(operator):
	_fields = ()

	def __init__(self, parent=None):
		super(Mod, self).__init__(parent)

	def postinit(self):
		pass


class Module(mod):
	_fields = ('body',)

	def __init__(self, parent=None):
		super(Module, self).__init__(parent)

	def postinit(self, body):
		self.body = body


class Mult(operator):
	_fields = ()

	def __init__(self, parent=None):
		super(Mult, self).__init__(parent)

	def postinit(self):
		pass


class Name(expr):
	_fields = ('id', 'ctx')

	def __init__(self, parent=None):
		super(Name, self).__init__(parent)

	def postinit(self, id, ctx):
		self.id = id
		self.ctx = ctx


class Not(unaryop):
	_fields = ()

	def __init__(self, parent=None):
		super(Not, self).__init__(parent)

	def postinit(self):
		pass


class NotEq(cmpop):
	_fields = ()

	def __init__(self, parent=None):
		super(NotEq, self).__init__(parent)

	def postinit(self):
		pass


class NotIn(cmpop):
	_fields = ()

	def __init__(self, parent=None):
		super(NotIn, self).__init__(parent)

	def postinit(self):
		pass


class Num(expr):
	_fields = ('n',)

	def __init__(self, parent=None):
		super(Num, self).__init__(parent)

	def postinit(self, n):
		self.n = n


class Or(boolop):
	_fields = ()

	def __init__(self, parent=None):
		super(Or, self).__init__(parent)

	def postinit(self):
		pass


class Param(expr_context):
	_fields = ()

	def __init__(self, parent=None):
		super(Param, self).__init__(parent)

	def postinit(self):
		pass


class Pass(stmt):
	_fields = ()

	def __init__(self, parent=None):
		super(Pass, self).__init__(parent)

	def postinit(self):
		pass


class Pow(operator):
	_fields = ()

	def __init__(self, parent=None):
		super(Pow, self).__init__(parent)

	def postinit(self):
		pass


class Print(stmt):
	_fields = ('dest', 'values', 'nl')

	def __init__(self, parent=None):
		super(Print, self).__init__(parent)

	def postinit(self, dest, values, nl):
		self.dest = dest
		self.values = values
		self.nl = nl


class RShift(operator):
	_fields = ()

	def __init__(self, parent=None):
		super(RShift, self).__init__(parent)

	def postinit(self):
		pass


class Raise(stmt):
	_fields = ('type', 'inst', 'tback')

	def __init__(self, parent=None):
		super(Raise, self).__init__(parent)

	def postinit(self, type, inst, tback):
		self.type = type
		self.inst = inst
		self.tback = tback


class Repr(expr):
	_fields = ('value',)

	def __init__(self, parent=None):
		super(Repr, self).__init__(parent)

	def postinit(self, value):
		self.value = value


class Return(stmt):
	_fields = ('value',)

	def __init__(self, parent=None):
		super(Return, self).__init__(parent)

	def postinit(self, value):
		self.value = value


class Set(expr):
	_fields = ('elts',)

	def __init__(self, parent=None):
		super(Set, self).__init__(parent)

	def postinit(self, elts):
		self.elts = elts


class SetComp(expr):
	_fields = ('elt', 'generators')

	def __init__(self, parent=None):
		super(SetComp, self).__init__(parent)

	def postinit(self, elt, generators):
		self.elt = elt
		self.generators = generators


class Slice(slice):
	_fields = ('lower', 'upper', 'step')

	def __init__(self, parent=None):
		super(Slice, self).__init__(parent)

	def postinit(self, lower, upper, step):
		self.lower = lower
		self.upper = upper
		self.step = step


class Store(expr_context):
	_fields = ()

	def __init__(self, parent=None):
		super(Store, self).__init__(parent)

	def postinit(self):
		pass


class Str(expr):
	_fields = ('s',)

	def __init__(self, parent=None):
		super(Str, self).__init__(parent)

	def postinit(self, s):
		self.s = s


class Sub(operator):
	_fields = ()

	def __init__(self, parent=None):
		super(Sub, self).__init__(parent)

	def postinit(self):
		pass


class Subscript(expr):
	_fields = ('value', 'slice', 'ctx')

	def __init__(self, parent=None):
		super(Subscript, self).__init__(parent)

	def postinit(self, value, slice, ctx):
		self.value = value
		self.slice = slice
		self.ctx = ctx


class Suite(mod):
	_fields = ('body',)

	def __init__(self, parent=None):
		super(Suite, self).__init__(parent)

	def postinit(self, body):
		self.body = body


class TryExcept(stmt):
	_fields = ('body', 'handlers', 'orelse')

	def __init__(self, parent=None):
		super(TryExcept, self).__init__(parent)

	def postinit(self, body, handlers, orelse):
		self.body = body
		self.handlers = handlers
		self.orelse = orelse


class TryFinally(stmt):
	_fields = ('body', 'finalbody')

	def __init__(self, parent=None):
		super(TryFinally, self).__init__(parent)

	def postinit(self, body, finalbody):
		self.body = body
		self.finalbody = finalbody


class Tuple(expr):
	_fields = ('elts', 'ctx')

	def __init__(self, parent=None):
		super(Tuple, self).__init__(parent)

	def postinit(self, elts, ctx):
		self.elts = elts
		self.ctx = ctx


class UAdd(unaryop):
	_fields = ()

	def __init__(self, parent=None):
		super(UAdd, self).__init__(parent)

	def postinit(self):
		pass


class USub(unaryop):
	_fields = ()

	def __init__(self, parent=None):
		super(USub, self).__init__(parent)

	def postinit(self):
		pass


class UnaryOp(expr):
	_fields = ('op', 'operand')

	def __init__(self, parent=None):
		super(UnaryOp, self).__init__(parent)

	def postinit(self, op, operand):
		self.op = op
		self.operand = operand


class While(stmt):
	_fields = ('test', 'body', 'orelse')

	def __init__(self, parent=None):
		super(While, self).__init__(parent)

	def postinit(self, test, body, orelse):
		self.test = test
		self.body = body
		self.orelse = orelse


class With(stmt):
	_fields = ('context_expr', 'optional_vars', 'body')

	def __init__(self, parent=None):
		super(With, self).__init__(parent)

	def postinit(self, context_expr, optional_vars, body):
		self.context_expr = context_expr
		self.optional_vars = optional_vars
		self.body = body


class Yield(expr):
	_fields = ('value',)

	def __init__(self, parent=None):
		super(Yield, self).__init__(parent)

	def postinit(self, value):
		self.value = value
