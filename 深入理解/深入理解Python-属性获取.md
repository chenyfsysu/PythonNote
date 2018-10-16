### 一、属性访问
``` python
# main.py
class A(object):
    def __init__(self):
        self.name = "coco"

    def func(self):
        pass

a = A()

print A.func # <unbound method A.func of <__main__.A object>
print a.func # <bound method A.func of <__main__.A object>
print a.name # coco
print a.age  # raise Attribute
```
上面这段代码可能大家都理解，也能知道答案。用过Python的人都知道通过**(.)**可以访问一个对象的属性、对象能够访问其类型（Type）的属性、**__getattr__**能够自定义属性访问规则。但是可能没有思考过当你键入**(.)**的时候，Python解释器是怎么处理的？当你定义**__getattr__**时，是否会影响改变访问的规则，影响属性访问的性能。**源码之下，了无秘密**，这些问题必须要深入到Python解释器的层面才能得到解答（以下源码都是以CPython解释器为准）。
### 二、深入剖析
通过执行dis指令可以查看以上逻辑的字节码

``` python
python -m dis main.py
11          39 LOAD_NAME                2 (a)
            42 LOAD_ATTR                3 (func)
```
可以看到对对象进行属性访问的字节码是**LOAD_ATTR**，以此为切入点开始探索属性访问源码再合适不过。**eval.c**中可以看到字节码**LOAD_ATTR**的处理逻辑是：

``` cpp
 TARGET(LOAD_ATTR)
 {
     w = GETITEM(names, oparg);
     v = TOP();
     x = PyObject_GetAttr(v, w);
     Py_DECREF(v);
     SET_TOP(x);
     if (x != NULL) DISPATCH();
     break;
 }
```
可以看到，源码中对于属性访问的秘密正是从**PyObject_GetAttr**开始的。接下来再深入到**PyObject_GetAttr**中：

``` cpp
PyObject * PyObject_GetAttr(PyObject *v, PyObject *name)
{
 PyTypeObject *tp = Py_TYPE(v)
 if (tp->tp_getattro != NULL)
     return (*tp->tp_getattro)(v, name);
 if (tp->tp_getattr != NULL)
     return (*tp->tp_getattr)(v, PyString_AS_STRING(name));
}
```
**PyObject_GetAttr**非常简短，显然真正的访问逻辑并不是在这里。但是从这里我们已经能窥得两个重要的信息1）属性访问是通过其类型（PyTypeObject）完成的 2）真正的执行逻辑在tp_getattro和tp_getattr身上。

### 二、tp_getattro 指针
在PyTypeObject的定义中：

```cpp
typedef struct _typeobjet {
    getattrfunc tp_getattr;
    setattrfunc tp_setattr;
    
    getattrfunc tp_getattro;
    setattrfunc tp_setattr;
} PyTypeObject;
```
可以看到**tp_getattr**和**tp_getattro**都是函数指针，根据Python的官方文档介绍tp_getattr已经废弃，所以我们只需要关注**tp_getattro**。看到函数指针，一下子柳暗花明，这是要对类型的不同状态执行不同的搜索策略！不同的状态洗，只需要将**tp_getattro**指针指向对应的函数。根据Python文档介绍，tp_getattro可能指向三个搜索函数：**slot_tp_getattro**、**slot_tp_getattro_hook**和**PyObject_GenericGetAttr**。那么什么时候指向**slot_tp_getattro**、什么时候指向**slot_tp_getattt_hook**、什么时候指向**PyObject_GenericGetAttr**呢。这点在源码的注释里也介绍的很清楚：

``` cpp
/* There are two slot dispatch functions for tp_getattro.

   - slot_tp_getattro() is used when __getattribute__ is overridden
     but no __getattr__ hook is present;

   - slot_tp_getattr_hook() is used when a __getattr__ hook is present.

   The code in update_one_slot() always installs slot_tp_getattr_hook(); this
   detects the absence of __getattr__ and then installs the simpler slot if
   necessary. */
```
总结起来就是：
>__* PyObject_GenericGetAttr：默认的搜索函数
> * slot_tp_getattro：当类定义了**__getattribute__**函数且没有定义**__getattr__**函数
> * slot_tp_getattr_hook：当类定义了**__getattr__**


