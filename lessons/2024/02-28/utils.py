import sys

from data import server_host, server_port


def manage_exception(msg, err):
    print(f"[ERROR] {msg} ({server_host}:{server_port})")
    print(f"Reason: {err}")
    sys.exit()
