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

## Performance Comparison: Classical vs Post-Quantum

Now let's measure and compare the performance of classical cryptography versus post-quantum cryptography.

### Setup for Performance Testing

First, add these imports to your code:

```python
import time
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
```

### Classical RSA Implementation

Add this code to compare with RSA:

```python
def time_classical_crypto():
    """Measure RSA key generation, signing, and verification times"""
    
    # === KEY GENERATION ===
    start_time = time.time()
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    keygen_time = time.time() - start_time
    
    # === SIGNING ===
    message = b"Hello world"
    start_time = time.time()
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    signing_time = time.time() - start_time
    
    # === VERIFICATION ===
    start_time = time.time()
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        verification_success = True
    except:
        verification_success = False
    verification_time = time.time() - start_time
    
    return {
        'keygen_time': keygen_time,
        'signing_time': signing_time,
        'verification_time': verification_time,
        'verification_success': verification_success
    }
```

### Post-Quantum SPHINCS+ Implementation

Add this code to measure SPHINCS+ performance:

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

Add this code to run the comparison:

```python
def compare_performance():
    """Compare classical RSA vs post-quantum SPHINCS+ performance"""
    
    print("🔐 Cryptographic Performance Comparison")
    print("=" * 50)
    
    # Test classical cryptography
    print("Testing Classical RSA (2048-bit)...")
    classical_results = time_classical_crypto()
    
    # Test post-quantum cryptography
    print("Testing Post-Quantum SPHINCS+...")
    pq_results = time_postquantum_crypto()
    
    # Display results
    print("\n📊 RESULTS:")
    print("-" * 30)
    print(f"{'Operation':<15} {'RSA (ms)':<12} {'SPHINCS+ (ms)':<15} {'Ratio':<10}")
    print("-" * 60)
    
    operations = ['keygen_time', 'signing_time', 'verification_time']
    operation_names = ['Key Generation', 'Signing', 'Verification']
    
    for op, name in zip(operations, operation_names):
        rsa_ms = classical_results[op] * 1000
        sphincs_ms = pq_results[op] * 1000
        ratio = sphincs_ms / rsa_ms if rsa_ms > 0 else float('inf')
        
        print(f"{name:<15} {rsa_ms:<12.2f} {sphincs_ms:<15.2f} {ratio:<10.1f}x")
    
    print("-" * 60)
    print(f"RSA Verification: {'✓' if classical_results['verification_success'] else '✗'}")
    print(f"SPHINCS+ Verification: {'✓' if pq_results['verification_success'] else '✗'}")

# Run the comparison
if __name__ == "__main__":
    compare_performance()
```

## Key Size Comparison

Add this code to compare key and signature sizes:

```python
def compare_sizes():
    """Compare key and signature sizes between RSA and SPHINCS+"""
    
    print("\n📏 SIZE COMPARISON:")
    print("-" * 40)
    
    # RSA sizes
    rsa_private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    rsa_public = rsa_private.public_key()
    rsa_signature = rsa_private.sign(b"test", padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
    
    # SPHINCS+ sizes
    sphincs_public, sphincs_private = generate_keypair()
    sphincs_signature = sign(sphincs_private, b"test")
    
    print(f"{'Component':<20} {'RSA (bytes)':<15} {'SPHINCS+ (bytes)':<18}")
    print("-" * 55)
    print(f"{'Public Key':<20} {len(rsa_public.public_bytes(Encoding.DER, rsa.PublicFormat.SubjectPublicKeyInfo)):<15} {len(sphincs_public):<18}")
    print(f"{'Private Key':<20} {len(rsa_private.private_bytes(Encoding.DER, PrivateFormat.PKCS8, NoEncryption())):<15} {len(sphincs_private):<18}")
    print(f"{'Signature':<20} {len(rsa_signature):<15} {len(sphincs_signature):<18}")

# Add this to your main function
compare_sizes()
```

## Questions to Consider

1. **Performance Trade-offs**: What do you notice about the speed differences between classical and post-quantum signatures?

2. **Size Trade-offs**: How do the key sizes and signature sizes compare?

3. **Security**: Why might we accept slower performance for post-quantum security?

4. **Blockchain Implications**: How might these performance differences affect blockchain transaction throughput?

## Complete Example

Here's how your complete `pq_performance.py` file should look:

```python
# Add all the imports and functions above, then:

def main():
    print("🚀 Post-Quantum Cryptography Demo")
    print("=" * 40)
    
    # Original SPHINCS+ demo
    public_key, secret_key = generate_keypair()
    signature = sign(secret_key, b"Hello world")
    print(f"✓ SPHINCS+ signature verification: {verify(public_key, b'Hello world', signature)}")
    
    # Performance comparison
    compare_performance()
    
    # Size comparison
    compare_sizes()

if __name__ == "__main__":
    main()
```

This exercise will help you understand the practical implications of post-quantum cryptography in terms of both security and performance!