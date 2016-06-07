import unittest
from bwtest import human_read

class Test(unittest.TestCase):
    def test_basic_addition(self):
        self.failUnlessEqual(human_read(1), "1.00Bps")
        self.failUnlessEqual(human_read(2000), "1.00KBps")
        self.failUnlessEqual(human_read(2500000), "2.00MBps")
        self.failUnlessEqual(human_read(0), "0Bps")

if __name__ == '__main__':
	unittest.main()

