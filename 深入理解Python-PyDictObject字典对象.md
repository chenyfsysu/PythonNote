关联容器是非常重要的数据结构，它记录着一对对符合该容器所代表的关联规则的元素对。所有的语言都提供了关联容器的数据结构，比如C++中的map对象，C#中的Dictionary, 而在Python中是dict。关联容器保留了元素对的映射关系，能让元素搜索更加快速。C++底层是用红黑树实现map，它能保证元素的搜索效率在logN级别。而在Python中， 关联容器dict更是占据极其重要的地位，Python内部实现中很多数据结构都使用了dict来存储，比如全局空间变量的存储globals、局部空间变量的存储locals等。正是因为如此广泛的应用，要求dict的搜索效率更高，在底层中dict的是以散列表（hash）实现，它能保证搜索效率在O(1)级别。
### 一、PyDictObject
关联对象在python中是dict对象，它对应的其实就是c层中的PyDict对象。PyDict对象的定义如下：
``` c
typedef struct _dictobject PyDictObject;
struct _dictobject {
    PyObject_HEAD
    Py_ssize_t ma_fill;  /* # Active + # Dummy */
    Py_ssize_t ma_used;  /* # Active */

    /* The table contains ma_mask + 1 slots, and that's a power of 2.
     * We store the mask instead of the size because the mask is more
     * frequently needed.
     */
    Py_ssize_t ma_mask;

    /* ma_table points to ma_smalltable for small tables, else to
     * additional malloc'ed memory.  ma_table is never NULL!  This rule
     * saves repeated runtime null-tests in the workhorse getitem and
     * setitem calls.
     */
    PyDictEntry *ma_table;
    PyDictEntry *(*ma_lookup)(PyDictObject *mp, PyObject *key, long hash);
    PyDictEntry ma_smalltable[PyDict_MINSIZE];
};
```
### 二、dict搜索与hash
``` c
static PyDictEntry *lookdict_string(PyDictObject *mp, PyObject *key, register long hash)
{
    register size_t i;
    register size_t perturb;
    register PyDictEntry *freeslot;
    register size_t mask = (size_t)mp->ma_mask;
    PyDictEntry *ep0 = mp->ma_table;
    register PyDictEntry *ep;

    if (!PyString_CheckExact(key)) {
        mp->ma_lookup = lookdict;
        return lookdict(mp, key, hash);
    }
    i = hash & mask;
    ep = &ep0[i];
    if (ep->me_key == NULL || ep->me_key == key)
        return ep;
    if (ep->me_key == dummy)
        freeslot = ep;
    else {
        if (ep->me_hash == hash && _PyString_Eq(ep->me_key, key))
            return ep;
        freeslot = NULL;
    }
}

static PyDictEntry *lookdict(PyDictObject *mp, PyObject *key, register long hash)
{
}
```
### 三、dict插入与删除
``` c
static int insertdict(register PyDictObject *mp, PyObject *key, long hash, PyObject *value)
{
    register PyDictEntry *ep;

    assert(mp->ma_lookup != NULL);
    ep = mp->ma_lookup(mp, key, hash);
    if (ep == NULL) {
        Py_DECREF(key);
        Py_DECREF(value);
        return -1;
    }
    return insertdict_by_entry(mp, key, hash, ep, value);
}

static int insertdict_by_entry(register PyDictObject *mp, PyObject *key, long hash,
                    PyDictEntry *ep, PyObject *value)
{
    PyObject *old_value;

    MAINTAIN_TRACKING(mp, key, value);
    if (ep->me_value != NULL) {
        old_value = ep->me_value;
        ep->me_value = value;
        Py_DECREF(old_value); /* which **CAN** re-enter */
        Py_DECREF(key);
    }
    else {
        if (ep->me_key == NULL)
            mp->ma_fill++;
        else {
            assert(ep->me_key == dummy);
            Py_DECREF(dummy);
        }
        ep->me_key = key;
        ep->me_hash = (Py_ssize_t)hash;
        ep->me_value = value;
        mp->ma_used++;
    }
    return 0;
}
```
### 四、PyDictObject对象缓存池
``` c
static void dict_dealloc(register PyDictObject *mp)
{
    register PyDictEntry *ep;
    Py_ssize_t fill = mp->ma_fill;
    PyObject_GC_UnTrack(mp);
    Py_TRASHCAN_SAFE_BEGIN(mp)
    for (ep = mp->ma_table; fill > 0; ep++) {
        if (ep->me_key) {
            --fill;
            Py_DECREF(ep->me_key);
            Py_XDECREF(ep->me_value);
        }
    }
    if (mp->ma_table != mp->ma_smalltable)
        PyMem_DEL(mp->ma_table);
    if (numfree < PyDict_MAXFREELIST && Py_TYPE(mp) == &PyDict_Type)
        free_list[numfree++] = mp;
    else
        Py_TYPE(mp)->tp_free((PyObject *)mp);
    Py_TRASHCAN_SAFE_END(mp)
}
```