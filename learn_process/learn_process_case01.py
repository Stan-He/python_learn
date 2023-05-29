from multiprocessing import Process
import time
class A(object):
    def __init__(self):
        self.a="a"
    
    def start(self):
        i=0 
        while i<10:
            print(i)
            i+=1
    
    def stop(self):
        pass

a=A()
p = Process(target=a.start)
p.start()
print(p.pid)
time.sleep(7)
p.terminate()