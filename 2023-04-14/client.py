import logging
import socket
import sys
from threading import Thread

import yaml


def main():
    try:
        # create a TCP socket (SOCK_STREAM)
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)
        logging.info("Socket created")
    except socket.error as err:
        logging.error("Error during creation of the socket")
        logging.info(f"Reason: {err}")
        sys.exit()

    logging.info("Socket created")

    config = yaml.safe_load(open("config.yaml", "r"))
    addr = (config["server"]["host"], config["server"]["port"])
    name = config["name"]

    try:
        s.connect(addr)
    except ConnectionRefusedError:
        manage_exception("Connection refused from the server")
    except TimeoutError:
        manage_exception("Timeout error during connection to the server")

    s.send(name.encode())
    msg = "x"

    t = Thread(target=print_msgs, kwargs={"s": s})
    t.start()

    while msg.lower() != "end":
        msg = input(f"{name} < ")
        s.send(msg.encode())

    print("Connection closed")
    s.close()


def manage_exception(arg0, target_host, target_port, arg3):
    logging.warning(f"{arg0}{target_host}:{target_port}")
    logging.warning(f"Details: {arg3}")
    sys.exit()


def print_msgs(s):
    while True:
        try:
            msg = s.recv(200).decode()
            print(msg)
        except OSError:
            return


main()
