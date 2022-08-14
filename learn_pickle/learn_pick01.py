import pickle

class A(object):
    def __init__(self):
        self.a= "abc"


class D(object):
    def __init__(self):
        self.d= "abc"
        self.a= A()

#pickle dumps/loads 方法，将对象转换为bytes
d1 = {"k1":"v1","k2":"v2"}
s = pickle.dumps(d1)
print(s)
d2 = pickle.loads(s)
print(d2)

d1=D()
s = pickle.dumps(d1)
print(s)
d2 = pickle.loads(s)
print(d2.a.a)

#pickle dump/load 方法，将对象存储到文件
d1=D()
with open("myobj.pickle","wb") as f:
    pickle.dump(d1,f)

#注意d2从pickle中load之前，必须要能知道class D，del D会导致反序列化失败
#del D
with open("myobj.pickle","rb") as f:
    d2 = pickle.load(f)


print(d2.a.a)