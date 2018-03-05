++++++++++++++++++++++++++++++++
Python semantics and Limitations
++++++++++++++++++++++++++++++++

fatoptimizer bets that the Python code is not modified when modules are loaded,
but only later, when functions and classes are executed. If this assumption is
wrong, fatoptimizer changes the semantics of Python.

.. _semantics:

Python semantics
================

It is very hard, to not say impossible, to implementation and keep the exact
behaviour of regular CPython. CPython implementation is used as the Python
"standard". Since CPython is the most popular implementation, a Python
implementation must do its best to mimic CPython behaviour. We will call it the
Python semantics.

fatoptimizer should not change the Python semantics with the default
configuration.  Optimizations modifying the Python semantics must be disabled
by default: opt-in options.

As written above, it's really hard to mimic exactly CPython behaviour. For
example, in CPython, it's technically possible to modify local variables of a
function from anywhere, a function can modify its caller, or a thread B can
modify a thread A (just for fun). See `Everything in Python is mutable
<https://faster-cpython.readthedocs.io/mutable.html>`_ for more information.
It's also hard to support all introspections features like ``locals()``
(``vars()``, ``dir()``), ``globals()`` and
``sys._getframe()``.

Builtin functions replaced in the middle of a function
======================================================

fatoptimizer uses :ref:`guards <guard>` to disable specialized function when
assumptions made to optimize the function are no more true. The problem is that
guard are only called at the entry of a function. For example, if a specialized
function ensures that the builtin function ``chr()`` was not modified, but
``chr()`` is modified during the call of the function, the specialized function
will continue to call the old ``chr()`` function.

The :ref:`copy builtin functions to constants <copy-builtin-to-constant>`
optimization changes the Python semantics. If a builtin function is replaced
while the specialized function is optimized, the specialized function will
continue to use the old builtin function. For this reason, the optimization
is disabled by default.

Example::

    def func(arg):
        x = chr(arg)

        with unittest.mock.patch('builtins.chr', result='mock'):
            y = chr(arg)

        return (x == y)

If the :ref:`copy builtin functions to constants
<copy-builtin-to-constant>` optimization is used on this function, the
specialized function returns ``True``, whereas the original function returns
``False``.

It is possible to work around this limitation by adding the following
:ref:`configuration <config>` at the top of the file::

    __fatoptimizer__ = {'copy_builtin_to_constant': False}

But the following use cases works as expected in FAT mode::

    import unittest.mock

    def func():
        return chr(65)

    def test():
        print(func())
        with unittest.mock.patch('builtins.chr', return_value="mock"):
            print(func())

Output::

    A
    mock

The ``test()`` function doesn't use the builtin ``chr()`` function.
The ``func()`` function checks its guard on the builtin ``chr()`` function only
when it's called, so it doesn't use the specialized function when ``chr()``
is mocked.


Guards on builtin functions
===========================

When a function is specialized, the specialization is ignored if a builtin
function was replaced after the end of the Python initialization. Typically,
the end of the Python initialization occurs just after the execution of the
``site`` module. It means that if a builtin is replaced during Python
initialization, a function will be specialized even if the builtin is not the
expected builtin function.

Example::

    import builtins

    builtins.chr = lambda: mock

    def func():
        return len("abc")

In this example, the ``func()`` is optimized, but the function is *not*
specialize. The internal call to ``func.specialize()`` is ignored because the
``chr()`` function was replaced after the end of the Python initialization.


Guards on type dictionary and global namespace
===============================================

For other guards on dictionaries (type dictionary, global namespace), the guard
uses the current value of the mapping. It doesn't check if the dictionary value
was "modified".


Tracing and profiling
=====================

Tracing and profiling works in FAT mode, but the exact control flow and traces
are different in regular and FAT mode. For example, :ref:`loop unrolling
<loop-unroll>` removes the call to ``range(n)``.

See ``sys.settrace()`` and ``sys.setprofiling()`` functions.


Expected limitations
====================

Function inlining optimization makes debugging more complex:

* sys.getframe()
* locals()
* pdb
* etc.
* don't work as expected anymore

Bugs, shit happens:

* Missing guard: specialized function is called even if the "environment"
  was modified

FAT python! Memory vs CPU, fight!

* Memory footprint: loading two versions of a function is memory uses more
  memory
* Disk usage: .pyc will be more larger

Possible worse performance:

* guards adds an overhead higher than the optimization of the specialized code
* specialized code may be slower than the original bytecode
