### 一、类与继承
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
### 三、__mro__
``` python
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
```