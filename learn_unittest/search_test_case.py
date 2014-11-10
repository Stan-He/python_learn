#coding=utf-8
import unittest
import time

class TestSequenceFunctions(unittest.TestCase):
    def __init__(self, testName, ip_port):
        unittest.TestCase.__init__(self,testName)
        self.ip_port = ip_port
        
    def setUp(self):
        self.seq = range(10)
        
    def test_shuffle(self):
        self.assertEqual(33, 33)

    def test_choice(self):
        self.assertEqual(33, 33)
 
    def test_sample(self):
        time.sleep(1)
        print 'ip_port'+self.ip_port
        self.assertEqual(33, 33)

class TestDictValueFormatFunctions(unittest.TestCase):
    def __init__(self, testName, ip_port):
        unittest.TestCase.__init__(self,testName)
        self.ip_port = ip_port
        
    def test_choice1(self):
        self.assertEqual(34, 33)
        
    def test_choice2(self):
        self.assertEqual(33, 33)
        
class SearchTestCase():
    def __init__(self, ip_port):
        self.ip_port = ip_port
        self.suites = unittest.TestSuite()
    def load_testcaseclass(self,testcaseclass): 
        testnames = unittest.TestLoader().getTestCaseNames(testcaseclass)
        for tn in testnames:
            self.suites.addTest(testcaseclass(tn,self.ip_port))
        return self.suites
    
    def load_all_testcase(self):
        self.load_testcaseclass(TestSequenceFunctions)
        self.load_testcaseclass(TestDictValueFormatFunctions)
        return self.suites