from cryptography.hazmat.primitives 
# template for classical crypto


#example

# from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey     #what is Ed25519?
# private_key = Ed25519PrivateKey.generate()
# signature = private_key.sign(b"my authenticated message")
# public_key = private_key.public_key()
# # Raises InvalidSignature if verification fails
# public_key.verify(signature, b"my authenticated message")

#print(signature)

# signature2 = private_key.sign(b"my authenticated message")

# print(signature2) #compare signatures, what do you see?
# what is the difference between the two signatures?
