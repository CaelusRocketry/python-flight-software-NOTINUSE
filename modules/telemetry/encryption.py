from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

key = b'getmeoutgetmeout'
BLOCK_SIZE = 32

def encode(packet):
    cipher = AES.new(key, AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(pad(packet, BLOCK_SIZE)))

def decode(message):
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(base64.b64decode(message)), BLOCK_SIZE)
