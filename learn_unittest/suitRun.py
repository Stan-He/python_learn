# encoding=UTF-8
import yantu_search #载入沿途搜索用例
import unittest

#沿途搜索测试集
suite_yantu = unittest.TestLoader().loadTestsFromTestCase(yantu_search.YantuSearchTestClass)
#回归测试集
suit_regression=unittest.TestSuite(suite_yantu)
#执行回归测试
unittest.TextTestRunner(verbosity=2).run(suit_regression)