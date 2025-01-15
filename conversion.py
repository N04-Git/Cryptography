# Modules
import os, sys
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
import base64


# Index is important
encryptions = ['AES', 'DES', 'BLOWFISH', 'RSA', 'ECC']

# Classes
class AESCryptor:
    def __init__(self):
        self.key = get_random_bytes(32)

    def encrypt(self, data) -> bytes:
        print('Using generated key :', self.key)
        iv = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        cipher_data = cipher.encrypt(pad(data, AES.block_size))
        return iv + cipher_data
    
    def decrypt(self, cipher_data, key:None) -> bytes:
        if key:
            self.key = key
        iv = cipher_data[:16]
        cipher_data = cipher_data[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(cipher_data), AES.block_size)


class RSACryptor:
    def __init__(self):
        self.key_size = 2048
        self.key_pair = RSA.generate(self.key_size)

    def getPublicKey(self) -> bytes:
        public_key = self.key_pair.publickey().export_key()
        return public_key

    def getPrivateKey(self) -> bytes:
        private_key = self.key_pair.export_key()
        return private_key 

    def encrypt(self, data, public_key) -> bytes:
        key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(key)
        return cipher.encrypt(data)

    def decrypt(self, data, private_key) -> bytes:
        key = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(key)
        return cipher.decrypt(data)


def makeChunks(chunk_size, bytes) -> list:
    # Split bytes into packets of 512 bytes
    steps = len(bytes) // chunk_size
    current = 0
    
    splitted = [None] * (steps + 1)
    
    c = 0
    while c <= steps:
        chunk = bytes[current:current+chunk_size]
        splitted[c] = chunk
        
        # Update counter & current
        c += 1
        current += chunk_size
    
    return splitted

def makeSerializable(toSerialize:bytes) -> str:
    b = base64.b64encode(toSerialize).decode('utf-8')
    print(f' {len(toSerialize)} >>> {len(b)}')
    return b

def unmakeSerializable(toDeserialize:str) -> bytes:
    b = base64.b64decode(toDeserialize.encode('utf-8'))
    print(f' {len(toDeserialize)} >>> {len(b)}')
    return b

def encryptFile(fdata, encryption_index) -> list:
    """
    [0] => encrypted file bytes
    [1] => (optional) key
    """
    
    print(f"""
____________________| Encrypting file |____________________  
- File size : {len(fdata)}
- Encryption Index : {encryption_index}
- Encryption Algorithm ({len(str(encryptions[encryption_index]))}) : {encryptions[encryption_index]}
""")
    
    # AES
    if encryption_index == 0:
        cryptor = AESCryptor()
        return [cryptor.encrypt(fdata), cryptor.key]
    
    # DES
    elif encryption_index == 1:
        pass
    
    # BLOWFISH
    elif encryption_index == 2:
        pass
    
    # RSA
    elif encryption_index == 3:
        pass
    
    # ECC
    elif encryption_index == 4:
        pass

    else:
        print('Index out of range : ', encryption_index, encryptions)
        exit(1)


def decryptFile(fdata, encryption_index, key=None) -> bytes:
    print(f"""
____________________| Decrypting file |____________________  
- File size : {len(fdata)}
- Encryption Index : {encryption_index}
- Encryption Algorithm ({len(str(encryptions[encryption_index]))}) : {encryptions[encryption_index]}
- Key ({len(str(key))}) : {key}
""")
    if encryption_index == 0:
        cryptor = AESCryptor()
        return cryptor.decrypt(fdata, key)
    
    elif encryption_index == 1:
        pass
    
    elif encryption_index == 2:
        pass
    
    elif encryption_index == 3:
        pass
    
    elif encryption_index == 4:
        pass
    
    return b''

