+++++++++++++++++++
fatoptimizer module
+++++++++++++++++++

fatoptimizer API
================

.. warning::
   The API is not stable yet.

``fatoptimizer.__version__`` is the module version string (ex: ``'0.3'``).

.. function:: optimize(tree, filename, config)

   Optimize an AST tree. Return the optimized AST tree.


.. function:: pretty_dump(node, annotate_fields=True, include_attributes=False, lineno=False, indent='  ')

   Return a formatted dump of the tree in *node*.  This is mainly useful for
   debugging purposes.  The returned string will show the names and the values
   for fields.  This makes the code impossible to evaluate, so if evaluation is
   wanted *annotate_fields* must be set to False.  Attributes such as line
   numbers and column offsets are not dumped by default.  If this is wanted,
   *include_attributes* can be set to True.


.. class:: Config

   Configuration of the optimizer.

   See :ref:`fatoptimizer configuration <config>`.


.. class:: FATOptimizer(config)

   Code transformers for ``sys.set_code_transformers()``.


.. class:: OptimizerError

   Exception raised on bugs in the optimizer.


Installation
============

The :ref:`fatoptimizer module <fatoptimizer>` requires a Python 3.6 patched
with `PEP 510 "Specialize functions with guards"
<https://www.python.org/dev/peps/pep-0510/>`_ and `PEP 511 "API for code
transformers" <https://www.python.org/dev/peps/pep-0511/>`_ patches.

Type::

    pip install fatoptimizer

Manual installation::

    python3.6 setup.py install

Optimized code requires the :ref:`fat module <fat>` at runtime if at least one
function is specialized.


.. _config:

Configuration
=============

It is possible to configure the AST optimizer per module by setting
the ``__fatoptimizer__`` variable. Configuration keys:

* ``enabled`` (``bool``): set to ``False`` to disable all optimization (default: true)

* ``constant_propagation`` (``bool``): enable :ref:`constant propagation <const-prop>`
  optimization? (default: true)

* ``constant_folding`` (``bool``): enable :ref:`constant folding
  <const-fold>` optimization? (default: true)

* ``copy_builtin_to_constant`` (``bool``): enable :ref:`copy builtin functions
  to constants <copy-builtin-to-constant>` optimization? (default: false)

* ``inlining`` (``bool``): enable :ref:`function inlining
  <inlining>` optimization? (default: false)

* ``remove_dead_code`` (``bool``): enable :ref:`dead code elimination
  <dead-code>` optimization? (default: true)

* maximum size of constants:

  - ``max_bytes_len``: Maximum number of bytes of a text string (default: 128)
  - ``max_int_bits``: Maximum number of bits of an integer (default: 256)
  - ``max_str_len``: Maximum number of characters of a text string (default: 128)
  - ``max_seq_len``: Maximum length in number of items of a sequence like
    tuples (default: 32). It is only a preliminary check: ``max_constant_size``
    still applies for sequences.
  - ``max_constant_size``: Maximum size in bytes of other constants
    (default: 128 bytes), the size is computed with ``len(marshal.dumps(obj))``

* ``replace_builtin_constant`` (``bool``): enable :ref:`replace builtin
  constants <replace-builtin-constant>` optimization? (default: true)

* ``simplify_iterable`` (``bool``): enable :ref:`simplify iterable optimization
  <simplify-iterable>`? (default: true)

* ``unroll_loops``: Maximum number of loop iteration for loop unrolling
  (default: ``16``). Set it to ``0`` to disable loop unrolling. See
  :ref:`loop unrolling <loop-unroll>` and :ref:`simplify comprehension <compr>`
  optimizations.

Example to disable all optimizations in a module::

    __fatoptimizer__ = {'enabled': False}

Example to disable the constant folding optimization::

    __fatoptimizer__ = {'constant_folding': False}

See the :class:`Config` class.


Run tests
=========

Type::

    tox

You may need to install or update tox::

    pip3 install -U tox

Run manually tests::

    python3 test_fatoptimizer.py

There are also integration tests which requires a Python 3.6 with patches PEP
509, PEP 510 and PEP 511. Run integration tests::

    python3.6 -X fat test_fat_config.py
    python3.6 -X fat test_fat_size.py
