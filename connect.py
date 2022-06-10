from re import S
import socket
import select
import errno
import os

remote_addr = '85.25.41.144'
base_port = 1024
nports = 500
nchildren = 120

def connect_socket(port):
    return s

def main(base_port, nports):
    listen_port_range = range(base_port, base_port + nports)
    connect_sockets = []

    print(f"# connecting {nports} ports starting from {base_port}")
    for port in listen_port_range:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setblocking(0)
        try:
            s.connect((remote_addr, port))
        except OSError as err:
            if err.errno == errno.EINPROGRESS:
                connect_sockets.append(s)
            else:   
                print(f"# ERRNO {err.errno} port {port}")
                raise err
    #print(connect_sockets)
    print(f"# connecting {len(connect_sockets)} sockets")
    exception_sockets = connect_sockets.copy()
    while True:
        _, writable, exceptional = select.select([], connect_sockets, exception_sockets)
        for s in writable:
            if s in connect_sockets:
                print(f"# connected socket {s.fileno()}")
                connect_sockets.remove(s)
            if s in exceptional:
                print(f"# socket {s.fileno()} closed")
                s.close()
                exception_sockets.remove(s)

if __name__ == "__main__":
    for i in range(0, nchildren):
        newpid = os.fork()
        if newpid == 0:
            main(base_port + nports * i, nports)

    os.wait() # wrong, but who cares
