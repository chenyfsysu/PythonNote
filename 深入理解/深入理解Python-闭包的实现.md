### 一、一个Python坑
对于Python新手，这个坑一定都踩过

``` python
def print_sth(a):
    print a   
def do_sth():
  callback = []
  for i in xrange(5):
    callback.append(lambda : print_sth(i))

  for cb in callback:
    cb()
```
在一个循环中通过设置闭包(lambda)回调，这里我们期望的是在回调时打印**0,1,2,3,4**，但是令人失望的是打印的是**4,4,4,4,4**。Python的闭包是怎么实现的，为什么会遇到这样的问题？

### 二、从Python层面
在闭包中可以引用外层函数的变量，在上面例子中是引用了i，那么这个i一定保存在什么地方，等调用闭包时再读取。首先我们想到，i会不会保存在外层函数**do_sth**中。通过dir()指令可以看某个对象的所有属性内容，外层函数**do_sth**是一个函数也是一个对象（万物皆对象），当然也可以通过**dir**查看属性内容。
``` python
[.... 'func_closure', 'func_code', 'func_defaults', 'func_dict', 'func_doc', 'func_globals', 'func_name']
```
一堆func开头的的属性引起了我们的注意，**func_closure**更是格外显目。**closure**不正是闭包的意思吗，这里面的内容一定和闭包紧密相关。我们尝试打印打印**do_sth**的**func_closure**的内容，遗憾的是居然是**None**。再仔细想想，**do_sth**只是外层函数，而**lambda**才是闭包，所以闭包的内容会不会在lambda（闭包）函数中。打印闭包的**func_closure**内容（可以把闭包用变量保存，再使用dis函数），果然在这里发现了特别的内容:

``` python
(<cell at 0x024FD730: int object at 0x004AA9E4>,)
```
这里有两个关键字**int**和**cell**，闭包引用的变量i正是一个**int**类型，看到这里我们更加肯定**func_closure**的内容就是闭包引用的内容。但是**cell**的是什么呢？在Python层面已经很难解答这个问题了，我们必须要进一步深入到Python解释器的层面才能进行解答。
### 三、闭包实现的字节码
和之前一样，我们想要深入理解Python某个内容实现，字节码是一个再好不过的切入点。通过dis函数可以查看外层函数**do_sth**和闭包**lambda**的字节码：
``` python
# do_sth的字节码
             ....
             22 STORE_DEREF              0 (i)
             ...
  8          25 LOAD_CLOSURE             0 (i)
             28 BUILD_TUPLE              1
             31 LOAD_CONST               2 (<code object <lambda> at 01CF6B18, file main.py>)
             34 MAKE_CLOSURE             0
             37 STORE_FAST               1 (cb)
        
# 闭包函数的字节码
 8           0 LOAD_GLOBAL              0 (print_item)
             3 LOAD_DEREF               0 (i)
             6 CALL_FUNCTION            1
```
我们关注到4个特殊的字节码：**STORE_DEREF**、**LOAD_CLOSURE**、**MAKE_CLOSURE**、**LOAD_DEREF**。从字节码的意思来看，这个四个字节码做的内容也很清晰了：
> * STORE_DEREF：外层函数保存闭包使用的变量内容
> * LOAD_CLOSURE：获取所有的必要使用的变量内容
> * MAKE_CLOSURE：创建闭包函数
> * LOAD_DEREF：内层函数获取完成函数的变量内容

到这一步，已经对闭包的实现流程已经有了大概的宏观的理解：创建闭包时，会把闭包的使用的变量内容保存在闭包函数内。接下来再深入到每个字节码的实现，闭包的问题就能游刃而解了。
#### 1）STORE_DEREF

``` cpp
TARGET(STORE_DEREF)
{
    w = POP();
    x = freevars[oparg];
    PyCell_Set(x, w);
    Py_DECREF(w);
    DISPATCH();
}
```

#### 2）LOAD_CLOSURE
``` cpp
TARGET(LOAD_CLOSURE)
{
    x = freevars[oparg];
    Py_INCREF(x);
    PUSH(x);
    if (x != NULL) DISPATCH();
    break;
}
```
#### 3）MAKE_CLOSURE

``` cpp
TARGET(MAKE_CLOSURE)
{
    v = POP(); /* code object */
    x = PyFunction_New(v, f->f_globals);
    Py_DECREF(v);
    if (x != NULL) {
        v = POP();
        if (PyFunction_SetClosure(x, v) != 0) {
            /* Can't happen unless bytecode is corrupt. */
            why = WHY_EXCEPTION;
        }
        Py_DECREF(v);
    }
    ...
}
```
#### 4）LOAD_DEREF

