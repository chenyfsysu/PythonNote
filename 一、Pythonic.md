Pythonic的意思是在编写Python代码更符合Python风格。作为程序员，我们一般先接触C、C++等语言再接触Python，在编写Python代码时容易受到这些语言的编程思维影响，代码显得Non-Pythonic。以下总结Python编程中一些典型的Pythonic代码风格。


### 遍历list
```python
lst = [1, 2, 3, 4, 5]
for l in lst:
    pass
```

### 遍历list特定步长
``` python
a = [1, 2, 3, 4, 5]
for i in a[::2]:
	print i
# 1 3 5 list[start:end:step]
```

### 预设字典默认值
``` python
groups = {}
for (key, value) in data:
    groups.setdefault(key, []).append(value)
```

### 列表解析
``` python
lst = [1, 2, 3, 4, 5]
lst1 = [x for x in lst if x > 3]
# lst1 = [4, 5]
```

### 字符串拼接
``` python
lst = ['My', 'Name', 'is', 'coco']
str = ' '.join(lst)
```

### dict合并
``` python
a = {'name': 'coco', 'score': 20}
b = {'age': 18, 'id': 2933}
a.update(b)
# a = {'age': 18, 'score': 20, 'name': 'coco', 'id': 2933}
```

### unpack
```python
data = ('coco', '90, True)
name, score, _ = data
```

### enmurate
```python
lst = ['coco', 'jang']
for index, name in enmurate(lst):
    print index, name
# 0 coco
# 1 jang
```

### for...else...
```python
lst = [1, 3, 4, 7]
for val in lst:
    if val > 10:
        print 'find number greater than 10'
        break
else:
    print 'no number greater than 10
```

### filter
```python
lst = [1, 2, 3, 4, 5]
lst = filter(lambda x: x > 2, lst)
# 3 4 5
```

### zip
```python
names = ['coco', 'jang', 'peter']
scores = [90, 30, 40, 50]
for name, score in zip(names, scores):
    print name, score
# coco 90
# jang 30
# peter 40
```

### map
```python
lst = [1, 2, 3]
lst = map(lambda x: x * 100, lst)
# lst = [100, 200, 300]
```

### reduce
```python
lst = [1, 2, 3]
sum = recude(lambda x, y: x + y, lst)
# sum = 6
```

### bisect排序模块(找出列表中的插入位置)
```python
import bisect

a = [2, 3, 6, 7, 9]
idnex = bisect.bisect(a, 5)
# index = 2
```