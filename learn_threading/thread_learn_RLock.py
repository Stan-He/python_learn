# -*- coding=UTF-8 -*-
import threading
import time

rlock=threading.RLock()
data=0
"""
RLock使用了“拥有的线程”和“递归等级”的概念，处于锁定状态时，RLock被某个线程拥有。拥有RLock的线程可以再次调用acquire()，释放锁时需要调用release()相同次数。
可以认为RLock包含一个锁定池和一个初始值为0的计数器，每次成功调用 acquire()/release()，计数器将+1/-1，为0时锁处于未锁定状态。
"""

def func():
    print (f'{threading.current_thread().name} acquire lock...')
    if rlock.acquire():
        print (f'{threading.current_thread().name} get lock...')
        time.sleep(2)
        
        print (f'{threading.current_thread().name} acquire lock again...')
        if rlock.acquire():
            print (f'{threading.current_thread().name} get lock again...')
            global data
            data+=1
            print(data)
            time.sleep(2)
        
        print (f'{threading.current_thread().name} release...')
        rlock.release()
        time.sleep(2)
        print (f'{threading.current_thread().name} release...')
        rlock.release()
        
t1=threading.Thread(target=func)
t2=threading.Thread(target=func)
t3=threading.Thread(target=func)
t1.start()
t2.start()
t3.start()