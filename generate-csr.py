#!/usr/bin/env python

# This script adapted from the tutorial at
# https://cryptography.io/en/latest/x509/tutorial/
#
# Key and CSR are written out in the directory this is run in.
# Key will be encrypted with a passphrase given after executing this script.
#
# Any existing key and CSR files will be deleted and overwritten. Beware!

# Certificate issued through the Federal PKI, beginning with the
# form found here: https://pki.treas.gov/OCA/cert.form.pdf
#
# (Bear in mind, pki.treas.gov itself uses a cert issued by
# the Federal PKI, you may need to click through a warning.)

import sys
import os
import getpass

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID

# Pick one of the SANs to use as the CN.
key_name = "test1.fpki.18f.gov"
key_file = "%s.key" % key_name
csr_file = "%s.csr" % key_name

# SANS: test[1..15].fpki.18f.gov
sans = [x509.DNSName("test%i.fpki.18f.gov" % n) for n in list(range(1,16))]

# CSR values.
common_name = key_name
country_name = "US"
state_or_province_name = "District of Columbia"
locality_name = "Washington"
organization_name = "U.S. Government"
organizational_unit_name = "General Services Administration"



# Get the passphrase to encrypt the key read in over STDIN.
try:
    first_pass = getpass.getpass(prompt='Passphrase to encrypt key: ')
    second_pass = getpass.getpass(prompt='Repeat passphrase: ')

    if first_pass == second_pass:
        passphrase = first_pass.encode("utf-8")
    else:
        print("Passphrases didn't agree. Try again.")
        exit()
except KeyboardInterrupt:
    print()
    exit()

# Generate a 2048-bit RSA key.
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Delete any existing key and CSR files. Beware!
for path in [key_file, csr_file]:
    if (os.path.exists(path)):
        print("Deleting %s" % path)
        os.remove(path)

# Write our key to disk for safe keeping
with open(key_file, "wb") as f:
    print("Writing %s" % key_file)
    f.write(key.private_bytes(
       encoding=serialization.Encoding.PEM,
       format=serialization.PrivateFormat.TraditionalOpenSSL,
       encryption_algorithm=serialization.BestAvailableEncryption(passphrase),
    ))


# Generate a CSR
csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([

    # Provide various details about who we are.
    x509.NameAttribute(NameOID.COUNTRY_NAME, country_name),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state_or_province_name),
    x509.NameAttribute(NameOID.LOCALITY_NAME, locality_name),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization_name),
    x509.NameAttribute(NameOID.COMMON_NAME, common_name),

])).add_extension(
    x509.SubjectAlternativeName(sans),
    critical=False,

# Sign the CSR with our private key.
).sign(key, hashes.SHA256(), default_backend())

# Write our CSR out to disk.
with open(csr_file, "wb") as f:
    print("Writing %s" % csr_file)
    f.write(csr.public_bytes(serialization.Encoding.PEM))
