from Crypto.PublicKey import RSA

key = RSA.generate(4096)
private_key = key.export_key()
file_out = open("private.pem", "wb")
file_out.write(private_key)

public_key = key.publickey().export_key()
file_out = open("public.pem", "wb")
file_out.write(public_key)
