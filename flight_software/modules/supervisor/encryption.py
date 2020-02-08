from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

key = b'getmeoutgetmeout'
BLOCK_SIZE = 32

""" 
Encrypts the string version of Packet 
"""
def encrypt(packet):
    return packet.to_string().encode()
#    cipher = AES.new(key, AES.MODE_ECB)
#    return cipher.encrypt(pad(packet.encode(), BLOCK_SIZE))

"""
Decrypts the string version of Packet 
"""
def decrypt(encoded_packet):
    return Packet.from_string(encoded_packet.decode())
#    cipher = AES.new(key, AES.MODE_ECB)
#    return unpad(cipher.decrypt(message), BLOCK_SIZE).decode()