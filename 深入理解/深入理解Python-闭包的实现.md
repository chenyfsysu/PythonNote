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
一堆func开头的的属性引起了我们的注意，**func_closure**更是格外显目。**closure**不正是闭包的意思吗，这里面的内容一定和闭包紧密相关。我们尝试打印打印**do_sth**的**func_closure**的内容，遗憾的是居然是**None**。再仔细想想，**do_sth**只是外层函数，而**lambda**才是闭包，所以闭包的内容会不会再lambda（闭包）函数中。打印闭包的**func_closure**内容（可以把闭包用变量保存，再使用dis函数），果然在这里发现了特别的内容:

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
我们关注到4个特殊的字节码：**STORE_DEREF**、**LOAD_CLOSURE**、**MAKE_CLOSURE**、**LOAD_DEREF**。接下来从Pyhton源码的层面查看这四个字节码的实现，必能解答闭包的问题。
###  四、源码实现
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
### 五、co_cellvars和co_freevars
``` cpp
typedef struct {
  ...
    PyObject *co_freevars;  /* tuple of strings (free variable names) */
    PyObject *co_cellvars;      /* tuple of strings (cell variable names) */
} PyCodeObject;
```
### 六、PyCellObject
``` cpp
typedef struct {
  PyObject_HEAD
  PyObject *ob_ref; /* Content of the cell or NULL when empty */
} PyCellObject;
```

``` cpp
PyObject *
PyCell_Get(PyObject *op)
{
    if (!PyCell_Check(op)) {
        PyErr_BadInternalCall();
        return NULL;
    }
    Py_XINCREF(((PyCellObject*)op)->ob_ref);
    return PyCell_GET(op);
}
```

``` cpp
int
PyCell_Set(PyObject *op, PyObject *obj)
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
### 七、总结
