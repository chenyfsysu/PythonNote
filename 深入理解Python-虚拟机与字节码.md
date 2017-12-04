### 一、Python执行原理
Python的执行过程大概可以分为编译与解释两个过程。等等，Python不是一门解释型语言吗，为什么还要进行编译过程。
事实上，Python是会有编译过程，但是Python的编译和C/C++的编译不完全等价。C/C++编译是将高级语言翻译成机器能读懂的机器代码。而Python编译的思想也是一样的，但是不是编译成机器代码，而是编译成C语言更容易读懂的字节码(bytecode)。Python的编译过程主要是为了加速运行时代码的解释速度，提高Python的运行效率。如果执行每行代码都要经过词法分析、语法分析、AST建立等过程，那执行效率可想而知是有多慢的。而解释过程，则是Python虚拟机读取编译后的字节码，逐条执行所有的字节码。
### 二、PyCodeObject字节码对象
前面提到Python程序执行时会先将Python代码编译成字节码序列，然后交由虚拟机执行。而字节码对象在内存中的表示则是PyCodeObject对象，它的定义如下：
``` c
/* Bytecode object */
typedef struct {
    PyObject_HEAD
    int co_argcount;		/* #arguments, except *args */
    int co_nlocals;		/* #local variables */
    int co_stacksize;		/* #entries needed for evaluation stack */
    int co_flags;		/* CO_..., see below */
    PyObject *co_code;		/* instruction opcodes */
    PyObject *co_consts;	/* list (constants used) */
    PyObject *co_names;		/* list of strings (names used) */
    PyObject *co_varnames;	/* tuple of strings (local variable names) */
    PyObject *co_freevars;	/* tuple of strings (free variable names) */
    PyObject *co_cellvars;      /* tuple of strings (cell variable names) */
    /* The rest doesn't count for hash/cmp */
    PyObject *co_filename;	/* string (where it was loaded from) */
    PyObject *co_name;		/* string (name, for reference) */
    int co_firstlineno;		/* first source line number */
    PyObject *co_lnotab;	/* string (encoding addr<->lineno mapping) See
				   Objects/lnotab_notes.txt for details. */
    void *co_zombieframe;     /* for optimization only (see frameobject.c) */
    PyObject *co_weakreflist;   /* to support weakrefs to code objects */
} PyCodeObject;
```
可以看到PyCodeObject中保存了
### 三、Python虚拟机架构
在编译了代码称谓字节码后，Python虚拟机就会接管后面程序的执行。在
``` c
typedef struct _frame {
    PyObject_VAR_HEAD
    struct _frame *f_back;	/* previous frame, or NULL */
    PyCodeObject *f_code;	/* code segment */
    PyObject *f_builtins;	/* builtin symbol table (PyDictObject) */
    PyObject *f_globals;	/* global symbol table (PyDictObject) */
    PyObject *f_locals;		/* local symbol table (any mapping) */
    PyObject **f_valuestack;	/* points after the last local */
    PyObject **f_stacktop;
    PyObject *f_trace;		/* Trace function */
    PyObject *f_exc_type, *f_exc_value, *f_exc_traceback;

    PyThreadState *f_tstate;
    int f_lasti;		/* Last instruction if called */
    int f_lineno;		/* Current line number */
    int f_iblock;		/* index in f_blockstack */
    PyTryBlock f_blockstack[CO_MAXBLOCKS]; /* for try and loop blocks */
    PyObject *f_localsplus[1];	/* locals+stack, dynamically sized */
} PyFrameObject;
```
### 四、字节码
Python中所有的字节码类型都定义在opcode中，可以看到一共有117种字节码类型，包含了存储属性、读取常量、创建dict、创建tuple、创建list等基本操作。
``` c
/* Instruction opcodes for compiled code */

#define STORE_ATTR	95	/* Index in name list */
#define DELETE_ATTR	96	/* "" */
#define STORE_GLOBAL	97	/* "" */
#define DELETE_GLOBAL	98	/* "" */
#define DUP_TOPX	99	/* number of items to duplicate */
#define LOAD_CONST	100	/* Index in const list */
#define LOAD_NAME	101	/* Index in name list */
#define BUILD_TUPLE	102	/* Number of tuple items */
#define BUILD_LIST	103	/* Number of list items */
#define BUILD_SET	104     /* Number of set items */
#define BUILD_MAP	105	/* Always zero for now */
#define LOAD_ATTR	106	/* Index in name list */
#define COMPARE_OP	107	/* Comparison operator */
#define IMPORT_NAME	108	/* Index in name list */
#define IMPORT_FROM	109	/* Index in name list */
#define JUMP_FORWARD	110	/* Number of bytes to skip */
...
```

### 五、字节码执行
``` c
PyObject *PyEval_EvalFrameEx(PyFrameObject *f, int throwflag)
{
    for (;;)
    {
         switch (opcode) {
            TARGET(LOAD_CONST)
            {
                x = GETITEM(consts, oparg);
                Py_INCREF(x);
                PUSH(x);
                FAST_DISPATCH();
            }
            ...
        }
    }
}
```