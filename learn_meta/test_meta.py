from curses.ascii import SP
import six
from abc import ABCMeta, abstractmethod

class SpecialMeta(type):
    def __new__(cls,name,bases,d):
        #重载__new__函数加入一些诡异的操作
        print(cls)      #<class '__main__.SpecialMeta'>
        print(name)     #MySubclass
        print(bases)    #(<class '__main__.MyClass'>,)
        print(d.items())    #{'__module__': '__main__', '__qualname__': 'MySubclass', '__init__': <function MySubclass.__init__ at 0x7f11401be680>, '__classcell__': <cell at 0x7f11403b3250: empty>}
        
        
        return super(SpecialMeta, cls).__new__(cls,name,bases,d)

class MyClass(object):
    def __init__(self,argA,argB):
        self.a = argA
        self.b = argB

class MySubclass(six.with_metaclass(SpecialMeta,MyClass)):
    def __init__(self,argA,argB,argC):
        super(MySubclass, self).__init__(argA=argA,argB=argB)
        self.c=argC


obj = MySubclass(1,2,3)
print(obj.c)
print(obj.a)