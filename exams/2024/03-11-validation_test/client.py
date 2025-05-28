import socket

HOST = "localhost"  # The server's hostname or IP address
PORT = 65432  # The port used by the server


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        command = input(
            "Enter command (help, time, date, month, day, year, hour, minutes, seconds): "
        )
        if command.lower() == "quit":
            break
        s.sendall(command.encode())
        data = s.recv(1024).decode()
        print(data)
