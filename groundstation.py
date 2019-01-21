import socket
import time


def t_connect(hostIp, port):
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostIp, port))
    return


def t_server_wait(numofclientwait, port):
    global s2
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.bind(('', port))
    s2.listen(numofclientwait)


def t_server_next():
    global s
    s = s2.accept()[0]


def t_write(D):
    s.send(D + '\r')
    return


def t_read():
    a=""
    while a == "":
        a = s.recv(1)
    return a


def t_close():
    s.close()
    return


t_server_wait(5, 17098)
t_server_next()
print(t_read())
while True:
    command = input("Command: ")
    t_write(command)
