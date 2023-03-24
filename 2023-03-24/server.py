import socket
import sys
from threading import Thread


def main():
    try:
        # create a TCP socket (SOCK_STREAM)
        s = socket.socket(family=socket.AF_INET,
                          type=socket.SOCK_STREAM, proto=0)
    except socket.error as err:
        print("Error during creation of the socket")
        print(f"Reason: {err}")
        sys.exit()

    target_host = "0.0.0.0"
    target_port = 32000
    addr = (target_host, target_port)
    s.bind(addr)
    s.listen(5)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    while True:
        c_sock, c_addr = s.accept()
        c_name = c_sock.recv(200).decode()
        t = Thread(target=client_management,
                   kwargs={'name': c_name, 'sock': c_sock, 'addr': c_addr})
        t.start()

    s.close()


def client_management(name, sock, addr):
    msg = "x"
    while msg != "end":
        msg = sock.recv(200).decode()
        print(f"{name}>", msg)
    print(f"{name}> leaves the chat")
    sock.close()


main()
