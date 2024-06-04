import json
import socket
import sys
from threading import Thread

from data import server_addr

clients = {}


def main():
    try:
        # create a TCP socket (SOCK_STREAM)
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)
        s.bind(server_addr)
        s.listen(5)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while True:
            c_sock, c_addr = s.accept()
            clients[c_addr] = c_sock

            c_name = c_sock.recv(200).decode()
            print(f"{c_name} joins the chat")
            Thread(
                target=client_manager,
                kwargs={"name": c_name, "sock": c_sock, "addr": c_addr},
            ).start()
        s.close()
    except socket.error as err:
        print("Error during creation of the socket")
        print(f"Reason: {err}")
        sys.exit()


def client_manager(name, sock, addr):
    msg = "x"
    while msg != "end":
        msg = sock.recv(200).decode()
        if msg != "end":
            print(f"{name} >", msg)
        for c_addr, c_sock in clients.items():
            if c_addr != addr:
                d = {"name": name, "msg": msg}
                c_sock.send(json.dumps(d).encode())
    print(f"{name} leaves the chat")
    sock.close()


main()
