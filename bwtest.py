import os 
import sys
import time
import signal
# Creates a list of all interfaces to assure the user used the correct input


class curr_prev_holder(object):
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
        try:
            with open(filename, 'r') as dev_file:
                interf = devname + ':'
                if str(interf) not in interfaces():
                    sys.exit("Please use a valid interface name.")
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
                except:
                    print("file format incorrect")
                    sys.exit()
        except IOError:
            print("'/proc/net/dev' not available. ")


def interfaces():
    with open('/proc/net/dev', 'r') as dev_file:
        interface_list = []
        for line in dev_file:
            arr = line.split()
            interface_list.append(arr[0])
        return interface_list


# Prints the header
def header(name):
    header_tuple = (str(name +
                    " |   Receive                         |  Transmit"),
                    str(" " * len(name) +
                    " |bytes       packets       errs     |bytes       " +
                        "packets       errs"))
    return header_tuple

def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)
    try:
        if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
            sys.exit(1)

    except KeyboardInterrupt:
        raise
        print("Ok ok, quitting")
        sys.exit()

    # restore the exit gracefully handler here
    signal.signal(signal.SIGINT, exit_gracefully)

def main_bw_test():
    if len(sys.argv) != 2:
        print("Number of arguments incorrect")
        sys.exit()
    devname = str(sys.argv[1])
    bw_info = curr_prev_holder(devname)
    while True:
        arr = bw_info.data_arr(devname, '/proc/net/dev')
        bw_info.set_currs(arr)
        dev_info = bw_info.new_dev_info()
        print (dev_info)
        bw_info.set_prvs(arr)
        time.sleep(1)


if __name__ == "__main__":
    pid = os.getpid()
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    main_bw_test()
