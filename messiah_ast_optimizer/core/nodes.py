# -*- coding:utf-8 -*-
"""
动态拓展原生AstNode
"""

import _ast
import inspect

from module_loader import ModuleLoader
from const import NT_LOCAL, NT_GLOBAL_IMPLICIT, NT_GLOBAL_EXPLICIT, NT_FREE, NT_CELL, NT_UNKNOWN


def dynamic_extend(cls):
	def _dynamic_extend(klass):
		for name, func in inspect.getmembers(klass, inspect.ismethod):
			setattr(cls, name, func.im_func)

	return _dynamic_extend


class Node(object):

	def __postinit__(self, parent):
		self.parent = parent
		self.is_constant = False
		self.scope = None

	def nModule(self):
		module = self
		while module.parent:
			module = module.parent

		return module

	def nScope(self):
		scope = self
		while scope and scope.scope is None:
			scope = scope.parent

		return scope if scope.scope else None

	def nFunc(self):
		func = self
		while func and not isinstance(f, ast.FunctionDef):
			func = func.parent

		return func if isinstance(func, ast.FunctionDef) else None

	def nClass(self):
		cls = self
		while cls and not isinstance(cls, ast.ClassDef):
			cls = cls.parent
		return cls if isinstance(cls, ast.ClassDef) else None

	def assignConst(self, val):
		self.is_constant = True
		self.val = val


class ScopeNode(Node):
	def __postinit__(self, parent):
		Node.__postinit__.im_func(self, parent)

	def load(self, name, only_locals=True):
		sc = self.scope.identify(name) == NT_LOCAL
		if sc:
			return self.scope.locals.get(name, None)
		if not only_locals and sc in (NT_GLOBAL_EXPLICIT, NT_GLOBAL_IMPLICIT):
			return self.nModule().load(name)

		return None

@dynamic_extend(_ast.alias)
class alias(Node):
	pass


@dynamic_extend(_ast.arguments)
class arguments(Node):
	pass


@dynamic_extend(_ast.boolop)
class boolop(Node):
	pass


@dynamic_extend(_ast.cmpop)
class cmpop(Node):
	pass


@dynamic_extend(_ast.comprehension)
class comprehension(Node):
	pass


@dynamic_extend(_ast.excepthandler)
class excepthandler(Node):
	pass


@dynamic_extend(_ast.expr)
class expr(Node):
	pass


@dynamic_extend(_ast.expr_context)
class expr_context(Node):
	pass


@dynamic_extend(_ast.keyword)
class keyword(Node):
	pass


@dynamic_extend(_ast.mod)
class mod(Node):
	pass


@dynamic_extend(_ast.operator)
class operator(Node):
	pass


@dynamic_extend(_ast.slice)
class slice(Node):
	pass


@dynamic_extend(_ast.stmt)
class stmt(Node):
	pass


@dynamic_extend(_ast.unaryop)
class unaryop(Node):
	pass


@dynamic_extend(_ast.Add)
class Add(Node):
	pass


@dynamic_extend(_ast.And)
class And(Node):
	pass


@dynamic_extend(_ast.Assert)
class Assert(Node):
	pass


@dynamic_extend(_ast.Assign)
class Assign(Node):
	pass


@dynamic_extend(_ast.Attribute)
class Attribute(Node):
	pass


@dynamic_extend(_ast.AugAssign)
class AugAssign(Node):
	pass


@dynamic_extend(_ast.AugLoad)
class AugLoad(Node):
	pass


@dynamic_extend(_ast.AugStore)
class AugStore(Node):
	pass


@dynamic_extend(_ast.BinOp)
class BinOp(Node):
	pass


@dynamic_extend(_ast.BitAnd)
class BitAnd(Node):
	pass


@dynamic_extend(_ast.BitOr)
class BitOr(Node):
	pass


@dynamic_extend(_ast.BitXor)
class BitXor(Node):
	pass


@dynamic_extend(_ast.BoolOp)
class BoolOp(Node):
	pass


@dynamic_extend(_ast.Break)
class Break(Node):
	pass


@dynamic_extend(_ast.Call)
class Call(Node):
	pass


@dynamic_extend(_ast.ClassDef)
class ClassDef(ScopeNode):
	def nMro(self):
		mro = [self]
		seqs = [seq.nMro() for seq in self.nBases() if seq]

	def nBases(self):
		bases = []
		for base in self.bases:
			if isinstance(base, _ast.Name):
				base.id != 'object' and bases.append(base.load())
			elif isinstance(base, _ast.Attribute):
				pass
		return bases


@dynamic_extend(_ast.Compare)
class Compare(Node):
	pass


@dynamic_extend(_ast.Continue)
class Continue(Node):
	pass


@dynamic_extend(_ast.Del)
class Del(Node):
	pass


@dynamic_extend(_ast.Delete)
class Delete(Node):
	pass


@dynamic_extend(_ast.Dict)
class Dict(Node):
	pass


@dynamic_extend(_ast.DictComp)
class DictComp(Node):
	pass


@dynamic_extend(_ast.Div)
class Div(Node):
	pass


@dynamic_extend(_ast.Ellipsis)
class Ellipsis(Node):
	pass


@dynamic_extend(_ast.Eq)
class Eq(Node):
	pass


@dynamic_extend(_ast.ExceptHandler)
class ExceptHandler(Node):
	pass


@dynamic_extend(_ast.Exec)
class Exec(Node):
	pass


@dynamic_extend(_ast.Expr)
class Expr(Node):
	pass


@dynamic_extend(_ast.Expression)
class Expression(Node):
	pass


@dynamic_extend(_ast.ExtSlice)
class ExtSlice(Node):
	pass


