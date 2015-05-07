import socket
import select
import threading
import sys

HOST = '127.0.0.1'  # Symbolic name meaning all available interfaces
PORT = 5963    # Arbitrary non-privileged port
addr = (HOST, PORT)


def socket_ready_to_connect():
    # creat a socket ready to connect
    # s = None
    # for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
    #     af, socktype, proto, canonname, sa = res
    #     try:
    #         s = socket.socket(af, socktype, proto)
    #     except socket.error as msg:
    #         s = None
    #         continue
    #     try:
    #         s.connect(sa)
    #     except socket.error as msg:
    #         s.close()
    #         s = None
    #         continue
    #     break
    # if s is None:
    #     print 'could not open socket'
    #     sys.exit(1)

    s = socket.socket()
    s.connect(addr)
    return s


def receave_from_server(s):
    my_inputs = [s]
    while True:
        r, w, e = select.select(my_inputs, [], [])
        if s in r:
            try:
                print s.recv(1024)
            except Exception, e:
                print e
                exit()
        else:
            print 's is not in r'


def talk(s):
    while True:
        try:
            info = raw_input()
        except Exception, e:
            print e
            exit()
        try:
            s.send(info)
        except Exception, e:
            print e
            exit()


def main():
    ss = socket_ready_to_connect()
    receive_threading = threading.Thread(target=receave_from_server, args=(ss,))
    receive_threading.start()
    talking_threading = threading.Thread(target=talk, args=(ss,))
    talking_threading.start()


if __name__ == '__main__':
    main()