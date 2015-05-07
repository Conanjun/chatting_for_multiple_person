import socket
import select
import thread
import sys

HOST = '127.0.0.1'  # Symbolic name meaning all available interfaces
PORT = 5963    # Arbitrary non-privileged port

inputs = []
online_people = {}


def socket_ready_to_connect():
    # creat a socket ready to connect
    ss = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        #print socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE)
        af, socktype, proto, canonname, sa = res
        try:
            ss = socket.socket(af, socktype, proto)
        except socket.error as msg:
            ss = None
            continue
        try:
            ss.bind(sa)
            ss.listen(4)  # define the max people to talk
        except socket.error as msg:
            ss.close()
            ss = None
            continue
        break
    if ss is None:
        print 'could not open socket'
        sys.exit(1)
    return ss


def who_in_room(online_people_dict):
    name_list = []
    for k in online_people_dict:
        name_list.append(online_people_dict[k])
    return name_list


def socket_connected(ss):
    print 'enter the socket_connected'
    conn, addr = ss.accept()
    print 'client connected'
    welcome = '''Welcome to Conan\'s chatting room.\nPlease enter your nickname: '''
    try:
        conn.send(welcome)
        nickname = conn.recv(1024)
        inputs.append(conn)
        online_people[conn] = nickname
        namelist = "Persons in the room: %s" % (who_in_room(online_people))
        conn.send(namelist)
    except Exception, e:
        print e


def server_run():
    ss = socket_ready_to_connect()
    inputs.append(ss)
    print 'Chatting Room is running'
    while True:
        r, w, e = select.select(inputs, [], [])
        for connection in r:
            if connection is ss:
                # haven't connected
                socket_connected(ss)
            else:
                # connected
                disconnection = False
                try:
                    data = connection.recv(1024)
                    data = online_people[connection] + ' say: ' + data
                except socket.error:
                    data = online_people[connection] + ' leave the room'
                    disconnection = True
                if disconnection is True:
                    inputs.remove(connection)
                    print data
                    # send to other people the leaving message
                    for other in inputs:
                        if other != ss and other != connection:
                            try:
                                other.send(data)
                            except Exception, e:
                                print e
                    del online_people[connection]
                else:
                    print data
                    # send to other people the person saying
                    for other in inputs:
                        if other != ss and other != connection:
                            try:
                                other.send(data)
                            except Exception, e:
                                print e


if __name__ == '__main__':
    server_run()



