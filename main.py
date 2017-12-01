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
