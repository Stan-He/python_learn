class A(object):
    pass
class B(A):
    pass
class C(B):
    pass
class D(A):
    pass
class E(D):
    pass
class F(C,E):
    pass


f=F()
print f.__MRO__
