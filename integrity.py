import hashlib
import os

def getHash(data, algorithm):
    """
    Data : data to get the hash from
    Algorithm : md5, sha-256, ...
    """

    hasher = hashlib.new(name=algorithm)
    hasher.update(data)
    return hasher.hexdigest()

def getFileInfo(fpath, hashAlgorithm='sha-256'):
    """
    Returns 
    -File name
    -File path
    -File size
    -File hash
    """
    
    with open(fpath, 'rb') as f:
        data = f.read()
    
    # File name
    n = os.path.basename(fpath)
    
    # File path
    p = os.path.dirname(fpath)
    
    # File size
    s = len(data)
    
    # File hash
    h = getHash(data, algorithm=hashAlgorithm)
    
    return (n, p, s, h)