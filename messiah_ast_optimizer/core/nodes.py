# -*- coding:utf-8 -*-
"""
动态拓展原生AstNode
"""

import _ast
import inspect
import itertools
import builtin
import inspect

from module_loader import ModuleLoader
from const import NT_LOCAL, NT_GLOBAL_IMPLICIT, NT_GLOBAL_EXPLICIT, NT_FREE, NT_CELL, NT_UNKNOWN
from exception import MMroResolutionException, MUnpackSequenceException, MEvalException
from eval import PyFrame


def dynamic_extend(cls):
	def _dynamic_extend(klass):
		for name, func in inspect.getmembers(klass, inspect.ismethod):
			setattr(cls, name, func.im_func)
		cls.__excls__ = klass

	return _dynamic_extend


class Node(object):

	def __preinit__(self, parent):
		self.parent = parent
		self.n_isconstant = False
		self.n_use_pscope = False

	def __postinit__(self):
		pass

	def release(self):
		self.parent = None

	def clone(self):
		fields = {}

		for field in self._fields:
			val = getattr(self, field)
			fields[field] = val.clone() if isinstance(val, _ast.AST) else val

		return self.__class__(**fields)

	def eval(self, *args):
		raise MEvalException('Node Class of %s did not define eval function' % self.__class__.__name__)

	def getattr(self, name):
		raise MEvalException('Node Class of %s did not define getattr function' % self.__class__.__name__)

	def nModule(self):
		module = self
		while module.parent:
			module = module.parent

		return module

	def isScope(self):
		return issubclass(self.__excls__, ScopeNode)

	def isNamespaceProvider(self):
		return issubclass(self.__excls__, NamespaceProvider)

	def nScope(self):
		scope, n_use_pscope = self, self.n_use_pscope
		while scope and (not scope.isScope() or n_use_pscope):
			scope = scope.parent
			if scope.isScope() and n_use_pscope:
				scope = scope.parent
				n_use_pscope = False
			if scope.n_use_pscope:
				n_use_pscope = scope.n_use_pscope

		return scope

	def nFrame(self):
		pass

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
		self.n_isconstant = True
		self.n_val = val


class ScopeNode(Node):
	def __preinit__(self, parent):
		Node.__preinit__.im_func(self, parent)

	def release(self):
		Node.release(self)
		self.scope = None

	def load(self, name, only_locals=True):
		sc = self.scope.identify(name)
		if sc == NT_LOCAL:
			return self._load(name, self.scope.locals.get(name, None))
		if not only_locals and sc in (NT_GLOBAL_EXPLICIT, NT_GLOBAL_IMPLICIT):
			return self.nModule().load(name)

		return None

	def _load(self, name, node):
		return node.lookup(name) if node and node.isNamespaceProvider() else node


class FrameNode(object):
	def __preinit__(self):
		pass


class NamespaceProvider(object):
	def lookup(self, name):
		raise NotImplementedError


@dynamic_extend(_ast.alias)
class alias(Node):
	
	def inferName(self):
		name, asname = self.name, self.asname
		return asname or (name[:name.find('.')] if '.' in name else name)


@dynamic_extend(_ast.arguments)
class arguments(Node):
	
	def needArgs(self):
		return any((self.args, self.vararg, self.kwarg, self.defaults))

	def argsFlag(self):
		return len(self.args), self.vararg is None, self.kwarg is None

	def unpackPosArgs(self, callsite, is_method=False):
		pos_args = {}
		bias = 1 if is_method else 0
		if len(callsite.args) + bias > len(self.args):
			raise TypeError('too many arguments provied')

		if is_method:
			if not isinstance(callsite.func, _ast.Attribute):
				raise TypeError('call method with no instance')

			pos_args[self.args[0].id] = callsite.func.value

		for idx, arg in enumerate(callsite.args):
			pos_args[self.args[idx + bias].id] = arg

		for keyword in callsite.keywords:
			if keyword.arg in pos_args:
				raise TypeError('arguments of %s already provied' % keyword.arg)

			pos_args[keyword.arg] = keyword.value

		return pos_args


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
	def eval(self, frame):
		return [self.arg, self.value.eval(frame)]


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
class Assign(Node, NamespaceProvider):
	def __preinit__(self, parent):
		Node.__preinit__.im_func(self, parent)

	def __postinit__(self):
		self.n_lookups = {}
		self.evalLookup()

	def evalLookup(self):
		
		for i, target in enumerate(self.targets):
			import astunparse

			lookups = self.unpackSequence(target, self.value)
			self.n_lookups.update(lookups)

	def unpackSequence(self, target, val):
		if isinstance(target, _ast.Name):
			return {target.id : val}
		elif isinstance(target, (_ast.List, _ast.Tuple)):
			if val is None:
				items = {}
				for t in target.elts:
					items.update(self.unpackSequence(t, None))
				return items

			if not isinstance(val, (_ast.List, _ast.Tuple)):
				return self.unpackSequence(target, None)
			
			if val and len(target.elts) != len(val.elts):
				raise MUnpackSequenceException('ValueError: unpack sequence of targets and value do not match')

			items = {}
			for t, v in zip(target.elts, val.elts):
				items.update(self.unpackSequence(t, v))

			return items
		else:
			return {}

	def lookup(self, name):
		return self.n_lookups.get(name, None)


