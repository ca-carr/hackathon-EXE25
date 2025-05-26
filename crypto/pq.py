from secrets import compare_digest
from hashlib import sha3_256
import time

from pqcrypto.sign.sphincs_shake_256s_simple import generate_keypair, sign, verify

# Alice generates a (public, private) key pair
public_key, private_key = generate_keypair()
print("Public Key:", public_key)
print("Private Key:", private_key)

# Alice signs her message using her private key
signature = sign(private_key, b"Hello world")
signature2 = sign(private_key, b"Hello world")

# We check the siganture digests
print("Signature:", sha3_256(signature).hexdigest())
print("Signature2:", sha3_256(signature2).hexdigest())

# Alice signs a different message using her private key again
signature3 = sign(private_key, b"Hello squirrel")
print("Signature3:", signature3)

# Bob uses Alice's public key to validate her signature
assert verify(public_key, b"Hello world", signature)
print("Signature verified successfully!")

# Bob uses Alice's public key to check the validity of a different signature, which should fail
assert not verify(public_key, b"Hello world", signature3)
print("Signature verification failed as expected!")