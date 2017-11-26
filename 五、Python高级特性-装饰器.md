### 一、什么是装饰器
装饰器是一个著名的设计模式，它的思想是从函数/类的逻辑中抽象出与具体逻辑无关装饰性内容成为一个通用结构， 并且可以复用这个通用结构。比如一个网页业务用户会获取图片、发表文章等，而用户在进行这些操作前都需要验证用户的合法性（验证账号和密码），验证用户合法性的逻辑我们就可以认为是装饰性行为，也就可以把这部分行为构建为一个装饰器。后面如果有其他逻辑比如用户发表评论的业务需要验证合法性，就可以复用这个装饰器进行装饰，无需重复实现该逻辑。再比如实现了某个函数需要限制调用时间限制， 比如五秒钟只能调用一次，那么这个限制调用可以认为是一个装饰行为。由上面的装饰器的介绍可知，使用装饰器具有以下两个优点：
> * 1）抽象出装饰性行为，让代码逻辑更清晰，更易于维护
> * 2）复用装饰性行为，减少重复性代码的编写



### 二、Python装饰器
Python中使用装饰器，先定义装饰器wrapper的行为，然后在待装饰函数的定义上以@wapper装饰即可完成。以上面限制函数调用周期的例子为例，我们要限制一个函数最多5秒中调用一次可以这样实现：
1）定义装饰器limit_call
``` python
def limit_call(func):
	def wrapper(*args):
		if not hasattr(func, 'call_time'):
			func.call_time = 0

		if time.time() - func.call_time < 5.0:
			print 'call func limit 5.0 seconds'
			return

		func.call_time = time.time()
		return func(*args)

	return wrapper
```
2)使用装饰器limit_call装饰func
``` python
@limit_call
def func():
	print 'call func'
```
连续两次调用func， 第一次调用会成功，第二次调用会被阻断（5秒后才能再次调用）
``` python
func()  # call func
func()  # func func limit 5.0 seconds
```


### 三、带参数的装饰器
上面实现了一个限制5秒调用一次函数的装饰器，假设有一些函数需要限定10秒调用一次，有些需要20秒调用一次，那么我们为这些限制都实现一个装饰器吗。这显然是不合理的，Python中可以实现参数的装饰器，装饰器的功能可以根据参数内容动态执行。比如，以下实现一个可以动态控制限制时间的limit_call
``` python
import time

def limit_call(limit_time):
	def wrapper(func):
		def _wrapper(*args):
			if not hasattr(func, 'call_time'):
				func.call_time = 0

			if time.time() - func.call_time < limit_time:
				print 'call func limit %.1f seconds' % limit_time
				return

			func.call_time = time.time()
			return func(*args)
		return _wrapper
	return wrapper

@limit_call(10.0)
def func():
	print 'call func'

func()  # call func
func()  # func func limit 10.0 seconds
```

### 三、多个装饰器
对于一个函数，可以使用多个装饰器装饰，先装饰的装饰器后执行(越靠近函数定义)。比如执行一个函数，我们既希望限定它的调用周期，又希望在它调用的时候打印执行时间。那么可以实现一个统计调用时间的装饰器time_calc，使用time_calc和limit_call同时装饰函数，这里注意time_calc一定要在内层，这样才能保证统计的是func的运行时间。
``` python
def time_calc(func):
	def wrapper(*args):
		timestamp = time.time()
		rsl = func(*args)
		print 'func run time calc %f' % (time.time() - timestamp)
		return rsl
	return wrapper

@limit_call(10.0)
@time_calc
def func():
	print 'call func'
```
这样执行的时候就会先检查函数调用周期（limit_call)，再统计函数运行时间(time_calc)



### 四、类装饰器
以上主要介绍了函数的装饰器，实际上类也可以添加装饰器以修饰类的行为。比如我们想统计一个类的创建次数，可以一个创建一个calc_create的装饰器：
``` python
def calc_create(cls):
	def wrapper(*args):
		if not hasattr(cls, 'create_cnt'):
			cls.create_cnt = 0
		cls.create_cnt += 1
		print 'cls: %s, create_time: %d' % (cls.__name__, cls.create_cnt)
		return cls(*args)

	return wrapper



@calc_create
class Object(object):
	pass

a = Object()  # cls: Object, create_time: 1
b = Object()  # cls: Object, create_time: 2
```