# -*- coding: latin-1 -*-
#
# Copyright (C) AB Strakt
# Copyright (C) Jean-Paul Calderone
# See LICENSE for details.

"""
Simple echo server, using nonblocking I/O
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


if len(sys.argv) < 2:
    print("Usage: python server.py PORT")
    sys.exit(1)

dir = os.path.dirname(sys.argv[0])
if dir == "":
    dir = os.curdir

# Initialize context
ctx = SSL.Context(SSL.SSLv23_METHOD)
ctx.set_options(SSL.OP_NO_SSLv2)
ctx.set_cipher_list("ALL:@SECLEVEL=0")
ctx.set_verify(
    SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT, verify_cb
)  # Demand a certificate
ctx.use_privatekey_file(os.path.join(dir, "keys/server.pkey"))
ctx.use_certificate_file(os.path.join(dir, "keys/server.cert"))
ctx.load_verify_locations(os.path.join(dir, "keys/CA.cert"))

# Set up server
server = SSL.Connection(ctx, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
server.bind(("", int(sys.argv[1])))
server.listen(3)
server.setblocking(0)

clients = {}
writers = {}


def dropClient(cli, errors=None):
    if errors:
        print(f"Client {clients[cli]} left unexpectedly")
        print(f"  {errors}")
    else:
        print(f"Client {clients[cli]} left politely")
    del clients[cli]
    if cli in writers:
        del writers[cli]
    if not errors:
        cli.shutdown()
    cli.close()


while 1:
    try:
        r, w, _ = select.select([server] + list(clients.keys()), writers.keys(), [])
    except:
        break

    for cli in r:
        if cli == server:
            cli, addr = server.accept()
            print(f"Connection from {addr}")
            clients[cli] = addr

        else:
            try:
                ret = cli.recv(1024)
            except (SSL.WantReadError, SSL.WantWriteError, SSL.WantX509LookupError):
                pass
            except SSL.ZeroReturnError:
                dropClient(cli)
            except SSL.Error as errors:
                dropClient(cli, errors)
            else:
                if cli not in writers:
                    writers[cli] = ""
                writers[cli] = writers[cli] + ret

    for cli in w:
        try:
            ret = cli.send(writers[cli])
        except (SSL.WantReadError, SSL.WantWriteError, SSL.WantX509LookupError):
            pass
        except SSL.ZeroReturnError:
            dropClient(cli)
        except SSL.Error as errors:
            dropClient(cli, errors)
        else:
            writers[cli] = writers[cli][ret:]
            if writers[cli] == "":
                del writers[cli]

for cli in clients.keys():
    cli.close()
server.close()
