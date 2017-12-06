### 一、类的类
Pythoner一定听过都听过这句话：Python一切皆对象。在Python中，对象(object/instance)是由类生成，我们可以通过对象的__class__获取对象对应的类是哪个。
``` python
class Object(object):
	pass

obj = Object()
print  obj.__class__  # <class '__main__.Object'>
```
可以看到obj.__class__属性正是它对应的类：Object。Python中一切皆对象，
类本身也是一种对象（一切皆对象），那类的类是谁，答案就是：元类。Pyhton中一切皆对象，一切对象皆由类实例化。那问题来了，类是由谁实例化， 类的类是谁。我们可以通过打印Object的__class__属性看看这个类的类是谁。
``` python
print Object__class__  # <type 'type'>
```
打印出来发现Object的类是type这东西，那么type是什么呢?
### 二、元类
事实上，type正是我们这篇要介绍的：元类。元类、类、对象的关系：元类的实例是类，类的实例是对象(元类的类是它自己）：
![metaclass](https://github.com/chenyfsysu/PythonNote/blob/master/src/metaclass.png)
我们可以通过元类type实例化一个类，我们可以通过type实例化一个Math类，并为这个类绑定一个add方法。
``` python
def add(self, a, b):
	return a + b

Math = type('Math', (object, ), dict(add=add))
print Math  # <class '__main__.Math'>

math = Math()
print math  # <__main__.Math object at 0x0255A650>

rsl = math.add(1, 2)
print rsl  # 3
```
可以看到通过type('Math', (object, ), dict(add=add))， 确实动态实例化一个Math类，通过这个类也可以正常实例化math方法。
### 三、利用元类实现ORM
以上介绍可以看到通过类是由元类实例化，类的类是元类。从元类的特性看，我们可以知道元类可以动态地改变类的行为，这个动态特性让操作类更加方便。用过django的同学一定都会觉得框架里面的Model非常模型，通过定义Model的数据库字段就能自动读写数据库。
``` python
from django.db import models
class Person(models.Model):
	name = models.CharField(max_length=30)
	city = models.CharField(max_length=60)

person = Person():
person.save()  # 通过save可以自动存储
```
可以看到Model确实能够方便，它能够自动识别定义的数据库字段，将对象的成员和数据库字段一一对应。那django内部是怎么完成这点的呢？每次存储遍历Person的所有字段，如果是Field的子类就存储？这显然是效率低下的。事实上，django实现Model的ORM框架正式通过元类实现的。Model的元类ModelBase(可以通过__metaclass__指定元类), 在创建Model类的时候，就检查其所有的Field属性并将其存储起来。下面我们实现一个类似django Model的ORM框架。
``` python
class BaseField(object):
	def serialize(self):
		raise NotImplementedError

class IntField(BaseField):
	def __init__(self, val=0):
		self.val = val

	def serialize(self):
		return self.val

class StringField(BaseField):
	def __init__(self, val=''):
		self.val = val

	def serialize(self):
		return self.val


class ModelBase(type):
	"""MetaClass"""
	def __new__(cls, name, bases, attrs):
		mapping = {}
		for attr, val in attrs.iteritems():
			if isinstance(val, BaseField):
				mapping[attr] = val.__class__
		for attr in mapping:
			attrs.pop(attr)

		attrs['mapping'] = mapping
		return type.__new__(cls, name, bases, attrs)


class Model(object):
	__metaclass__ = ModelBase

	def save(self):
		print '--------------------save------------------'
		for attr, field in self.mapping.iteritems():
			print 'save %s, val: %s' % (attr, field(getattr(self, attr)).serialize())

class Person(Model):
	name = StringField()
	age = IntField()

person = Person()
person.name = 'coco'
person.age = 18
person.save()

# --------------------save------------------
# save age, val: 18
# save name, val: coco
```
类创建时会调用元类的def __new__(cls, name, bases, attrs)方法，其中attrs存储了该类的所有属性，通过该方法可以动态改变类的内容。通过ModelBase在Model类创建时就创建成员与数据库字段对应的mapping属性，save的时候就可以根据mapping进行操作。