# Threaded-PortScanner
Portscanning tool written in python 3 with the use of threading to make it faster and more efficient and argparse to easily scan ports from the terminal. Tried to follow PEP8 as much as possible

# Flags and usage
*usage: portscanner.py [-h] [-u] [-p PORT] target*

##### positional arguments:
- [x] target - The IP address or hostname you would like to scan

##### optional arguments:
- [x] -h, --help - show this help message and exit
- [x] -u, --udp - to include UDP ports as well
- [x] -p PORT, --port PORT - specify the ports you want to scan divided by commas(,) or dashes(-) if you want an range, example: *portscan -p 1-1024,666,1337 10.3.3.3*

### Demo
![Demo of the portscanner](https://github.com/jlhk/Threaded-PortScanner/blob/master/portscan_demo_v2.gif)
