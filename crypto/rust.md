# Post-Quantum Digital Signatures in Rust: A Student Guide

## Introduction

This guide demonstrates post-quantum digital signatures using the SPHINCS+ algorithm in Rust. SPHINCS+ is a hash-based signature scheme that is currently seen to be secure against both classical and quantum computers.

## Prerequisites and Installation

### Installing Rust

First, install Rust using rustup, the official Rust toolchain installer:

**On Linux: (your workspace)**
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env
```


Verify your installation:
```bash
rustc --version
cargo --version
```

### Project Setup

Create a new Rust project:
```bash
cargo new sphincs_demo
cd sphincs_demo
```

## Dependencies

Edit your `Cargo.toml` file to include the necessary dependencies:

```toml
[package]
name = "sphincs_demo"
version = "0.1.0"
edition = "2024"

[dependencies]
pqcrypto-sphincsplus = "0.7.1"
pqcrypto-traits = "0.3"
sha3 = "0.10"
hex = "0.4"
```

## Implementation

Replace the contents of `src/main.rs` with the following code:

```rust
use pqcrypto_sphincsplus::sphincsshake256ssimple::*;
use pqcrypto_traits::sign::{PublicKey, SecretKey, SignedMessage};
use sha3::{Digest, Sha3_256};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("=== SPHINCS+ Digital Signature Demo ===\n");
    
    // Alice generates a (public, private) key pair
    let (public_key, secret_key) = keypair();
    
    // Display key information (first 32 bytes for brevity)
    println!("Public Key (first 32 bytes): {:?}", &public_key.as_bytes()[..32]);
    println!("Secret Key (first 32 bytes): {:?}", &secret_key.as_bytes()[..32]);
    println!();
    
    // Alice signs her message using her private key
    let message1 = b"Hello world";
    let signature1 = sign(message1, &secret_key);
    let signature2 = sign(message1, &secret_key);
    
    // Compute and display signature hashes to demonstrate non-deterministic behavior
    let mut hasher1 = Sha3_256::new();
    hasher1.update(signature1.as_bytes());
    let hash1 = hasher1.finalize();
    
    let mut hasher2 = Sha3_256::new();
    hasher2.update(signature2.as_bytes());
    let hash2 = hasher2.finalize();
    
    println!("Signature 1 hash: {}", hex::encode(hash1));
    println!("Signature 2 hash: {}", hex::encode(hash2));
    println!("Signatures are different (non-deterministic): {}\n", hash1 != hash2);
    
    // Alice signs a different message
    let message2 = b"Hello squirrel";
    let signature3 = sign(message2, &secret_key);
    println!("Signature 3 created for different message\n");
    
    // Bob uses Alice's public key to validate her signature
    match open(&signature1, &public_key) {
        Ok(verified_msg) if verified_msg == message1 => {
            println!("✓ Signature 1 verified successfully!");
        },
        Ok(_) => println!("✗ Signature 1 verification failed: message mismatch"),
        Err(e) => println!("✗ Signature 1 verification failed: {:?}", e),
    }
    
    // Bob attempts to verify signature3 against the original message (should fail)
    match open(&signature3, &public_key) {
        Ok(verified_msg) if verified_msg == message1 => {
            println!("✗ Unexpected: Signature 3 should not verify for original message");
        },
        Ok(_) => println!("✓ Signature 3 verification failed as expected (wrong message)"),
        Err(_) => println!("✓ Signature 3 verification failed as expected (invalid signature)"),
    }
    
    // Bob verifies signature3 against the correct message (should succeed)
    match open(&signature3, &public_key) {
        Ok(verified_msg) if verified_msg == message2 => {
            println!("✓ Signature 3 verified successfully for correct message!");
        },
        Ok(_) => println!("✗ Signature 3 verification failed: message mismatch"),
        Err(e) => println!("✗ Signature 3 verification failed: {:?}", e),
    }
    
    Ok(())
}
```

## Running the Code

Execute your program:
```bash
cargo run
```

Expected output will show key generation, signature creation, hash comparison, and verification results.

## Key Concepts Explained

### SPHINCS+ Properties

**Hash-Based Security**: SPHINCS+ derives its security from the cryptographic properties of hash functions rather than mathematical problems like integer factorization or discrete logarithms.

**Post-Quantum Resistance**: The algorithm remains secure against attacks by quantum computers, making it suitable for long-term cryptographic applications.

**Non-Deterministic Signatures**: Unlike some signature schemes, SPHINCS+ produces different signatures for the same message and key pair, enhancing security through randomization.

### Security Considerations

**Key Management**: Store private keys securely and never expose them in production code or version control systems.

**Message Integrity**: The signature verification process ensures both authenticity (the message came from the holder of the private key) and integrity (the message hasn't been tampered with).

**Algorithm Parameters**: The `shake256ssimple` variant provides a balance between signature size, signing speed, and security level.

## Best Practices

1. **Error Handling**: Always handle cryptographic operations with proper error checking
2. **Secure Random Generation**: The library handles secure randomness internally
3. **Key Lifecycle**: Generate fresh key pairs for each application or user
4. **Constant-Time Operations**: The underlying library implements constant-time operations to prevent timing attacks

## Further Exploration

How does this compare with the classical algorithms, or those used in python?

