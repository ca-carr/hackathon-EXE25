# Set-up 

In terminal ensure we are in directory `hackathon-EXE25`, then run these commands in order.

```bash 
source venv/bin/activate
cd crypto
python3 pq.py 
```
---

# Post-Quantum Cryptography: Understanding the Code

## What is Post-Quantum Cryptography?

Post-quantum cryptography refers to cryptographic algorithms that are believed to be secure against attacks by quantum computers. Traditional cryptographic methods like RSA and ECDSA could be broken by sufficiently powerful quantum computers using algorithms like Shor's algorithm.

## Understanding the `pq.py` Code

Let's break down the post-quantum cryptography example step by step:

### 1. Imports and Setup

```python
from secrets import compare_digest
from hashlib import sha3_256
import time

from pqcrypto.sign.sphincs_shake_256s_simple import generate_keypair, sign, verify
```

- **`secrets.compare_digest`**: Provides timing-attack resistant string comparison
- **`hashlib.sha3_256`**: SHA-3 hashing algorithm for creating message digests
- **`time`**: For measuring performance (we'll use this more later)
- **`pqcrypto.sign.sphincs_shake_256s_simple`**: SPHINCS+ signature scheme, a post-quantum digital signature algorithm

### 2. Key Generation

```python
# Alice generates a (public, private) key pair
public_key, private_key = generate_keypair()
print("Public Key:", public_key)
print("Private Key:", private_key)
```

**What's happening:**
- Alice creates a cryptographic key pair
- The **public key** can be shared with anyone and is used to verify signatures
- The **private key** must be kept confidential and is used to create signatures
- In SPHINCS+, these keys are much larger than classical schemes

### 3. Digital Signatures

```python
# Alice signs her message using her private key
signature = sign(private_key, b"Hello world")
signature2 = sign(private_key, b"Hello world")
```

**Key insight:** Notice that signing the same message twice produces different signatures! This is a feature called **randomised signatures**.

### 4. Signature Verification

```python
# We check the signature digests
print("Signature:", sha3_256(signature).hexdigest())
print("Signature2:", sha3_256(signature2).hexdigest())
```

Even though both signatures are for the same message, their hash digests are different, demonstrating the randomised nature.

### 5. Verification Process

```python
# Bob uses Alice's public key to validate her signature
assert verify(public_key, b"Hello world", signature)
print("Signature verified successfully!")

# Bob uses Alice's public key to check the validity of a different signature, which should fail
assert not verify(public_key, b"Hello world", signature3)
print("Signature verification failed as expected!")
```

**What's happening:**
- Bob can verify Alice's signature using her public key
- The verification confirms the message came from Alice and hasn't been tampered with
- Trying to verify a signature for a different message fails, as expected

### Post-Quantum SPHINCS+ Implementation

We can add this code to measure SPHINCS+ performance:

```python
def time_postquantum_crypto():
    """Measure SPHINCS+ key generation, signing, and verification times"""
    
    # === KEY GENERATION ===
    start_time = time.time()
    public_key, private_key = generate_keypair()
    keygen_time = time.time() - start_time
    
    # === SIGNING ===
    message = b"Hello world"
    start_time = time.time()
    signature = sign(private_key, message)
    signing_time = time.time() - start_time
    
    # === VERIFICATION ===
    start_time = time.time()
    verification_success = verify(public_key, message, signature)
    verification_time = time.time() - start_time
    
    return {
        'keygen_time': keygen_time,
        'signing_time': signing_time,
        'verification_time': verification_time,
        'verification_success': verification_success
    }
```

### Performance Comparison

Work on your own:
- Find and implement a classical signature scheme in python. 
- Perform the timing mechanism as above, and compare the times of classical to pq systems



## Questions to Consider

1. **Performance Trade-offs**: What do you notice about the speed differences between classical and post-quantum signatures?

2. **Size Trade-offs**: How do the key sizes and signature sizes compare?

3. **Security**: Why might we accept slower performance for post-quantum security?

4. **Blockchain Implications**: How might these performance differences affect blockchain transaction throughput?


This exercise will help you understand the practical implications of post-quantum cryptography in terms of both security and performance.