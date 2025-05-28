import logging
import socket
import sys
from threading import Thread

logging.basicConfig(encoding="utf-8", level=logging.DEBUG)
log = logging


def main():
    try:
        # create a TCP socket (SOCK_STREAM)
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)
        log.info("Socket created")
    except socket.error as err:
        log.error("Error during creation of the socket")
        log.info(f"Reason: {err}")
        sys.exit()

    target_host = "0.0.0.0"
    target_port = 32000
    addr = (target_host, target_port)
    s.bind(addr)
    s.listen(5)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    c_sockets = []
    while True:
        log.info("Waiting for incoming connection...")
        c_sock, _ = s.accept()
        c_sockets.append(c_sock)
        c_name = c_sock.recv(200).decode()
        log.info(f"{c_name} joined the chat")
        t = Thread(
            target=client_management,
            kwargs={"name": c_name, "sock": c_sock, "sockets": c_sockets},
        )
        t.start()
    s.close()


def client_management(name, sock, sockets):
    msg = "x"
    while msg.lower() != "end":
        msg = sock.recv(200).decode()
        log.info(f"{name} > {msg}")
        if msg.lower() != "end":
            for c_socket in sockets:
                if c_socket != sock:
                    try:
                        c_socket.send(f"{name} > {msg}".encode())
                    except OSError:
                        pass
    sockets.remove(sock)
    msg = f"{name} leaves the chat"
    log.warning(msg)
    for c_socket in sockets:
        c_socket.send(msg.encode())
    sock.close()


main()
