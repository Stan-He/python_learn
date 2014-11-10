#-*-coding=UTF-8 -*-
import threading
import time

product = None
con =  threading.Condition()

def produce():
    global product
    if con.acquire():
        while True:
            if product is None:
                print "producing....."
                product="anything"
                
                con.notify()
            con.wait()
            time.sleep(0.1)
            
def consume(name):
    global product
    if con.acquire():
        while True:
            if product is not None:
                print '%s is consume...' % name
                product= None
        
                con.notify()
            else:
                print '%s is noticing the producer...' %name
                con.notify()
    
            con.wait()
            time.sleep(0.5)

t1 = threading.Thread(target=produce)
t0 = threading.Thread(target=produce)
t2 = threading.Thread(target=consume,args=("Tom",))
t3 = threading.Thread(target=consume,args=("Jack",))
t4 = threading.Thread(target=consume,args=("dick",))
t0.start()
t1.start()
t2.start()
t3.start()
t4.start()
    