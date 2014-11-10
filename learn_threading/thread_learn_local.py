import threading

local = threading.local()

local.tname = 'main'

def func():
    local.tname='notmain'
    print local.tname
def func2():

    local.tname='haha'
    print local.tname

t1=threading.Thread(target=func)
t2=threading.Thread(target=func2)
t1.start()
t2.start()
t1.join()
print local.tname