@dynamic_extend(_ast.Attribute)
class Attribute(Node):
	
	def eval(self, frame):
		if isinstance(self.ctx, _ast.Store):
			raise MEvalException('cannot eval Attribute with ctx Store')

		return self.value.eval(frame).getattr(self.attr)


@dynamic_extend(_ast.AugAssign)
class AugAssign(Node, NamespaceProvider):
	def lookup(self, name):
		return None


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
	def eval(self, frame):
		func = self.func.eval(frame)

		if isinstance(func, _ast.FunctionDef):
			return self._eval(frame, func)
		elif getattr(func, '__builtin_delegate__', False):
			return self._evalDelegate(frame, func)
		else:
			raise MEvalException('cannot eval Call with NonFunctionDef or BuiltinDelegate')

	def _eval(self, frame, func):
		if any([self.args, self.keywords, self.starargs, self.kwargs]):
			raise MEvalException('cannot eval Call with arguments')

		if any((cell not in frame.f_cells for cell in func.scope.cells())):
			raise MEvalException('closure was not given, eval call cannot continue')

		# args = [arg.eval(frame) for arg in self.args]
		# keywords = [kw.eval(frame) for kw in self.keywords]
		# starargs = self.starargs.eval(frame) if self.starargs else None
		# kwargs = self.kwargs.eval(frame) if self.kwargs else None

		return func.eval(frame)

	def _evalDelegate(self, frame, func):
		posargs, keyargs = self._evalArgs(frame)

		return func(frame, *posargs, **keyargs)

	def _evalArgs(self, frame):
		posargs = [arg.eval(frame) for arg in self.args]
		keyargs = dict([kw.eval(frame) for kw in self.keywords])

		if self.starargs:
			starargs = self.starargs.eval(frame)
			posargs.extend(starargs)

		if self.kwargs:		
			kwargs = self.kwargs.eval(frame)
			keyargs.update(kwargs)

		return posargs, keyargs


