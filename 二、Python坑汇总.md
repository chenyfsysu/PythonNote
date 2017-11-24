#### 一、lambda late binding
说起python坑，应该大家都会想到这个，lambda的变量是在内部函数被调用的时候被查找，这时候for循环已经执行完了
```python
lst = [lambda i: i for i in range(5)]
for callback in lst:
	print callback()
# 4, 4, 4, 4, 4
```
正确的写法
```python
lst = (lambda i: i for i in range(5))
lst = [lambda i=i: i for i in range(5)]
```

#### 二、可变对象作为函数默认值会保存
```python
def func(a , lst=[]):
	lst.append(a)
	print lst

func(1)  # [1]
func(2)  # [1, 2]
```


#### 三、迭代器迭代后不重置
``` python
gen = (i for i in range(5))
2 in gen  # True
3 in gen  # True
1 in gen  # False 执行2 in gen, 3 in gend的时候已经迭代到了3
```

#### 四、继承重写基类值
``` python
class Base(object):
	val = 1

class Inherit1(Base):
	pass

class Inherit2(Base):
	pass

def printVal():
	print Base.val, Inherit1.val, Inherit2.val

printVal()  # 1 1 1
Inherit1.val = 2
printVal()  # 1 2 1
Base.val = 3
printVal()  # 3 2 3
```
Base修改val值为3后Inherit1的值没有修改，但是Inherit2的值却修改了，这是因为python类的属性都保留在dict中，访问属性时如果自身没有就访问父类属性，而Inherit1的val赋值后已经在自身属性添加了val。