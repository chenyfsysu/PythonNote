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

### 四、多重继承
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