### 三、普通属性访问(PyObject_GenericGetAttr)
上面已经知道了**PyObject_GenericGetAttr**是通用的搜索函数，这意味着绝大部分情况下，属性访问规则都是在该函数内。在深入**PyObject_GenericGetAttr**源码之前，先理解一下几个概念：
##### 1） Data Descriptor 和Non-Data Descriptor
首先要理解的就是Python Descriptor（描述器）。可能大部分人都用过@property来hook某个属性的访问，它实际上就是一个Descriptor。
``` python
class A(object):
    @property
    def name(self):
        return "coco"
```
描述起其通用形式是这样：
``` python
class Descriptor(object):
    def __init__(self, val):
        self.val = val

    def __get__(self, obj, objtype):
        return self.val

    def __set__(self, obj, val):
        self.val = val
```

``` python
class A(obejct):
    name = Descriptor("")
```
A的name就是一个Descriptor，如果定义了**__set__**函数，那么它是一个**Data Descriptor**，否则它是一个**Non-Data Descriptor**。
##### 2）MRO（Method Resolution Order)
**MRO**的全称是方法解析顺序，它定义了Python继承链的一个顺序列表。简单来说，**MRO**定义了在类型的属性查找顺序（查找一个类的属性就是在**MRO**中顺序查找）。对于新式类，Python中是使用C3算法来生成**MRO**，具体可查阅资料，这里不详细展开。

介绍完了**Descriptor**和**MRO**两个概念，接下来将正式深入**PyObject_GenericGetAttr**的源码。**PyObject_GenericGetAttr**的代码是在**object.c**中，它实际上只是一个代理函数，真正的实现是在**_PyObject_GenericGetAttrWithDict**中：

