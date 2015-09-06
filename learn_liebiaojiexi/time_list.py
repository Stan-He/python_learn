#from l1_true import l1_true
#from l1_false import l1_false
from timeit import Timer
L=range(1000)
#print l1_true(L)
#print l1_false(L)
import datetime
def l1_true(L):
    a=[x*x for x in L]
    return None
def l1_false(L):
    a=[]
    for i in L:
        a.append(i*i)
    return None

def l2_true(L):
    result=[x  for i in L for x in i]
    return None
def l2_false(L):
    a=[]
    for i in L:
        for x in i:
            a.append(x)




def timefun(f,n=1000,args=None):
    starttime=datetime.datetime.now()
    for i in range(n):
        f(args)
    endtime=datetime.datetime.now()
    result=(endtime-starttime).seconds
    return result*1.0/n

#print 't1_true:',timefun(l1_true,n=10000,args=range(10000))
#print 't1_false',timefun(l1_false,n=10000,args=range(10000))
#t1=Timer('l1_true()','from __main__ import l1_true')
#t2=Timer('l1_false()','from __main__ import l1_false')
#print 't1:',t1.repeat(10)
#print 't2:',t2.repeat(10)
L=[[i,i+1] for i in range(10000)]
print 'l2_true:',timefun(l2_true,n=10000,args=L)
print 'l2_false',timefun(l2_false,n=10000,args=L)
