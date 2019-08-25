import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import ast

def encode(packet):
    with open("public.pem", "rb") as publickey:
        key = RSA.import_key(publickey.read())
    cipher = PKCS1_OAEP.new(key)
    return cipher.encrypt(str.encode(packet))

def decode(message):
    with open("private.pem", "rb") as privatekey:
        key = RSA.import_key(privatekey.read())
    cipher = PKCS1_OAEP.new(key)
    return cipher.decrypt(ast.literal_eval(str(message))).decode("utf-8")
