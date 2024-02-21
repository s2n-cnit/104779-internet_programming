import socket
import sys

import yaml


def main(config_file="config.yaml"):
    try:
        # create a TCP socket (SOCK_STREAM)
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)
    except socket.error as err:
        print("Error during creation of the socket")
        print(f"Reason: {err}")
        sys.exit()

    print("Socket created")

    config = yaml.safe_load(open(config_file, "r"))
    addr = (config["server"]["host"], config["server"]["port"])
    name = config["name"]

    print(addr, name)

    try:
        s.connect(addr)
    except ConnectionRefusedError:
        manage_exception("Connection refused from the server", addr)
    except TimeoutError:
        manage_exception("Timeout error during connection to the server", addr)

    s.send(name.encode())
    msg = "x"
    while msg != "end":
        msg = input("Message: ")
        s.send(msg.encode())

    print("Connection closed")
    s.close()


def manage_exception(msg, target):
    print(f"{msg}:{target}")
    sys.exit()
