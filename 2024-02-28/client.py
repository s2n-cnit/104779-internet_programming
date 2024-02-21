import socket
import sys

import yaml


def main(config_file="config.yaml"):
    """
    Connects to a server using a TCP socket and sends messages to the server.

    Args:
        config_file (str, optional): The path to the configuration file.
        Defaults to "config.yaml".

    Raises:
        ConnectionRefusedError: If the connection to the server is refused.
        TimeoutError: If a timeout occurs during the connection to the server.

    Returns:
        None

    Examples:
        >>> main()
        Socket created
        ('localhost', 8080) MyName
        Message: Hello
        Message: World
        Message: end
        Connection closed
    """

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
    """
    Print an error message along with a target and exit the program.

    Args:
        msg (str): The error message.
        target (str): The target of the error.

    Returns:
        None

    Raises:
        SystemExit: Always raises SystemExit to exit the program.

    Examples:
        >>> manage_exception("Error", "file.txt")
        Error:file.txt
    """
    print(f"{msg}:{target}")
    sys.exit()
