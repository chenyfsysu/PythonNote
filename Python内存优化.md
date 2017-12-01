### 一、使用__slot__
```
import sys

class Object(object):
	def __init__(self):
		pass


class SlotObject(object):
	__slots__ = ()
	pass

a, b = Object(), SlotObject()
print sys.getsizeof(a)  # 32
print sys.getsizeof(b)  # 8
```
### 二、使用弱引用减少循环引用
