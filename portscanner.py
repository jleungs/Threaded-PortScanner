#!/usr/bin/env python3
'''
Simple portscanning tool written in python 3 with the use of threading to
make it faster and more efficient.
Written by Jonathan Leung
TODO: Generate an report argument and function, scanning multiple hosts(a subnet)
'''
import argparse
import socket
from threading import Lock, Thread, main_thread # Only importing the ones being used
from time import time

def port_scan(port):
    '''The port scan function to see which ports are open, prints if it finds
    one and adds +1 to the PORTS_FOUND to be able to print the amount of ports
    found'''
    with PORT_LOCK:
        global PORTS_FOUND
    # Getting the sockets for both UDP and TCP connections
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tcp_socket.connect((TARGET, port)) # Tries the connection
        with PRINT_LOCK:
            print('[TCP] Open port:', port, '| Service:',
                  socket.getservbyport(port, 'tcp'))
        PORTS_FOUND += 1 # Counts the amount of ports opened
        tcp_socket.close()
    except socket.error: # If the port is not opened, pass, do nothing
        pass
    if ARGS.udp: # If the UDP flag is used, SOCK_DGRAM = UDP socket
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            udp_socket.connect((TARGET, port)) # Tries the connection
            with PRINT_LOCK:
                print('[UDP] Open port:', port, '| Service:',
                      socket.getservbyport(port, 'udp'))
            PORTS_FOUND += 1 # Counts the amount of ports opened
            udp_socket.close()
        except socket.error: # If the port is not opened, pass, do nothing
            pass

def arguments():
    '''To get the IP address or hostname of the target to scan using argparse'''
    parser = argparse.ArgumentParser(description='Portscanner with threading')
    parser.add_argument('target', help='The IP address or hostname you '
                        'would like to scan', type=str) # Gets the IP/hostname of the target
    parser.add_argument('-u', '--udp', help='to include UDP ports as well',
                        action='store_true') # Flag for UDP scan
    # For specifying ports and portrange
    parser.add_argument('-p', '--port', help='specify the ports you want to '
                        'scan divided by commas(,) or dashes(-) if you want an range, '
                        'example: portscan -p 1-1024,666,1337 10.3.3.3', type=str)
    args = parser.parse_args()
    return args # Returns the parser to easily use the arguments

def threader(ports):
    '''This initialize the threads to work on specific ports'''
    with PORT_LOCK:
        global PORT_COUNT
    for port in ports: # Loops the ports as an argument for port_scan
        while PORT_COUNT < len(ports):
            with PORT_ADDING_LOCK:
                PORT_COUNT += 1
            port = ports[PORT_COUNT-1]
            port_scan(int(port))
            if PORT_COUNT > len(ports):
            # To make sure that all threads stop when the last port is scanned and
            # not only one
                main_thread().join()

def getting_ports():
    '''Getting the ports to scan and checking if it is specified by the user'''
    new_ports = []
    if ARGS.port:
        print('Scanning ports:', ARGS.port)
        ports = ARGS.port.split(',') # Splits the ports divided by commas
        for port in ports:
            if '-' in port: # Looks if it's a port range specified
                port = port.split('-')
    # If both arguments given between a dash is numbers and the second is larger
    # than the first, loops between that
                if port[0].isdigit() and port[1].isdigit() and int(port[0]) < int(port[1]):
                    for single_port in range(int(port[0]), int(port[1])+1):
                        new_ports.append(single_port)
                else:
                    print('Wrong port format..')
                    exit()
            elif port.isdigit(): # If it's an integer, adds it to the port list
                new_ports.append(port)
            else: # If it's not an int or has '-' in it, it's the wrong format
                print('Wrong port format..')
                exit()
    else:
        print('Scanning every port possible')
        for port in range(1, 0xffff+1):
            new_ports.append(port)
    return new_ports

def getting_target():
    '''Check for the IP/hostname given by the user'''
    target = ARGS.target.strip()
    try:
        socket.inet_aton(target)
        return target
    except (socket.error, OSError):
        try:
            socket.gethostbyname(target)
            return target
        except (socket.error, socket.gaierror):
            print('Unable to find the IP from the hostname')
            exit()

if __name__ == '__main__':
    START_TIME = time() # Getting the time before starting, to calculate the amount it took to run
    # The locks are needed to not screw up a variable or the print function
    PRINT_LOCK = Lock()
    PORT_LOCK = Lock()
    PORT_ADDING_LOCK = Lock()
    ARGS = arguments()
    TARGET = getting_target() # Getting the IP or hostname to scan
    FANCY_HEADER = '='*(54)
    print(FANCY_HEADER+'\nScanning ports for: '+TARGET+'\nThe service '
          'is based on the PORT, not actually checked\n'+FANCY_HEADER)
    # Starts at 0 because it gets +1 before being used as an argument in the
    # port_scan function, does not actually scan port 0
    PORT_COUNT = 0
    PORTS_FOUND = 0 # Counts the amount of ports scanned
    PORTS = getting_ports() # Getting a list of ports to scan
    for worker in range(300): # Starts 300 threads
# Setting daemon to true so you only have to kill the main thread, to kill all
        thread = Thread(target=threader, args=(PORTS,), daemon=True)
        thread.start() # Getting the workers to work

    print('[!] Found {} ports open'.format(PORTS_FOUND))
    print('[DONE] The scan took {0:.3f} seconds'.format(time() - START_TIME))
