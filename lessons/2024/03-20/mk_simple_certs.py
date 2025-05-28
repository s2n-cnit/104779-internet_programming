"""
Create certificates and private keys for the 'simple' example.
"""

from certgen import *  # yes yes, I know, I'm lazy
from OpenSSL import crypto

cakey = createKeyPair(TYPE_RSA, 2048)
careq = createCertRequest(cakey, CN="Certificate Authority")
cacert = createCertificate(
    careq, (careq, cakey), 0, (0, 60 * 60 * 24 * 365 * 5)
)  # five years
open("keys/CA.pkey", "wb").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, cakey))
open("keys/CA.cert", "wb").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cacert))
for fname, cname in [("client", "Simple Client"), ("server", "Simple Server")]:
    pkey = createKeyPair(TYPE_RSA, 2048)
    req = createCertRequest(pkey, CN=cname)
    cert = createCertificate(
        req, (cacert, cakey), 1, (0, 60 * 60 * 24 * 365 * 5)
    )  # five years
    open("keys/%s.pkey" % (fname,), "wb").write(
        crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey)
    )
    open("keys/%s.cert" % (fname,), "wb").write(
        crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
    )
