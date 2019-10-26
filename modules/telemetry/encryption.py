from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

key = b'getmeoutgetmeout'
BLOCK_SIZE = 32

def encrypt(packet):
    """ Encrypts the string version of Packet """
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(packet.encode(), BLOCK_SIZE))

def decrypt(message):
    """ Decrypts the string version of Packet """
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(message), BLOCK_SIZE).decode()
