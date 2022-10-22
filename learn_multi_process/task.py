import logging
import multiprocessing
#指定有层级关系的log名字，都能获取到add到
log = logging.getLogger("main")

class Task(object):
    def __init__(self):
        log.info(log.handlers)
        log.info("2--task init")

    def run_task(self):
        log.info("3--running a task")