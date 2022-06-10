import socket
import select
import errno
import os

base_port = 1024
nports = 500
nchildren = 120

def create_socket(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(1024)  # XXX
    return server_socket

def main(base_port, nports):
    listen_port_range = range(base_port, base_port + nports)
    listen_sockets = []

    print(f"# opening {nports} ports starting from {base_port}")
    n_inuse = 0
    for port in listen_port_range:
        try:
            s = create_socket(port)
            listen_sockets.append(s)
        except OSError as err:
            if err.errno == errno.EMFILE or err.errno == errno.ENFILE:
                print(f"# {len(listen_sockets)} listening sockets open")
                raise err
            elif err.errno == errno.EADDRINUSE:
                n_inuse += 1
            else:
                print(f"#ERRNO {err.errno}")
                raise err

    print(f"# listening on {len(listen_sockets)} sockets")
    read_sockets = listen_sockets.copy()
    while True:
        readable, _, exceptional = select.select(read_sockets, [], read_sockets)
        for s in readable:
            print(s)
            if s in listen_sockets:
                client_socket, address = s.accept()
                print(f"client {address} connected to socket {s.fileno()}")
                read_sockets.append(client_socket)
            else:
                data = s.recv(1024)
                if len(data) == 0:
                    print(f"# socket {s.fileno()} closed")
                    s.close()
                    read_sockets.remove(s)
                else:
                    print(f"# read {len(data)} octets from socket {s.fileno()}")


if __name__ == "__main__":
    for i in range(0, nchildren):
        newpid = os.fork()
        if newpid == 0:
            main(base_port + nports * i, nports)

    os.wait() # wrong, but who cares

