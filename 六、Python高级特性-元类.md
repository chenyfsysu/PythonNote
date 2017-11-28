### 一、使用while 1而不是while True
``` python
import timeit
 
def while_one():
    i = 0
    while 1:
        i += 1
        if i == 100000000:
            break
 
def while_true():
    i = 0
    while True:
        i += 1
        if i == 100000000:
            break
 
w1 = timeit.timeit(while_one, "from __main__ import while_one", number=3)
wt = timeit.timeit(while_true, "from __main__ import while_true", number=3)
print "while one: %s\nwhile_true: %s" % (w1, wt)
# while one: 10.3411697307
# while_true: 15.240744352
```
while 1比while True要快近三分之一（python 2），这是因为True和False不是关键字，每次执行都要对它们的值进行检查，而1在字节码中是个常量因此运行更快些。在Pyhton3中True和False已经成为关键字，运行速度可能差不多。

### 二、if x比if x ==更快
``` python
import timeit
 
def if_x_eq_true():
    x = True
    if x == True:
        pass
 
def if_x():
    x = True
    if x:
        pass
 
time1 = timeit.timeit(if_x_eq_true, "from __main__ import if_x_eq_true", number=10000000)
time2 = timeit.timeit(if_x, "from __main__ import if_x", number=10000000) 
print 'if_x_eq_true', time1
print 'if_x', time2

# if_x_eq_true 1.44378467262
# if_x 1.06990989512
```
if_x_eq_true比if_x更快，因为if_x_eq_true需要检查true值（其他值同理)
