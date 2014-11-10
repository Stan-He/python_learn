# encoding: UTF-8
import thread
import time

def func():
    for i in range(8):
        print i
        time.sleep(1)
    thread.exit()

thread.start_new(func, ()) #启动这个线程

lock = thread.allocate_lock()
print lock.locked()

count=0
if lock.acquire():
    count +=1
    lock.release()
time.sleep(10)