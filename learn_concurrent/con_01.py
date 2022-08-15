

"""
concurrent 的优势在于提供了 ThreadPoolExecutor 和 ProcessPoolExecutor
一个多线程，一个多进程。但 concurrent 本质上都是对 threading 和 multiprocessing 的封装。看它的源码可以知道，所以最底层并没有异步
"""

#创建线程池
from concurrent import futures
from multiprocessing import pool
import random
from os import getegid

pool = futures.ThreadPoolExecutor(max_workers =3)

#pool.submit：该方法的作用是提交一个可执行的回调task，返回一个Future对象，可以用result获取方法调用的返回值，配合wait使用
import requests, datetime, time
def get_results(url,enable_error=False):
    r = requests.get(url)
    if enable_error and random.randint(0,2)==1:
        raise Exception("dummy exception")
    print(f"{datetime.datetime.now()}:{url}:{r.status_code}")
    return r.status_code

urls = ['https://www.baidu.com','https://www.tmall.com','https://www.jd.com']

print("######################1##########################")
for url in urls:
    task = pool.submit(get_results,url)
print("main process")
time.sleep(1)

print("######################2##########################")
#map的方法
tasks = pool.map(get_results,urls)
for result in tasks:
    print(result)
time.sleep(1)

print("######################3##########################")
tasks=[]
for url in urls:
    task = pool.submit(get_results,url)
    tasks.append(task)
futures.wait(tasks)
for task in tasks:
    print(task.result())
print("waiting for all tasks done at main process")


print("######################5##########################")
#异常捕获
urls = ['www.baidu.com','https://www.tmall.com','https://www.jd.com']

tasks=[]
for url in urls:
    task = pool.submit(get_results,url,True)
    tasks.append(task)

errors = futures.as_completed(tasks)
for error in errors:
    #error.result()
    print(error.exception())

futures.wait(tasks)
print("waiting for all tasks done at main process")
for task in tasks:
    print(task.result())
