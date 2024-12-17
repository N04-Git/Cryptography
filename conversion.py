# Modules
import os, sys
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA

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