#!/usr/bin/env Python
import os 
import sys
import datetime
import time
import signal
# Creates a list of all interfaces to assure the user used the correct input

class curr_prev_holder(object):
    devicename = "eno1"
    #   prevs
    prevBI = 0
    prevBO = 0
    prevPI = 0
    prevPO = 0
    prevEI = 0
    prevEO = 0
    #   currs
    bytes_in = 0
    packet_in = 0
    errors_in = 0
    bytes_out = 0
    packet_out = 0
    errors_out = 0
    #    times
    times_run = 0
    #    creating a file
    text_file = open("graphable.dat", 'w')
    text_file.write(devicename)
    text_file.write("\n TIMESTAMP    [rx]bytes  [rx]packets  [rx]errs" +
                    "  " + "[tx]bytes  [tx]packets  [tx]errs")

    def __init__(self, interface):
        self.interface = interface

    # Makes data in Bytes human readable
    def human_read(self, data):
        data_sizes = ['Bps', 'KBps', 'MBps', 'GBps', 'TBps']
        if (data) == 0:
            return '0.00Bps'
        i = 0
        while data >= 1024 and i < len(data_sizes) - 1:
                data /= 1024.0
                i += 1
        new_number = ('%.2f' % data)
        return str(str(new_number) + str(data_sizes[i]))

    def set_prvs(self, arr):
        self.devicename = str(arr[0])
        self.prevBI = int(arr[1])
        self.prevBO = int(arr[9])
        self.prevPI = int(arr[2])
        self.prevPO = int(arr[10])
        self.prevEI = int(arr[3])
        self.prevEO = int(arr[11])

    def set_currs(self, arr):
        self.bytes_in = self.human_read(int(arr[1]) - self.prevBI)
        self.bytes_out = self.human_read(int(arr[9]) - self.prevBO)
        self.packet_in = self.human_read(int(arr[2]) - self.prevPI)
        self.packet_out = self.human_read(int(arr[10]) - self.prevPO)
        self.errors_in = self.human_read(int(arr[3]) - self.prevEI)
        self.errors_out = self.human_read(int(arr[11]) - self.prevEO)
        currtime = str(time.time())
        self.text_file.write("\n"+ currtime + ' ' + 
                             str(int(arr[1]) - self.prevBI) + ' ' +
                             str(int(arr[2]) - self.prevPI) + ' ' +
                             str(int(arr[3]) - self.prevEI) + ' ' +
                             str(int(arr[9]) - self.prevBO) + ' ' +
                             str(int(arr[10]) - self.prevPO) + ' ' +
                             str(int(arr[11]) - self.prevEO) + ' ')

    def new_dev_info(self):
        return str((' ' + ' ' *
                   len(self.interface) + '  ') + self.bytes_in +
                   ' ' * (12 - len(self.bytes_in)) +
                   self.packet_in + ' ' *
                   (14-len(self.packet_in)) +
                   self.errors_in +
                   ' ' * (10-len(self.errors_in)) +
                   self.bytes_out + ' ' *
                   (12-len(self.bytes_out)) +
                   self.packet_out + ' ' *
                   (14-len(self.packet_out)) +
                   self.errors_out)

    def data_arr(self, devname, filename):
        interf = devname + ':'
        self.devicename = str(interf)
        interfaces(interf)
        try:
            with open(filename, 'r') as dev_file:
                try:
                    dev_file.seek(200)
                    for line in dev_file:
                        arr = line.split()
                        if str(arr[0]) == str(interf):
                            name = str(arr[0])
                            if self.times_run % 10 == 0:
                                new_tup = header(name)
                                print new_tup[0]
                                print new_tup[1]
                            self.times_run += 1
                            return arr
                except KeyboardInterrupt:
                    c_gracefully()
                    self.text_file.close()
                except:
                    print("file format incorrect")
                    sys.exit()
        except IOError:
            print("'/proc/net/dev' not available. ")

def interfaces(interf):
   with open('/proc/net/dev', 'r') as dev_file:
       interface_list = []
       for line in dev_file:
           arr = line.split()
           interface_list.append(arr[0])
       if str(interf) not in interface_list:
           try:
               raise IOError
           except IOError:
               print('Please use the right interface device')

def c_gracefully():
     print (' System exiting...')
     sys.exit()

def header(name):
    header_tuple = (str(name +
                    " |   Receive                         |  Transmit"),
                    str(" " * len(name) +
                    " |bytes       packets       errs     |bytes       " +
                        "packets       errs"))
    return header_tuple

def get_dev():
    try:
        dev = str(sys.argv[1])
    except IndexError:
        print ("Please call with a device name")
        sys.exit()
    dev = str(sys.argv[1])
    return dev

def main_bw_test():
    devname = get_dev()
    bw_info = curr_prev_holder(devname)
    while True:
        arr = bw_info.data_arr(devname, '/proc/net/dev')
        bw_info.set_currs(arr)
        dev_info = bw_info.new_dev_info()
        print (dev_info)
        bw_info.set_prvs(arr)
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            bw_info.text_file.close()
            c_gracefully() 

if  __name__ == "__main__":
    main_bw_test()