@dynamic_extend(_ast.FloorDiv)
class FloorDiv(Node):
	pass


@dynamic_extend(_ast.For)
class For(Node):
	pass


@dynamic_extend(_ast.FunctionDef)
class FunctionDef(ScopeNode):
	pass


@dynamic_extend(_ast.GeneratorExp)
class GeneratorExp(Node):
	pass


@dynamic_extend(_ast.Global)
class Global(Node):
	pass


@dynamic_extend(_ast.Gt)
class Gt(Node):
	pass


@dynamic_extend(_ast.GtE)
class GtE(Node):
	pass


@dynamic_extend(_ast.If)
class If(Node):
	pass


@dynamic_extend(_ast.IfExp)
class IfExp(Node):
	pass


@dynamic_extend(_ast.Import)
class Import(Node):
	def __postinit__(self, parent):
		Node.__postinit__.im_func(self, parent)

		self.lookups = {alias.asname or alias.name: alias.name for alias in self.names}

	def lookup(self, name):
		name = self.lookups.get(name, '')
		return self.nModule().importModule(name) if name else None


@dynamic_extend(_ast.ImportFrom)
class ImportFrom(Node):
	def __postinit__(self, parent):
		Node.__postinit__.im_func(self, parent)
		self.lookups = {alias.asname or alias.name: alias.name for alias in self.names}

	def lookup(self, name):
		name = self.lookups.get(name, '')
		return self.nModule().importModule(self.module, fromlist=name, level=self.level) if name else None


@dynamic_extend(_ast.In)
class In(Node):
	pass


@dynamic_extend(_ast.Index)
class Index(Node):
	pass


@dynamic_extend(_ast.Interactive)
class Interactive(Node):
	pass


@dynamic_extend(_ast.Invert)
class Invert(Node):
	pass


@dynamic_extend(_ast.Is)
class Is(Node):
	pass


@dynamic_extend(_ast.IsNot)
class IsNot(Node):
	pass


@dynamic_extend(_ast.LShift)
class LShift(Node):
	pass


@dynamic_extend(_ast.Lambda)
class Lambda(ScopeNode):
	pass


@dynamic_extend(_ast.List)
class List(Node):
	pass


@dynamic_extend(_ast.ListComp)
class ListComp(Node):
	pass


@dynamic_extend(_ast.Load)
class Load(Node):
	pass


@dynamic_extend(_ast.Lt)
class Lt(Node):
	pass


@dynamic_extend(_ast.LtE)
class LtE(Node):
	pass


@dynamic_extend(_ast.Mod)
class Mod(Node):
	pass


@dynamic_extend(_ast.Module)
class Module(ScopeNode):
	def importModule(self, name, fromlist=None, level=-1):
		return ModuleLoader().load(name, fromlist, level, caller=self)

	def __postinit__(self, name, file, path):
		Node.__postinit__.im_func(self, None)
		self.__name__ = name
		self.__file__ = file
		self.__path__ = path

	def nModule(self):
		return self

	def load(self, name, only_locals=True):
		return self.scope.locals.get(name, None)


@dynamic_extend(_ast.Mult)
class Mult(Node):
	pass


@dynamic_extend(_ast.Name)
class Name(Node):
	def load(self, only_locals=True):
		return self.nScope().load(self.id, only_locals)


@dynamic_extend(_ast.Not)
class Not(Node):
	pass


@dynamic_extend(_ast.NotEq)
class NotEq(Node):
	pass


@dynamic_extend(_ast.NotIn)
class NotIn(Node):
	pass


@dynamic_extend(_ast.Num)
class Num(Node):
	pass


@dynamic_extend(_ast.Or)
class Or(Node):
	pass


@dynamic_extend(_ast.Param)
class Param(Node):
	pass


@dynamic_extend(_ast.Pass)
class Pass(Node):
	pass


@dynamic_extend(_ast.Pow)
class Pow(Node):
	pass


@dynamic_extend(_ast.Print)
class Print(Node):
	pass


@dynamic_extend(_ast.RShift)
class RShift(Node):
	pass


@dynamic_extend(_ast.Raise)
class Raise(Node):
	pass


@dynamic_extend(_ast.Repr)
class Repr(Node):
	pass


@dynamic_extend(_ast.Return)
class Return(Node):
	pass


@dynamic_extend(_ast.Set)
class Set(Node):
	pass


@dynamic_extend(_ast.SetComp)
class SetComp(Node):
	pass


@dynamic_extend(_ast.Slice)
class Slice(Node):
	pass


@dynamic_extend(_ast.Store)
class Store(Node):
	pass


@dynamic_extend(_ast.Str)
class Str(Node):
	pass


@dynamic_extend(_ast.Sub)
class Sub(Node):
	pass


@dynamic_extend(_ast.Subscript)
class Subscript(Node):
	pass


@dynamic_extend(_ast.Suite)
class Suite(Node):
	pass


@dynamic_extend(_ast.TryExcept)
class TryExcept(Node):
	pass


@dynamic_extend(_ast.TryFinally)
class TryFinally(Node):
	pass


@dynamic_extend(_ast.Tuple)
class Tuple(Node):
	pass


@dynamic_extend(_ast.UAdd)
class UAdd(Node):
	pass


@dynamic_extend(_ast.USub)
class USub(Node):
	pass


@dynamic_extend(_ast.UnaryOp)
class UnaryOp(Node):
	pass


@dynamic_extend(_ast.While)
class While(Node):
	pass


@dynamic_extend(_ast.With)
class With(Node):
	pass


@dynamic_extend(_ast.Yield)
class Yield(Node):
	pass
