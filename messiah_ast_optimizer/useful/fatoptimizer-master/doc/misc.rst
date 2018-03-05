++++
Misc
++++

Implementation
==============

Steps and stages
----------------

The optimizer is splitted into multiple steps. Each optimization has its own
step: fatoptimizer.const_fold.ConstantFolding implements for example constant
folding.

The function optimizer is splitted into two stages:

* stage 1: run steps which don't require function specialization
* stage 2: run steps which can add guard and specialize the function

Main classes:

* ModuleOptimizer: Optimizer for ast.Module nodes. It starts by looking for
  :ref:`__fatoptimizer__ configuration <config>`.
* FunctionOptimizer: Optimizer for ast.FunctionDef nodes. It starts by running
  FunctionOptimizerStage1.
* Optimizer: Optimizer for other AST nodes.

Steps used by ModuleOptimizer, Optimizer and FunctionOptimizerStage1:

* NamespaceStep: populate a Namespace object which tracks the local variables,
  used by ConstantPropagation
* ReplaceBuiltinConstant: replace builtin optimization
* ConstantPropagation: constant propagation optimization
* ConstantFolding: constant folding optimization
* RemoveDeadCode: dead code elimitation optimization

Steps used by FunctionOptimizer:

* NamespaceStep: populate a Namespace object which tracks the local variables
* UnrollStep: loop unrolling optimization
* CallPureBuiltin: call builtin optimization
* CopyBuiltinToConstantStep: copy builtins to constants optimization

Some optimizations produce a new AST tree which must be optimized again. For
example, loop unrolling produces new nodes like "i = 0" and duplicates the loop
body which uses "i". We need to rerun the optimizer on this new AST tree to run
optimizations like constant propagation or constant folding.


Pure functions
==============

A "pure" function is a function with no side effect.

Example of pure operators:

* x+y, x-y, x*y, x/y, x//y, x**y for types int, float, complex, bytes, str,
  and also tuple and list for x+y

Example of instructions with side effect:

* "global var"

Example of pure function::

    def mysum(x, y):
        return x + y

Example of function with side effect::

    global _last_sum

    def mysum(x, y):
        global _last_sum
        s = x + y
        _last_sum = s
        return s


Constants
=========

FAT Python introduced a new AST type: ``ast.Constant``. The optimizer starts by
converting ``ast.NameConstant``, ``ast.Num``, ``ast.Str``, ``ast.Bytes`` and
``ast.Tuple`` to ``ast.Constant``. Later, it can create constant of other
types. For example, ``frozenset('abc')`` creates a ``frozenset`` constant.

Supported constants:

* ``None`` singleton
* ``bool``: ``True`` and ``False``
* numbers: ``int``, ``float``, ``complex``
* strings: ``bytes``, ``str``
* containers:  ``tuple``, ``frozenset``


Literals
========

Literals are a superset of constants.

Supported literal types:

* (all constant types)
* containers: ``list``, ``dict``, ``set``


FunctionOptimizer
=================

``FunctionOptimizer`` handles ``ast.FunctionDef`` and emits a specialized
function if a call to a builtin function can be replaced with its result.

For example, this simple function::

    def func():
        return chr(65)

is optimized to::

    def func():
        return chr(65)

    _ast_optimized = func

    def func():
        return "A"
    _ast_optimized.specialize(func,
                              [{'guard_type': 'builtins', 'names': ('chr',)}])

    func = _ast_optimized
    del _ast_optimized


Detection of free variables
===========================

VariableVisitor detects local and global variables of an ``ast.FunctionDef``
node. It is used by the ``FunctionOptimizer`` to detect free variables.


Corner cases
============

Calling the ``super()`` function requires a cell variables.
