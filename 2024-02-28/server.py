import socket
import sys
from threading import Thread


def main():
    """
    Create a TCP socket, bind it to a target host and port, listen for
    incoming connections,
    and manage client connections in separate threads.

    Args:
        None

    Returns:
        None

    Examples:
        >>> main()
        Alice joins the chat
        Bob joins the chat
        ...
    """
    try:
        # create a TCP socket (SOCK_STREAM)
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)
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
        print(f"{c_name} joins the chat")
        t = Thread(
            target=client_management,
            kwargs={"name": c_name, "sock": c_sock, "addr": c_addr},
        )
        t.start()

    s.close()


def client_management(name, sock, addr):
    """
    Manage the communication with a client by receiving messages
    from the client,
    printing them along with the client's name, and closing the socket
    when the client leaves.

    Args:
        name (str): The name of the client.
        sock (socket.socket): The socket object representing the client
        connection.
        addr (tuple): The address of the client.

    Returns:
        None

    Examples:
        >>> client_management("Alice", sock, addr)
        Alice > Hello
        Alice > How are you?
        ...
        Alice leaves the chat
    """
    msg = "x"
    while msg != "end":
        msg = sock.recv(200).decode()
        if msg != "end":
            print(f"{name} >", msg)
    print(f"{name} leaves the chat")
    sock.close()


main()
