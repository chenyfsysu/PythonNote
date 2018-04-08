Ast Optimizer的设计与实现
========
#### 一、目的
Ast Optimizer设计的目的是对Python源代码进行静态优化，实现上是通过在代码打包过程中扫描源代码、构建源代码ast进行访问及优化、最后重新输出源代码。确切地说， Ast Optimizer是建立在一定约束条件下对源码进行优化。Python是高度自由的解释型语言，没有任何限制的静态代码优化几乎是无法实现的。既然是要做约束，那么这些约束从经验上来说一定要是合理的，是一些以前可能是默认的规则，现在是强制的约束。比如我们每个项目都会有一个const文件来定义一些常量，这些常量一般来说是不会改变的。基于这个约束，我们就可以在离线对这些常量inline，提升性能。

#### 二、设计与实现
##### 1、Optimizer
Optimizer的优化过程可分为三个阶段：Tokenizer、 Visitor、Transformer，它们负责的任务如下：
- **Tokenizer** ：对源代码的token进行扫描分析(主要是注释， 有些优化功能会通过注释打标签)， 分析结果供后续Transformer使用
- **Visitor** ：对源代码的ast进行预访问，分析结果供后续Transformer使用（如通过import确定文件优化顺序）
- **Transformer** ：Transformer是真正对源代码进行优化的步骤，通过定义ast的访问方法，修改对应的ast node， optimizer会自动将修改后的ast重新输出为源码

Optimizer设计之初就是期望做成容易拓展的、可动态增减优化内容的优化器。通过装饰器OptimizeStep可以为Optimizer增加Optimize step进行对应优化内容：
```python
from steps.constant_optimizer import ConstantOptimizeStep
from steps.inline_optimizer import InlineOptimizeStep
from steps.component_optimizer import ComponentOptimizeStep

@OptimizeStep(ConstantOptimizeStep, InlineOptimizeStep, ComponentOptimizeStep)
class Optimizer(object):
	pass
```
##### 2、Optimize step
Optimize Step主要由三部分Tokenizer， Visitor、Transformer三部分组成，其中Tokenizer和Visitor是可选的。
``` python
class ConstantTokenizer(StepTokenizer):
	def visit_Comment(self, token, srow_scol, erow_ecol, line, context):
		pass
		
class ConstantVisitor(StepVisitor):
	pass

class ConstantTransformer(StepTransformer):
	def onEnter(self):
		pass

	def visit_ClassDef(self, node, context):
		return node

ConstantOptimizeStep = OptimizerStep(tokenizer=ConstantTokenizer, visitor=ConstantVisitor, transformer=ConstantTransformer)
```

#### 三、ast分析
为了方便进行ast分析，框架内部提供了一些通用功能，如通过动态拓展原生ast node提供一些必要的功能(如ClassDef提供计算mro等)、ModuleLoader提供import功能、在Builder阶段确定所有变量的作用域等。
##### 1、动态拓展ast node
``` python
def dynamic_extend(cls):
	def _dynamic_extend(klass):
		for name, func in inspect.getmembers(klass, inspect.ismethod):
			setattr(cls, name, func.im_func)
		cls.__excls__ = klass

	return _dynamic_extend

@dynamic_extend(_ast.ClassDef)
class ClassDef(ScopeNode):
	def nMro(self):
		pass
	def nBases(self):
		pass
```
##### 2、跨文件import
为了方便多文件分析，通过ModuleLoader可以在AstNode层进行import操作得到对应的astNode，ModuleLoader实现上跟Python源码一致。
``` python
class ModuleLoader(Singleton):
	def load(self, name, fromlist=None, level=-1, caller=None):
		pass
```
##### 3、变量作用域确定
在构建ast树后，会首先进行一次访问，这次访问的目的类似于python的compile过程，会首先确定所有变量的作用域是Local、Global还是Cell、Free等。
``` python
NT_LOCAL = 1
NT_GLOBAL_IMPLICIT = 2
NT_GLOBAL_EXPLICIT = 3
NT_FREE = 4
NT_CELL = 5
NT_UNKNOWN = 6

class Scope(object):
	def __init__(self, type, name, lookup, locals):
		self.type = type
		self.name = name
		self.lookup = lookup
		self.locals = locals

	def identify(self, name):
		return self.lookup.get(name, NT_UNKNOWN)
```

#### 五、后续迭代
目前Optimizer还处于正在开发阶段，上述的大部分功能都已经实现。当前仍在继续开发更多的功能，后续计划添加的功能有1）eval系统实现对一些简单函数的运行 2）增加文件关联、批量进行扫描等。