@dynamic_extend(_ast.ClassDef)
class ClassDef(ScopeNode):
	def nMro(self):
		mro = [self]
		seqs = [seq.nMro() for seq in self.nBases() if seq]
		while True:
			seqs = filter(None, seqs)
			if not seqs:
				break

			for seq in seqs:
				merge = seq[0]
				if any(s for s in seqs if merge in s[1:]):
					merge = None
				else:
					break
			if not merge:
				raise MMroResolutionException('Cannot create consistent method resolution')
			mro.append(merge)
			for seq in seqs:
				merge in seq and seq.remove(merge)

		return mro

	def nBases(self):
		bases = []
		for base in self.bases:
			if isinstance(base, _ast.Name):
				not base.isBuiltinObject() and bases.append(base.load())
			elif isinstance(base, _ast.Attribute):
				pass
		return bases

	def nFullBases(self):
		fullbases = []
		for bases in self.nBases():
			fullbases.append(bases)
			fullbases.extend(bases.nFullBases())
		return fullbases

	def nMethods(self):
		pass

	def nFullMethods(self, mro=None):
		if not mro:
			mro = self.nMro()

	def nAttrs(self):
		pass

	def nFullAttrs(self):
		pass

	def isbaseclass(self, node):
		if not isinstance(node, _ast.ClassDef):
			return False

		return node in self.nFullBases()

	def getmembers(self):
		methods, attrs =  {}, []
		for body in self.body:
			if isinstance(body, _ast.FunctionDef):
				methods[body.name] = body
			elif isinstance(body, (_ast.Assign, _ast.AugAssign)):
				attrs.append(body)

		return methods, attrs

	def fullGetmembers(self, mro=None):
		if not mro:
			mro = self.nMro()

		methods, attrs = {}, []
		for cls in reversed(mro):
			_methods, _attrs = cls.getmembers()
			methods.update(_methods)
			attrs.extend(_attrs)

		return methods, attrs

	def getbodies(self, predicate=None):
		bodies = [body for body in self.body if not predicate or predicate(body)]
		return bodies

	def fullGetbodies(self, mro=None, predicate=None):
		return [body for base in mro for body in base.getbodies(predicate)]


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
	def __postinit__(self):
		self.py_func = None

	def eval(self, frame):
		if self.decorator_list:
			raise MEvalException('cannot eval FunctionDef with decorator_list')

		if self.args.needArgs():
			raise MEvalException('cannot eval FunctionDef with arguments')

		frame = PyFrame({}, self.nModule().scope.locals, builtin.Builtin.get())

		for body in self.body:
			result = body.eval(frame)
			if isinstance(body, _ast.Return):
				return result

	def evalCall(self, args, keywords, starargs, kwargs):
		pass

	def getCallArgs(self, args, keywords, starargs, kwargs):
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
class Import(Node, NamespaceProvider):
	def __preinit__(self, parent):
		Node.__preinit__.im_func(self, parent)

	def __postinit__(self):
		self.as_lookups = {}
		for alias in self.names:
			if alias.asname:
				self.as_lookups[alias.asname] = alias.name

	def lookup(self, name):
		name = self.as_lookups[name] if name in self.as_lookups else name
		return self.nModule().importModule(name) if name else None

	def findModule(self, name):
		return self.nModule().findModule(name)


@dynamic_extend(_ast.ImportFrom)
class ImportFrom(Node, NamespaceProvider):
	def __preinit__(self, parent):
		Node.__preinit__.im_func(self, parent)

	def __postinit__(self):
		self.as_lookups = {}
		for alias in self.names:
			if alias.asname:
				self.as_lookups[alias.asname] = alias.name

	def lookup(self, name):
		name = self.as_lookups[name] if name in self.as_lookups else name
		return self.nModule().importModule(self.module, fromlist=name, level=self.level or -1) if name else None

	def findModule(self):
		return self.nModule().findModule(self.module, level=self.level or -1)


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

	def findModule(self, name, level=-1):
		return ModuleLoader().load(name, fromlist=None, level=level, caller=self, lazy=True)

	def __preinit__(self, name, file, path, internal=False, incomplete=False):
		Node.__preinit__.im_func(self, None)
		self.__name__ = name
		self.__file__ = file
		self.__path__ = path
		self.__internal__ = internal
		self.__incomplete__ = incomplete

	def getattr(self, name):
		if name not in self.scope.locals:
			raise MEvalException('Module object has no attribute %s' % name)

		return self.scope.locals[name]

	def nModule(self):
		return self

	def load(self, name, only_locals=True):
		return self._load(name, self.scope.locals.get(name, None))


@dynamic_extend(_ast.Mult)
class Mult(Node):
	pass


@dynamic_extend(_ast.Name)
class Name(Node):
	def isBuiltinObject(self):
		return self.id == 'object'

	def load(self, only_locals=True):
		return self.nScope().load(self.id, only_locals)

	def eval(self, frame):
		if not isinstance(self.ctx, _ast.Load):
			raise MEvalException('Eval name of Store type')

		ref = None
		nt = self.nScope().scope.identify(self.id)
		if nt == NT_LOCAL:
			ref = frame.loadName(self.id)
		elif nt == NT_FREE:
			ref = frame.loadDeref(self.id)
		elif nt in (NT_GLOBAL_IMPLICIT, NT_GLOBAL_EXPLICIT):
			ref = frame.loadGlobal(self.id)

		if not ref:
			raise MEvalException('Cannot Load name %s' % self.id)

		if getattr(ref, '__builtin_delegate__', False):
			return ref

		if issubclass(ref.__excls__, NamespaceProvider):
			return ref.lookup(self.id)

		return ref


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
	def eval(self, frame):
		return self


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
	def eval(self, frame):
		return self.value.eval(frame)


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
	def eval(self, frame):
		return self

	def asConstant(self):
		return self.s


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
	def eval(self, frame):
		if isinstance(self.ctx, _ast.Store):
			raise MEvalException('eval name of Store type')

		return tuple([elt.eval(frame) for elt in self.elts])


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
