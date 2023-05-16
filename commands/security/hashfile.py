import hashlib
from pyargon2 import hash


def hashfile(to_hash):
    argonhash = str(hash(to_hash, "123456789123456789"))
    argonhash = argonhash.encode('utf-8')
    return hashlib.sha256(argonhash).digest()