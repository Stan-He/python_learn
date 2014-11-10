# -*- coding=UTF-8 -*-

import threading
import time

#计算器初值为2
semaphore = threading.Semaphore(1)

def func(name):
    print "%s acuire semaphore..." % threading.currentThread().getName()
    
    if semaphore.acquire():
        print "%s get a semaphore." % threading.currentThread().getName()
        for i in range(5):
            print "%s : %d" % (name,i)
            time.sleep(0.3)
        print "%s reelase a semaphore." % threading.currentThread().getName()
        semaphore.release()
        
t1 =  threading.Thread(target=func,args=("t1",))
t2 =  threading.Thread(target=func,args=("t2",))
t3 =  threading.Thread(target=func,args=("t3",))
t4 =  threading.Thread(target=func,args=("t4",))
t1.start()
t2.start()
t3.start()
t4.start()

semaphore.release()