import os, sys
import hashlib

def getHash(data, algorithm):
    """
    Data : data to get the hash from
    Algorithm : md5, sha-256, ...
    """

    hasher = hashlib.new(name=algorithm)
    hasher.update(data)
    return hasher.hexdigest()

with open('tests\\file.pdf', 'rb') as f:
    fdata = f.read()
