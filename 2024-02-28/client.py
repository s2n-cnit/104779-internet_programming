import json
import socket
from threading import Lock, Thread

from data import server_addr
from utils import manage_exception

lock = Lock()


def main():
    try:
        # create a TCP socket (SOCK_STREAM)
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)
        s.connect(server_addr)
        name = input("Name: ")
        s.send(name.encode())
        Thread(
            target=recv_manager,
            kwargs={"sock": s},
        ).start()
        msg = "x"
        while msg != "end":
            lock.acquire()
            msg = input("Message: ")
            lock.release()
            s.send(msg.encode())
        print("Connection closed")
        s.close()
    except ConnectionRefusedError as err:
        manage_exception("connection refused from the server", err)
    except TimeoutError as err:
        manage_exception("timeout expiration during connection to the server", err)
    except socket.error as err:
        manage_exception("socket creation", err)


def recv_manager(sock):
    while True:
        d = json.loads(sock.recv(10000).decode())
        lock.acquire()
        print(f"{d['name']} >", d["msg"])
        lock.release()


main()
