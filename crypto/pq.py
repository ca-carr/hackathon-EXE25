from secrets import compare_digest
from hashlib import sha3_256

from pqcrypto.sign.sphincs_shake_256s_simple import generate_keypair, sign, verify

# Alice generates a (public, secret) key pair
public_key, secret_key = generate_keypair()
print("Public Key:", public_key)
print("Secret Key:", secret_key)

# Alice signs her message using her secret key
signature = sign(secret_key, b"Hello world")
signature2 = sign(secret_key, b"Hello world")

# We check the siganture digests
print("Signature:", sha3_256(signature).hexdigest())
print("Signature2:", sha3_256(signature2).hexdigest())

# Alice signs a different message using her secret key again
signature3 = sign(secret_key, b"Hello squirrel")
print("Signature3:", signature3)

# Bob uses Alice's public key to validate her signature
assert verify(public_key, b"Hello world", signature)
print("Signature verified successfully!")

# Bob uses Alice's public key to check the validity of a different signature, which should fail
assert not verify(public_key, b"Hello world", signature3)
print("Signature verification failed as expected!")