``` cpp
TARGET(LOAD_DEREF)
{
    x = freevars[oparg];
    w = PyCell_Get(x);
    if (w != NULL) {
        PUSH(w);
        DISPATCH();
    }
    ...
}
```
从字节码的源码实现上看，这四个字节码的实现内容和我们上面的猜想是一致的。**STORE_DEREF**外层函数保存闭包使用内容，**LOAD_CLOSURE**获取所有使用内容用于创建闭包，**MAKE_CLOSURE**创建闭包，**LOAD_DEREF**是闭包函数获取使用内容。这几个字节码都很简单，我们注意到**MAKE_CLOSURE**的保存闭包使用的内容的函数**PyFunction_SetClosure(x, v)**, 它的实现是：
``` cpp
int PyFunction_SetClosure(PyObject *op, PyObject *closure)
{
    ...
    Py_XSETREF(((PyFunctionObject *)op)->func_closure, closure);
    return 0;
}
```
可以看到它正是保存到函数对象的**func_closure**中，这也验证了我们在脚本层查看的内容。而接下来的内容只有一个，保存到闭包中的引用内容到底保存了什么？我们看到外层函数保存和闭包函数获取的实现是**PyCellGet**和**PyCellSet**：

``` cpp
PyObject *PyCell_Get(PyObject *op)
{
    if (!PyCell_Check(op)) {
        PyErr_BadInternalCall();
        return NULL;
    }
    Py_XINCREF(((PyCellObject*)op)->ob_ref);
    return PyCell_GET(op);
}

int PyCell_Set(PyObject *op, PyObject *obj)
{
    PyObject* oldobj;
    if (!PyCell_Check(op)) {
        PyErr_BadInternalCall();
        return -1;
    }
    oldobj = PyCell_GET(op);
    Py_XINCREF(obj);
    PyCell_SET(op, obj);
    Py_XDECREF(oldobj);
    return 0;
}
```
可以看到**PyCellGet**和**PyCellSet**都共同指向了一个内容：**PyCellObject**!

### 五、PyCellObject
接下来就进入**PyCellObject**, 它的声明简单：
``` cpp
typedef struct {
  PyObject_HEAD
  PyObject *ob_ref; /* Content of the cell or NULL when empty */
} PyCellObject;
```
我们关注到一个重要信息**ob_ref**，ref是引用的意思吗？再回头看**PyCell_Set**, 它的真正实现是**PyCell_SET**：
``` cpp
#define PyCell_SET(op, v) (((PyCellObject *)(op))->ob_ref = v)
```
果然**ob_ref**是保存了对外层函数变量的引用，**PyCell_SET**把引用的内容保存在**PyCellObject**的**ob_ref**中，引用的时候也通过**Py_XINCREF(obj)**增加了引用计数。看到这里一下子豁然开朗了，第一节提到的Python的坑也得到了解决：**因为闭包函数中保存的是对外层函数变量的引用**。在第一节中通过for循环生成闭包函数，实际上他们引用的内容都是同一个：**i**！而经过for循环后，它的值正是4，所以每个lambda的打印值都是4。

## 六、co_cellvars和co_freevars
上面已经了解到了闭包引用的内容的保存，读取，也知道了保存的什么内容。但是还有一个疑问：怎么决定要保存什么内容到**func_closure**上？显示把外层函数的所有变量都保存是不切实际的，我们很容易想到闭包函数要用到什么内容就保存什么内容。那这个在源码中是怎么实现的呢？再回到字节码**STORE_DEREF**和**LOAD_DEREF**的实现中，我们在之前忽略了一个内容：取出cell是在：**x = freevars[oparg]**，那freevars是什么？看到前面**freevars**的定义中：
``` cpp
for (i = 0; i < PyTuple_GET_SIZE(co->co_cellvars); ++i) {
    cellname = PyString_AS_STRING(
        PyTuple_GET_ITEM(co->co_cellvars, i));
    found = 0;
    for (j = 0; j < nargs; j++) {
        argname = PyString_AS_STRING(
            PyTuple_GET_ITEM(co->co_varnames, j));
        if (strcmp(cellname, argname) == 0) {
            c = PyCell_New(GETLOCAL(j));
            if (c == NULL)
                goto fail;
            GETLOCAL(co->co_nlocals + i) = c;
            found = 1;
            break;
        }
    }
    if (found == 0) {
        c = PyCell_New(NULL);
        if (c == NULL)
            goto fail;
        SETLOCAL(co->co_nlocals + i, c);
    }
}
}
```
``` cpp
typedef struct {
  ...
    PyObject *co_freevars;  /* tuple of strings (free variable names) */
    PyObject *co_cellvars;      /* tuple of strings (cell variable names) */
} PyCodeObject;
```

### 七、结语
