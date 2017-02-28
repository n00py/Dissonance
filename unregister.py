from __future__ import absolute_import, division, print_function, unicode_literals

import socket
from zeroconf import ServiceInfo, Zeroconf

def get_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('8.8.8.8', 53))
    ip = sock.getsockname()[0]
    sock.close()
    return ip

def main():
    zeroconf = Zeroconf()
    ip_addr = get_ip()
    hostname = "192.168.250.1"
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
        zeroconf.unregister_service(info)

    try:
        raw_input("Waiting (press Enter to exit)...")
    finally:
        print("Unregistering...")
        zeroconf.unregister_service(info)
        zeroconf.close()


if __name__ == '__main__':
    print('Starting zeroconf publishing service')
    main()
else:
    print("Do not import this file")
    print(__name__)

