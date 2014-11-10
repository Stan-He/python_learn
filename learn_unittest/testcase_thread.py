#coding=utf-8
import threading
import time
import unittest
import fileinput
from search_test_case import SearchTestCase

class testCaseThread (threading.Thread):
    def __init__(self, ip_port,suites):
        threading.Thread.__init__(self)
        self.ip_port = ip_port
        self.suite = suites
        self.all_case_num = 0
        self.fail_case_num = 0
    def run(self):
        res =  unittest.TextTestRunner().run(self.suite)
        self.all_case_num = res.testsRun
        self.fail_case_num = len(res.failures)

if __name__=='__main__':
    startTime = time.time()
    lines = []
    threads = []
    for line in fileinput.input("ip_port_conf.txt"):
        lines.append(line.strip())
    print lines
    for line in lines:
        thread = testCaseThread(line,SearchTestCase(line).load_all_testcase())
        threads.append(thread)
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    print "runing end!\n"
    print 'ip_port,allcasenum,failcasenum'
    for th in threads:
        print th.ip_port+','+str(th.all_case_num)+','+str(th.fail_case_num)
    stopTime = time.time()
    timeTaken = stopTime - startTime
    print '\nruning cost '+ ("%.2f" % timeTaken) +' s'
        