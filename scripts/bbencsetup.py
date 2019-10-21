# bbencsetup.py
# Encryption setup
# Create public & private key
# (private key should be removed from the device...)
# 2019/10/20

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

#   # create private key, at the end remove from device
#   private_key = rsa.generate_private_key(
#       public_exponent=65537,
#       key_size=2048,
#       backend=default_backend()
#   )
#   
#   public_key = private_key.public_key()
#   
#   pem = private_key.private_bytes(
#       encoding=serialization.Encoding.PEM,
#       format=serialization.PrivateFormat.PKCS8,
#       encryption_algorithm=serialization.NoEncryption()
#   )
#   
#   with open('private_key.pem', 'wb') as f:
#       f.write(pem)
#   
#   # create public key
#   pem = public_key.public_bytes(
#       encoding=serialization.Encoding.PEM,
#       format=serialization.PublicFormat.SubjectPublicKeyInfo
#   )
#   
#   with open('public_key.pem', 'wb') as f:
#       f.write(pem)
#   

# Sample code to load public & private keys:
with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

with open("public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )

# Sample code to encrypt string
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

message = b'encrypt me!'
encrypted = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print('Original Message: '+message)
print('Encrypted:')
print(encrypted)
with open('secret.msg', 'wb') as f:
    f.write(encrypted)

# Sample code to decrypt string
original_message = private_key.decrypt(
    encrypted,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print('Decrypted Message: '+original_message)



