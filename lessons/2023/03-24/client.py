import socket
import sys

import yaml


def main():
    try: 
        # create a TCP socket (SOCK_STREAM)
        s = socket.socket(family=socket.AF_INET,
                          type=socket.SOCK_STREAM, proto=0)
    except socket.error as err:
        print("Error during creation of the socket")
        print(f"Reason: {err}")
        sys.exit()

    print('Socket created')

    config = yaml.safe_load(open("config.yaml", "r"))
    addr = (config['server']['host'], config['server']['port'])
    name = config['name']

    try:
        s.connect(addr)
    except ConnectionRefusedError:
        manage_exception('Connection refused from the server')
    except TimeoutError:
        manage_exception("Timeout error during connection to the server")

    s.send(name.encode())
    msg = "x"
    while msg != "end":
        msg = input("Message: ")
        s.send(msg.encode())

    print("Connection closed")
    s.close()


def manage_exception(arg0, target_host, target_port, arg3):
    print(f"{arg0}{target_host}:{target_port}")
    print(f"Details: {arg3}")
    sys.exit()


main()
