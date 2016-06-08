import sys
import time
# Creates a list of all interfaces to assure the user used the correct input


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
                    " |bytes       packets       errs     |bytes       "+
                    "packets       errs"))
    return header_tuple


# Makes data in Bytes human readable
def human_read(data):
    data_sizes = ['Bps', 'KBps', 'MBps', 'GBps', 'TBps']
    if (data) == 0:
        return '0Bps'
    i = 0
    while data >= 1024 and i < len(data_sizes) - 1:
            data /= 1024
            i += 1
    new_number = ('%.2f' % data)
    return str(str(new_number) + str(data_sizes[i]))


def main_bw_test():
    prevBI = 0
    prevBO = 0
    prevPI = 0
    prevPO = 0
    prevEI = 0
    prevEO = 0
    times_run = 0
    if len(sys.argv) != 2:
        print("Number of arguments incorrect")
        sys.exit()
    devname = str(sys.argv[1])
    while True:
        try:
            with open('/proc/net/dev', 'r') as dev_file:
                interf = devname + ':'
                if str(interf) not in interfaces():
                    sys.exit("Please use a valid interface name.")
                else:
                    # At the 200th char
                    try:
                        dev_file.seek(200)
                        for line in dev_file:
                            arr = line.split()
                            if str(arr[0]) == str(interf):
                                name = str(arr[0])
                                if times_run % 10 == 0:
                                    new_tup =  header(name)
                                    print new_tup[0]
                                    print new_tup[1]
                                bytes_in = human_read(int(arr[1]) - prevBI)
                                bytes_out = human_read(int(arr[9]) - prevBO)
                                packet_in = human_read(int(arr[2]) - prevPI)
                                packet_out = human_read(int(arr[10]) - prevPO)
                                errors_in = human_read(int(arr[3]) - prevEI)
                                errors_out = human_read(int(arr[11]) - prevEO)
                                # 66 chars in the header after the initial |.
                                dev_info = str((' ' *
                                               len(name) + '  ') + bytes_in +
                                               ' ' * (12 - len(bytes_in)) +
                                               packet_in + ' ' *
                                               (14-len(packet_in)) +
                                               errors_in +
                                               ' ' * (10-len(errors_in)) +
                                               bytes_out + ' ' *
                                               (12-len(bytes_out)) +
                                               packet_out + ' ' *
                                               (14-len(packet_out)) +
                                               errors_out)
                                print (dev_info)
                                # Set prev sizes equal to curr sizes
                                prevBI = int(arr[1])
                                prevBO = int(arr[9])
                                prevPI = int(arr[2])
                                prevPO = int(arr[10])
                                prevEI = int(arr[3])
                                prevEO = int(arr[11])
                                times_run += 1
                                time.sleep(1)
                    except:
                        print("file format incorrect")
                        sys.exit()
        except IOError:
            print("'/proc/net/dev' not available. ")
            sys.exit()

if __name__ == "__main__":
   main_bw_test()
