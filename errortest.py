import unittest
from bwtest import human_read, interfaces, header

class Test(unittest.TestCase):
    
    def test_human_read(self):
        self.failUnlessEqual(human_read(1), "1.00Bps")
        self.failUnlessEqual(human_read(2000), "1.00KBps")
        self.failUnlessEqual(human_read(2500000), "2.00MBps")
        self.failUnlessEqual(human_read(0), "0Bps")


    def test_interfaces(self):
        self.failUnlessEqual(interfaces(), ['Inter-|', 'face', 'enp68s0f0:', 'enp67s0f1:', 'eno1:', 'eno2:', 'eno3:', 'eno4:', 'enp67s0f0:', 'lo:', 'virbr0-nic:', 'virbr0:', 'enp68s0f1:'])


    def test_header(self):
        eno1 = "eno1"
        test_tup = ((str(eno1 +
                    " |   Receive                         |  Transmit"),
                    str(" " * len(eno1) +
                    " |bytes       packets       errs     |bytes       "+
                    "packets       errs")))
        self.failUnlessEqual(header(eno1), (test_tup))
if __name__ == '__main__':
    unittest.main()
