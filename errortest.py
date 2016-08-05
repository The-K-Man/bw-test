import unittest
import signal
import mock
import sys
from mock import patch
from bwtest import interfaces, header, c_gracefully, get_dev
from bwtest import curr_prev_holder

class Test(unittest.TestCase):

    def test_dev(self):
        #with self.assertRaises(SystemExit) as cm:
            #get_dev()
            #self.assertEqual(cm.exception.code, 0)
        sys.argv = ["errortest.py", "lo"] 
        print (get_dev())

    def test_c(self):
            with self.assertRaises(SystemExit) as cm:
                c_gracefully()

    def test_interfaces(self):
        self.failUnlessEqual(interfaces("lo:"), interfaces("lo:"))
        self.assertRaises(IOError , interfaces("lololol"))

    def test_data_arr(self):
        tfile = 'testfile.txt'
        x = curr_prev_holder("lo")
        self.failUnlessEqual(x.data_arr("lo", tfile), ['lo:', '0', '0', '0',
                                                       '0', '0', '0', '0',
                                                       '0', '0', '0', '0',
                                                       '0', '0', '0', '0',
                                                       '0'])
        self.assertRaises(IOError, x.data_arr("lo", 'randomtext.txt'))

    def test_header(self):
        eno1 = "eno1"
        test_tup = ((str(eno1 +
                         " |   Receive                         |  Transmit"),
                     str(" " * len(eno1) +
                     " |bytes       packets       errs     |bytes       " +
                         "packets       errs")))
        self.failUnlessEqual(header("eno1"), (test_tup))

    def test_class_human(self):
        x = curr_prev_holder("eno1")
        self.failUnlessEqual(x.human_read(1), "1.00Bps")
        self.failUnlessEqual(x.human_read(2000), "1.95KBps")
        self.failUnlessEqual(x.human_read(2500000), "2.38MBps")
        self.failUnlessEqual(x.human_read(0), "0.00Bps")

    def test_class(self):
        arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        x = curr_prev_holder("eno1")
        x.set_currs(arr)
        x.set_prvs(arr)
        self.failUnlessEqual(x.prevPO, 10)
        self.failUnlessEqual(x.bytes_in, "1.00Bps")

    def test_printer(self):
        arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        x = curr_prev_holder("eno1")
        x.set_currs(arr)
        x.set_prvs(arr)
        self.failUnlessEqual(x.new_dev_info(), "       1.00Bps     2.00Bps       3.00Bps   9.00Bps     10.00Bps      11.00Bps")

if __name__ == '__main__':
    unittest.main()
