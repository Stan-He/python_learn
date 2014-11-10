# encoding:UTF-8
import random
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_shuffle(self):
        # make sure the shuffled sequence does not lose any elements
        #随机排序
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, range(10))

        # should raise an exception for an immutable sequence
        self.assertRaises(TypeError, random.shuffle, (1,2,3))

    def test_choice(self):
        element = random.choice(self.seq)
        #self.assertTrue(element in self.seq)
        self.assertIn(element, self.seq, msg='不在seq里')

    def test_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)
"""
if __name__ == '__main__':
    unittest.main()
"""

#把testcase添加到suite中
suite1 = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
suite2 = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
#整合到suite中
suite= unittest.TestSuite([suite1,suite2])
#把suite传递给run
unittest.TextTestRunner(verbosity=2).run(suite)