``` cpp
``` python
PyObject *_PyObject_GenericGetAttrWithDict(PyObject *obj, PyObject *name, PyObject *dict)
{
     descr = _PyType_Lookup(tp, name);
     // 1.是否是Data Descriptor
    if (descr != NULL &&
        PyType_HasFeature(descr->ob_type, Py_TPFLAGS_HAVE_CLASS)) {
        f = descr->ob_type->tp_descr_get;
        if (f != NULL && PyDescr_IsData(descr)) {
            res = f(descr, obj, (PyObject *)obj->ob_type);
            Py_DECREF(descr);
            goto done;
        }
    }
    // 2.从object的__dict__下获取
    if (dict != NULL) {
        res = PyDict_GetItem(dict, name);
    }
    
    // 3. 是否是Non-Data Descriptor
    if (f != NULL) {
        res = f(descr, obj, (PyObject *)Py_TYPE(obj));
        Py_DECREF(descr);
        goto done;
    }
    
    // 4.从type中获取的普通属性
    if (descr != NULL) {
        res = descr;
        /* descr was already increfed above */
        goto done;
    }
    
    // 5. raise AttributeError
    PyErr_Format(PyExc_AttributeError,
             "'%.50s' object has no attribute '%.400s'",
             tp->tp_name, PyString_AS_STRING(name));

}
```
从源码中可以看到，正常的属性访问总结起来有五个步骤：
> * 从type中获取该属性值（这里即是从对象的类型的MRO中查找，若获取回来的属性值是Data Descriptor，则调用Descriptor的get方法返回。
> * 从object的__dict__中获取属性值，若存在，则返回。
> * 若type中获取的属性值是Non-Data Descriptor，则调用Descriptor的get方法返回
> * 如果从type中获取的属性值不是Descriptor且不为空，返回该属性值
> * 访问失败，raise AttributeError

### 四、slot_tp_getattro与slot_tp_getattr_hook
以上已经介绍了**PyObject_GenericGetAttr**的属性访问流程。而对于定义了**__getattribute__**的类型，会重定向到**slot_tp_getattro**进行属性访问。对于定义了**__getattr__**的类型，会重定向到**slot_tp_getattr_hook**进行属性访问。
**slot_tp_getattro**的实现很简单，就只是简单的调用脚本中定义的**__getattribute__**方法。

``` cpp
static PyObject *slot_tp_getattro(PyObject *self, PyObject *name)
{
    static PyObject *getattribute_str = NULL;
    return call_method(self, "__getattribute__", &getattribute_str,
                       "(O)", name);
}
```
而对于**slot_tp_getattr_hook**, 则要先通**__getattribute__**检查是否有该属性，如果有则返回，没有则调用脚本定义的**__getattr__**方法检索属性。

``` cpp
static PyObject * slot_tp_getattr_hook(PyObject *self, PyObject *name)
{
    getattr = _PyType_Lookup(tp, getattr_str);
    getattribute = _PyType_Lookup(tp, getattribute_str);
    
    getattribute = _PyType_Lookup(tp, getattribute_str);
    if (getattribute == NULL ||
        (Py_TYPE(getattribute) == &PyWrapperDescr_Type &&
         ((PyWrapperDescrObject *)getattribute)->d_wrapped ==
         (void *)PyObject_GenericGetAttr))
        res = PyObject_GenericGetAttr(self, name);
    else {
        Py_INCREF(getattribute);
        res = call_attribute(self, getattribute, name);
        Py_DECREF(getattribute);
    }
    if (res == NULL && PyErr_ExceptionMatches(PyExc_AttributeError)) {
        PyErr_Clear();
        res = call_attribute(self, getattr, name);
    }
    Py_DECREF(getattr);
    return res;
}
```

### 五、getattro的装载
上面已经介绍了**PyObject_GenericGetAttr**、**slot_tp_getattro**、**slot_tp_getattr_hook**三个函数，但是有一个很重要的问题没提及：Python解释器是什么时候装载这三个函数的。Python解释器中有一个很重要的概念：slot（槽）机制。槽机制使Python非常灵活，比如通过**__getattr__** hook属性访问，通过**__setattr__** hook属性存储，通过**__add__** hook加法运算，这些功能都是通过槽机制来实现的（就是替换函数指针）。Python槽的定义如下：

``` python
static slotdef slotdefs[] = {
    TPSLOT("__getattribute__", tp_getattro, slot_tp_getattr_hook,
           wrap_binaryfunc, "x.__getattribute__('name') <==> x.name"),
    TPSLOT("__getattr__", tp_getattro, slot_tp_getattr_hook, NULL, ""),
    BINSLOT("__add__", nb_add, slot_nb_add, "+"),
    ...
};
```
可以看到，在槽中定义了定义了对应的属性名，解释器的函数指针以及处理函数。这样能很容易地根据属性状态重定向函数指针。函数指针的装载要处理两种情况，第一种情况是初始化，第二种情况是更新（比如动态设置了**__getattr__**属性）。
##### 类型创建时
创建新类型时，在**tp_new**中会调用**fixup_slot_dispatcher**对所有槽进行初始化。

``` cpp
static void
fixup_slot_dispatchers(PyTypeObject *type)
{
    slotdef *p;

    init_slotdefs();
    for (p = slotdefs; p->name; )
        p = update_one_slot(type, p);
}
```
##### 动态为类型设置属性
在更新类型属性时，会检查是否需要更新槽。如果需要会调用**update_slot**以更新该槽的指向内容。

``` cpp
res = PyObject_GenericSetAttr((PyObject *)type, name, value);
if (res == 0) {
    res = update_slot(type, name);
}
```
### 六、回到性能问题
至此，已经介绍了关于Python属性访问的大部分问题。再回到最初的疑问，当定义了**__getattr__**，是够会影响该类型的属性访问性能？显然，因为定义了__getattr__后，**slot_tp_getattr_hook**将会装载到**tp_getattro**槽中，而**slot_tp_geattr_hook**中执行了获取该类型的**__getattr__**和**__getattribute__**属性，再调用到**PyObject_GenericGetAttr**函数，访问性能势必会下降。经个人简单测试，定义了**__getattr__**后，整个类型的访问性能要下降15%左右。这意味着，在性能热点的类型中，还是尽量避免使用**__getattr__**来hook属性访问，因为它会改变该类型的访问策略，影响整个类型的属性访问性能。