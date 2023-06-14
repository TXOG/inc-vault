import hashlib
from pyargon2 import hash
import os
import base64


def hashfile(to_hash):
    argonhash = str(hash(to_hash, '23456345678346784567', hash_len=32))
    argonhash = argonhash.encode('utf-8')
    return argonhash[:32]



def sha1_hash(to_hash):
    return hashlib.sha1(to_hash).hexdigest()
