import os
import random
import string
import subprocess

privateKeyFilename = "private.pem"
publicKeyDerFilename = "public.der"
publicKeyPemFilename = "public.pem"
dataFilename = "data.txt"
signatureFilename = "signature.bin"
opensslPath = "C:\\cygwin\\bin\\openssl.exe"

# Create private key
subprocess.run([opensslPath, "ecparam", "-genkey", "-name", "secp384r1", "-noout", "-out", privateKeyFilename])

# Create public key
subprocess.run([opensslPath, "ec", "-in", privateKeyFilename, "-pubout", "-outform", "der", "-out", publicKeyDerFilename])

# Create data
if not os.path.exists(dataFilename):
    with open(dataFilename, "w") as data:
        for i in range(256):
            data.writelines(''.join(random.choice(string.printable) for i in range(64)))

dictCount = {}
for i in range(10):
    # Sign data
    subprocess.run([opensslPath, "dgst", "-ecdsa-with-SHA1", "-sign", privateKeyFilename, "-out", signatureFilename, dataFilename])
    if os.stat(signatureFilename).st_size in dictCount.keys():
        dictCount[os.stat(signatureFilename).st_size] += 1
    else:
        dictCount[os.stat(signatureFilename).st_size] = 1
print(dictCount)

# Verify data
subprocess.run([opensslPath, "ec", "-in", privateKeyFilename, "-pubout", "-out", publicKeyPemFilename])
subprocess.run([opensslPath, "dgst", "-ecdsa-with-SHA1", "-verify", publicKeyPemFilename, "-signature", signatureFilename, dataFilename])
