# -*- coding: latin-1 -*-
#
# Copyright (C) AB Strakt
# Copyright (C) Jean-Paul Calderone
# See LICENSE for details.

"""
Simple SSL client, using blocking I/O
"""

import os
import select
import socket
import sys

from OpenSSL import SSL


def verify_cb(conn, cert, errnum, depth, ok):
    # This obviously has to be updated
    print(f"Got certificate: {cert.get_subject()}")
    return ok


if len(sys.argv) < 3:
    print("Usage: python client.py HOST PORT")
    sys.exit(1)

dir = os.path.dirname(sys.argv[0])
if dir == "":
    dir = os.curdir

# Initialize context
ctx = SSL.Context(SSL.SSLv23_METHOD)
ctx.set_verify(SSL.VERIFY_PEER, verify_cb)  # Demand a certificate
ctx.set_ciphers("ALL:@SECLEVEL=0")
ctx.use_privatekey_file(os.path.join(dir, "keys/client.pkey"))
ctx.use_certificate_file(os.path.join(dir, "keys/client.cert"))
ctx.load_verify_locations(os.path.join(dir, "keys/CA.cert"))

# Set up client
sock = SSL.Connection(ctx, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
sock.connect((sys.argv[1], int(sys.argv[2])))

while 1:
    line = sys.stdin.readline()
    if line == "":
        break
    try:
        sock.send(line)
        sys.stdout.write(sock.recv(1024))
        sys.stdout.flush()
    except SSL.Error:
        print("Connection died unexpectedly")
        break


sock.shutdown()
sock.close()
