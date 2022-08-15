

"""
concurrent 的优势在于提供了 ThreadPoolExecutor 和 ProcessPoolExecutor
一个多线程，一个多进程。但 concurrent 本质上都是对 threading 和 multiprocessing 的封装。看它的源码可以知道，所以最底层并没有异步
"""

#创建线程池
from asyncio import as_completed
from concurrent import futures
import random
from os import getegid

pool = futures.ThreadPoolExecutor(max_workers =3)

#pool.submit：该方法的作用是提交一个可执行的回调task，返回一个Future对象，可以用result获取方法调用的返回值，配合wait使用
import requests, datetime, time
def get_results(url):
    r = requests.get(url)
    
    print(f"{datetime.datetime.now()}:{url}:{r.status_code}")
    return r.status_code

urls = ['https://www.baidu.com','https://www.tmall.com','https://www.jd.com']

with futures.ThreadPoolExecutor(max_workers=5) as executor:
    tasks = [executor.submit(get_results,url) for url in urls]
    for task in futures.as_completed(tasks):
        print(task.result())