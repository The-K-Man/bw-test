import sys
import unittest
from bwtest import human_read, interfaces, header

class Test(unittest.TestCase):
    
    def test_human_read(self):
        self.failUnlessEqual(human_read(1), "1.00Bps")
        self.failUnlessEqual(human_read(2000), "1.00KBps")
        self.failUnlessEqual(human_read(2500000), "2.00MBps")
        self.failUnlessEqual(human_read(0), "0Bps")


    def test_interfaces(self):
        self.failUnlessEqual(interfaces(), interfaces())


    def test_header(self):
        eno1 = "eno1"
        test_tup = ((str(eno1 +
                    " |   Receive                         |  Transmit"),
                    str(" " * len(eno1) +
                    " |bytes       packets       errs     |bytes       "+
                    "packets       errs")))
        self.failUnlessEqual(header(eno1), (test_tup))


    #def test_main(self):
        #self.assertRaises(IOError, main_bw_test())


if __name__ == '__main__':
    for i in sys.argv:
        print i
    unittest.main()
