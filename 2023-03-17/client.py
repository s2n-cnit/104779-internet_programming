import socket
import sys


def main():  # sourcery skip: extract-duplicate-method
    try: 
        # create a TCP socket (SOCK_STREAM)
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)
    except socket.error as err:
        print("Error during creation of the socket")
        print(f"Reason: {err}")
        sys.exit()

    print('Socket created')
    
    target_host = "localhost" # "127.0.0.1" is the same
    target_port = 32000 # Standard port for Web Server
    addr = (target_host, target_port)
    try:
        s.connect(addr)
        print(f"Socket is connected to {target_host}:{target_port}")
    except ConnectionRefusedError as err:
        print(f"Connection refused from {target_host}:{target_port}")
        print(f"Details: {err}")
        sys.exit()
    except TimeoutError as terr:
        print(f"Timeout error during connection to {target_host}:{target_port}")
        print(f"Details: {terr}")
        sys.exit()

    # req = 'GET / HTTP/1.0\r\n\r\n'
    # s.send(req.encode())
    # d = s.recv(1000000)
    # print(f"Data received {d}")

    # out = open("response.html", "w")
    # out.write(d.decode())
    
    #s.shutdown(2)

main()
