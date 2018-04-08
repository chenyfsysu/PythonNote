# -*- coding:utf-8 -*-


def func(x, y, z):
    print x, y, z
    return (x + y)

def dump():
    return 1
data = {'z': 2}
x = (1,)
func(1, y=dump(), **data)
