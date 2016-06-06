import sys
import time


# Creates a list of all interfaces to assure the user used the correct input
def interfaces():
    try:
        with open('/proc/net/dev', 'r') as dev_file:
            interface_list = []
            for line in dev_file:
                arr = line.split()
                try:
                    interface_list.append(arr[0])
                except IndexError:
                    print("File format incorrect")
                    sys.exit()
            return interface_list
    except Error:
        print ("File /proc/net/dev not found")


# Prints the header
def header(name):
    print (name + " |   Receive                         |  Transmit")
    print (" " * len(name) +
           " |bytes       packets       errs     |bytes       " +
           "packets       errs")


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


def main():
    prevBI = 0
    prevBO = 0
    prevPI = 0
    prevPO = 0
    prevEI = 0
    prevEO = 0
    times_run = 0
    try:
        devname = str(sys.argv[1])
    except:
        print("File format incorrect")
        sys.exit
    while True:
        try:
            with open('/proc/net/dev', 'r') as dev_file:
                continue 
        except EnvironmentError:
            print("/proc/net/dev file does not exist")
            sys.exit()
        interf = devname + ':'
        if str(interf) not in interfaces():
            sys.exit("Please use a valid interface name.")
        else:
            # At the 200th char
            #dev_file.seek(200)
            try:
                after_scnd_line = dev_file.readlines()[2:]
            except:
                print("/proc/net/dev file too short.")
                sys.exit()
            for line in after_scnd_lin:
                arr = line.split()
                if str(arr[0]) == str(interf):
                    try: 
                        name = str(arr[0])
                    except IndexError:
                        print("File format incorrect")
                        sys.exit()
                    if times_run % 10 == 0:
                        header(name)
                    try:    
                        bytes_in = human_read(int(arr[1]) - prevBI)
                        bytes_out = human_read(int(arr[9]) - prevBO)
                        packets_in = human_read(int(arr[2]) - prevPI)
                        packets_out = human_read(int(arr[10]) - prevPO)
                        errors_in = human_read(int(arr[3]) - prevEI)
                        errors_out = human_read(int(arr[11]) - prevEO)
                    except ValueError:
                        ("File format incorrect")
                        sys.exit()
                    # 66 chars in the header after the initial |.
                    dev_info = str((' ' *
                                    len(name) + '  ') + bytes_in +
                                   ' ' * (12 - len(bytes_in)) +
                                   packets_in + ' ' *
                                   (14-len(packets_in)) + errors_in +
                                   ' ' * (10 - len(errors_in)) +
                                   bytes_out + ' ' *
                                   (12-len(bytes_out)) +
                                   packets_out + ' ' *
                                   (14-len(packets_out)) + errors_out)
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
if __name__ == "__main__":
    main()
