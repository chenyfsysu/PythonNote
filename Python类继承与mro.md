### 一、类与继承
Python中一切皆对象，一切对象皆由类实例化。在面向对象语言中，类和对象是是最重要的两个概念。在Python中，可以通过class关键字定义一个类，通过实例化该类可以获取该类对应的对象。面向对象中类的继承也是一个重要的概念，通过继承子类可以拥有父类的所有功能。Python中也可以在定义时指定该类的继承对象，如下例子A继承于Python类型基类object， B继承于A。B中定义的方法会覆盖A的方法，也即在Pyhton中函数拥有多态的能力。
``` python
class A(object):
	def call(self):
		print 'call A'

class B(object):
	def call(self):
		print 'call B'

b = B()
b.call()  # call B
```

### 二、super
由上面的例子可知B同名函数call的函数会覆盖A的函数call。上面说子类拥有父类的所有功能，那如果通过B想要调用A的同名函数怎么办。Python提供了两种方法：第一种可以直接通过A.call()显式调用A的函数，第二种可以通过super，让Python自动解析B的父类函数。Python更建议使用super，super其实是一个类，它根据传入类型和self自动解析对应的父类。在下面这个例子中，通过A.call和super调用的效果是一样的，而在后面的多重继承中可以看到super的不同。super不是调用当前类的直接父类，而是解析出该类的最高子类的类体系下的下一调用类。
```
class A(object):
	def call(self):
		print 'call A'

class B(A):
	def call(self):
		super(B, self).call()
		print 'call B'

b = B()
b.call()  # call A call B
```
### 三、__mro__方法解析顺序
``` python
mro的全程是
print B.__mro__
# (<class '__main__.B'>, <class '__main__.A'>, <type 'object'>)
```
### 四、新式类与旧式类
``` python
import inspect

class A1(object): pass
class B1(A1): pass
class C1(A1): pass
class D1(B1, C1): pass

class A2: pass
class B2(A2): pass
class C2(A2): pass
class D2(B2, C2): pass

print D1.__mro__
print inspect.getmro(D2)

# (<class '__main__.D1'>, <class '__main__.B1'>, <class '__main__.C1'>, <class '__main__.A1'>, <type 'object'>)
# (<class __main__.D2 at 0x02518960>, <class __main__.B2 at 0x025185E0>, <class __main__.A2 at 0x024B4458>, <class __main__.C2 at 0x02518848>)
```
### 五、多重继承
```  python
class A(object):
	def call(self, p1):
		pass

class B(A):
	def call(self, p1, p2):
		super(B, self).call(p1)

class C(A):
	def call(self):
		pass


class D(B, C):
	def call(self, p1, p2):
		super(D, self).call(p1, p2)


d = D()
d.call(1, 2)
# TypeError: call() takes exactly 1 argument (2 given)

print  D.__mro__
# (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <type 'object'>)
```