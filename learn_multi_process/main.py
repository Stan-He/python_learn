from multiprocessing import Process
import multiprocessing
from task import Task
import logging
import os
"""
1、logging和multi-processing无关，无论是import的submodule还是multiprocess，只要logger的名字正确，都能打印
2、logging 具有层级结构，logging.basicConfig，相当于配置了默认的root-logger
3、basicConfig默认是stream logging，如果配置了handler就会覆盖这个logger
4、getLogger的作用是创建一个新的logger，或者获取一个已有的logger
"""

logfile = "mylog.log"
path = os.path.join(os.path.dirname(os.path.abspath(__file__)),logfile)
path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)),"mylog2.log")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s",
    filename=path,
    filemode = "w"
    )

handler = logging.FileHandler(filename=path2, mode="w")

log = logging.getLogger("main")
log.addHandler(handler)


log.info("******1--start main.py**********")
log.info("-----------multiprocess-----------------")
t = Task()
p = Process(target=t.run_task)
p.start()
p.join()
log.info("-----------no multiprocess-----------------")
t= Task()
t.run_task()

log.info("4--end main.py")