大概很多人都知道Python是由c实现的，Python程序本质上就是一个C程序，然而我们少有深入了解它的底层是如何实现的，它的运行机制是如何的。本文希望从C层面以宏观的形式了解python的运行原理。

### 一、Py_Main程序主入口
Py_Main是一个Python程序的c入口(忽略main函数), 我们执行python文件是通过python的解释器执行：python main.py，当然也可以通过控制台交互的方式执行python，还可以从python程序中获取帮助：python --help。Py_Main函数主要就是对这些功能进行分发， 我们这里主要是考虑运行python脚本的功能。对于执行python脚本的功能，PyMain主要进行两项工作：
> * 1）Py_Initizlize初始化python的执行环境：初始化sys、builtin模块等
> * 2）PyRun_AnyFileExFlags根据输入执行脚本文件或者进入交互模式执行脚本

``` c
int Py_Main(int argc, char **argv)
{
	// 其他功能的分发
	Py_Initialize();

    if (sts==-1 && filename!=NULL) {
    if ((fp = fopen(filename, "r")) == NULL) {
        fprintf(stderr, "%s: can't open file '%s': [Errno %d] %s\n",
            argv[0], filename, errno, strerror(errno));

        return 2;
    }
    else if (skipfirstline) {
        int ch;
        /* Push back first newline so line numbers
           remain the same */
        while ((ch = getc(fp)) != EOF) {
            if (ch == '\n') {
                (void)ungetc(ch, fp);
                break;
            }
        }
    }
    {
        /* XXX: does this work on Win/Win64? (see posix_fstat) */
        struct stat sb;
        if (fstat(fileno(fp), &sb) == 0 &&
            S_ISDIR(sb.st_mode)) {
            fprintf(stderr, "%s: '%s' is a directory, cannot continue\n", argv[0], filename);
            fclose(fp);
            return 1;
        }
    }
}

if (sts==-1) {
    /* call pending calls like signal handlers (SIGINT) */
    if (Py_MakePendingCalls() == -1) {
        PyErr_Print();
        sts = 1;
    } else {
        sts = PyRun_AnyFileExFlags(
            fp,
            filename == NULL ? "<stdin>" : filename,
            filename != NULL, &cf) != 0;
    }
}
}
```

### 二、Py_Initialize/Py_InitizlizeEx初始化运行环境
Py_Initialize初始化运行环境的工作实际是通过Py_InitizlizeEx执行：
``` c
void Py_Initialize(void)
{
    Py_InitializeEx(1);
}
```
Py_InitializeEx中主要为初始化python运行环境执行了以下工作：
> * 1）PyInterpreterState_New 创建一个全局的解释器
> * 2）PyThreadState_New 创建了并初始化了一个(主）线程执行环境
> * 3）_Py_ReadyTypes、_PyInt_Init等初始化python基本类型，缓存小整数等
> * 4）_PyBuiltin_Init 初始化builtin模块
> * 5）_PySys_Init 初始化sys模块
> * 6） initmain 创建__main__模块
``` c
void Py_InitializeEx(int install_sigs)
{
    interp = PyInterpreterState_New();
    if (interp == NULL)
        Py_FatalError("Py_Initialize: can't make first interpreter");
        
    tstate = PyThreadState_New(interp);
    if (tstate == NULL)
        Py_FatalError("Py_Initialize: can't make first thread");

    _Py_ReadyTypes();
    if (!_PyInt_Init())
        Py_FatalError("Py_Initialize: can't init ints");
        
    bimod = _PyBuiltin_Init();
    if (bimod == NULL)
        Py_FatalError("Py_Initialize: can't initialize __builtin__");

    sysmod = _PySys_Init();
    if (sysmod == NULL)
        Py_FatalError("Py_Initialize: can't initialize sys");
        
    initmain(); /* Module __main__ */
}
```
### 三、PyRun_AnyFileExFlags执行交互环境/运行代码文件
PyMain先执行Py_Initialize初始化执行环境后会执行PyRun_AnyFileExFlags。PyRun_AnyFileExFlags根据文件输入决定是进入交互环境(PyRun_InteractiveLoopFlags)还是执行脚本文件(PyRun_SimpleFileExFlags)：
``` c
int PyRun_AnyFileExFlags(FILE *fp, const char *filename, int closeit, PyCompilerFlags *flags)
{
    if (filename == NULL)
        filename = "???";
    if (Py_FdIsInteractive(fp, filename)) {
        int err = PyRun_InteractiveLoopFlags(fp, filename, flags);
        if (closeit)
            fclose(fp);
        return err;
    }
    else
        return PyRun_SimpleFileExFlags(fp, filename, closeit, flags);
}
```
### 四、PyRun_StringFlags
不管是PyRun_InteractiveLoopFlags还是PyRun_SimpleFileExFlags，本质上都是从不同的输入流获取脚本内容。获取脚本内容后会通过PyRun_StringFlags解析内容并执行脚本内容。PyParser_ASTFromString对输入的源码进行语法分析并返回一个语法分析树。run_mod跟居语法分析树生成字节码并通过激活虚拟机执行字节码。
``` c
PyObject * PyRun_StringFlags(const char *str, int start, PyObject *globals,
                  PyObject *locals, PyCompilerFlags *flags)
{
    PyObject *ret = NULL;
    mod_ty mod;
    PyArena *arena = PyArena_New();
    if (arena == NULL)
        return NULL;

    mod = PyParser_ASTFromString(str, "<string>", start, flags, arena);
    if (mod != NULL)
        ret = run_mod(mod, "<string>", globals, locals, flags, arena);
    PyArena_Free(arena);
    return ret;
}
```
### 四、run_mod执行Python代码
通过以上已经准备好了代码执行的大部分环境到了run_mod这一步。run_mod的两项重要任务是生成字节码、执行字节码。
```
static PyObject *run_mod(mod_ty mod, const char *filename, PyObject *globals, PyObject *locals,
         PyCompilerFlags *flags, PyArena *arena)
{
    PyCodeObject *co;
    PyObject *v;
    co = PyAST_Compile(mod, filename, flags, arena);
    if (co == NULL)
        return NULL;
    v = PyEval_EvalCode(co, globals, locals);
    Py_DECREF(co);
    return v;
}
```
#### 1）PyAST_Compile 生成字节码
PyAST_Compile根据语法分析树编译成字节码，返回的是PyCodeObject。
``` c
PyCodeObject *PyAST_Compile(mod_ty mod, const char *filename, PyCompilerFlags *flags,
              PyArena *arena)
{
    struct compiler c;
    PyCodeObject *co = NULL;
    ...
    co = compiler_mod(&c, mod);
    return co;
}
```
#### 2）PyEval_EvalCode 虚拟机执行字节码
PyEval_EvalCode根据PyCodeObject执行字节码内容(实际通过PyEval_EvalCodeEx执行）。PyEval_EvalCodeEx是通过虚拟机直接字节码比较复杂，后面理解虚拟机执行原理会深入理解。
