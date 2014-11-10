# -*- coding=UTF-8 -*-
import threading
import time

rlock=threading.RLock()
data=0

def func():
    print '%s acquire lock...' % threading.currentThread().getName()
    if rlock.acquire():
        print '%s get lock...' % threading.currentThread().getName()
        time.sleep(2)
        
        print '%s acquire lock again...' % threading.currentThread().getName()
        if rlock.acquire():
            print '%s get lock...' % threading.currentThread().getName()
            global data
            data+=1
            print data
            time.sleep(2)
        
        print '%s release lock...' % threading.currentThread().getName()
        rlock.release()
        time.sleep(2)
        print '%s release lock...' % threading.currentThread().getName()
        rlock.release()
        
t1=threading.Thread(target=func)
t2=threading.Thread(target=func)
t3=threading.Thread(target=func)
t1.start()
t2.start()
t3.start()