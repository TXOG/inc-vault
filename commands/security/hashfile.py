import hashlib
from pyargon2 import hash


def hashfile(to_hash, hash_salt):
    argonhash = str(hash(to_hash, str(hash_salt), hash_len=32))
    argonhash = argonhash.encode('utf-8')
    return argonhash[:32]



def sha1_hash(to_hash):
    return hashlib.sha1(to_hash).hexdigest()
