#!/usr/bin/env python

# This script adapted from the tutorial at
# https://cryptography.io/en/latest/x509/tutorial/

import sys
import getpass

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# The domain to name the key after.
domain = "test.fpki.18f.gov"

# SANS: test[1..15].fpki.18f.gov
sans = [("test%i.fpki.18f.gov" % n) for n in list(range(1,16))]

# Get the passphrase to encrypt the key read in over STDIN.
passphrase = getpass.getpass(prompt='Passphrase to encrypt key: ')
passphrase = bytes(passphrase, "utf-8")

# Generate a 2048-bit RSA key.
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)


# Write our key to disk for safe keeping
with open("%s.pem" % domain, "wb") as f:
    f.write(key.private_bytes(
       encoding=serialization.Encoding.PEM,
       format=serialization.PrivateFormat.TraditionalOpenSSL,
       encryption_algorithm=serialization.BestAvailableEncryption(passphrase),
    ))

