# bbenc.py
# Shaun Bowman
# 2019/10/20
#
# Encryption class for project blackbean

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
#import pickle #used to serialize encrypted message for storage in db
#import json   #used to serialize encrypted message for storage in db
#import base64 #used to serialize encrypted message for storage in db
import binascii
import hashlib

class bbenc:

    pub_key_f = 'public_key.pem'
    prv_key_f = 'private_key.pem'
    pub_key = None
    prv_key = None
    resp = None

    def load_public(self):
        # load public key from file
        with open(self.pub_key_f, "rb") as key_file:
            self.pub_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )
        self.resp = 'public key loaded'

    def load_private(self):
        # load private key from file
        with open(self.prv_key_f, "rb") as key_file:
            self.prv_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
        self.resp = 'private key loaded'

    def decrypt(self,encrypted):
        # Decrypt a message using private key
        original_message = self.prv_key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return original_message
    
    def encrypt(self, message='Blub'):
        # Encrypt a message using public key
        encrypted = self.pub_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        m = hashlib.sha256()
        m.update(message)
        encrypted = m.hexdigest()
        return encrypted

    def serialize(self, enc):
        # Serialize a binary encryption object as ascii
        #enc_bytes = pickle.dumps(enc)
        #data = {'code' : base64.b64encode(enc_bytes).decode('ascii')}
        #enc_json = json.dumps(data)
        #enc_base64 = binascii.b2a_base64(enc)
        #enc_base64 = binascii.hexlify(enc)
        return str(enc_base64)
