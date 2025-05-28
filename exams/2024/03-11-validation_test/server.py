import datetime
import socket

HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

commands = {
    "help": "Shows this help message.",
    "time": "Returns the current time.",
    "date": "Returns the current date (YYYY-MM-DD).",
    "month": "Returns the current month (as a number).",
    "day": "Returns the current day of the month (as a number).",
    "year": "Returns the current year.",
    "hour": "Returns the current hour (24-hour format).",
    "minutes": "Returns the current minutes.",
    "seconds": "Returns the current seconds.",
}


def get_current_time():
    now = datetime.datetime.now()
    return now.strftime("%H:%M:%S")


def get_current_date():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")


def get_current_month():
    now = datetime.datetime.now()
    return now.month


def get_current_day():
    now = datetime.datetime.now()
    return now.day


def get_current_year():
    now = datetime.datetime.now()
    return now.year


def get_current_hour():
    now = datetime.datetime.now()
    return now.hour


def get_current_minutes():
    now = datetime.datetime.now()
    return now.minute


def get_current_seconds():
    now = datetime.datetime.now()
    return now.second


def handle_client(conn, addr):
    print(f"Connected by {addr}")
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        command = data.strip().lower()
        if command == "help":
            response = "\n".join(f"{cmd}: {desc}" for cmd, desc in commands.items())
        elif command in commands:
            func = globals()[f"get_current_{command}"]
            response = str(func())
        else:
            response = f"Invalid command: '{command}'"
        conn.sendall(response.encode())
    conn.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on port {PORT}")
    while True:
        conn, addr = s.accept()
        handle_client(conn, addr)
