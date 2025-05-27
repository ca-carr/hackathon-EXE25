# P2P Relay Server

This repository provides a Python-based peer-to-peer relay server that supports distributed messaging, message deduplication, client broadcasting, and relay-to-relay synchronization. It is intended as a teaching tool for understanding peer-to-peer (P2P) networking and message propagation in distributed systems.

## How the Relay Works, An Overview

When the relay server starts, it does the following:

1. **Reads Configuration**:

   * Loads peer relay addresses from `relays.json`
   * Assigns a unique `RELAY_ID` and port

2. **Initializes Networking**:

   * Opens a TCP socket and listens for incoming connections on the specified port

3. **Registers Clients**:

   * Each client must first send its `peer_id` on connection
   * The relay tracks which IP is associated with which client

4. **Handles Incoming Messages**:

   * Messages are either:

     * **Client messages**: in the format `target_id||{"text": "..."}`
     * **Relay messages**: prefixed with `RELAY||` and sent between relays

5. **Validates and Logs Messages**:

   * Assigns a SHA-256 hash `msg_id` to each message
   * Prevents duplicates using a memory set (`stored_message_ids`)
   * Optionally logs messages to `relay_log.jsonl`

6. **Broadcasts and Forwards**:

   * Forwards validated messages to:

     * All known peers (clients)
     * All configured relay servers in the network

7. **Rate Limiting**:

   * Limits each IP to 10 messages every 10 seconds
   * Sends a warning if the limit is exceeded

This process simulates the decentralized propagation of data between nodes, similar to how transactions and blocks are spread in real-world blockchain networks.

## Features

* TCP-based message relay for P2P clients
* Unique message ID assignment (SHA-256)
* Broadcast to all clients and other relays
* Relay federation using JSON config (`relays.json`)
* Per-IP rate limiting (10 messages per 10 seconds)
* Message persistence (in-memory + optional `relay_log.jsonl`)
* Client acknowledgment with `msg_id`
* Modular and cross-platform compatible

## Files

* `main.py`: Main server script (configurable with `PORT` and `RELAY_ID`)
* `relays.json`: Config file listing known peer relays
* `relay_log.jsonl`: Optional append-only log of accepted messages

## Requirements

* Python 3.8+
* External dependencies:

  ```bash
  pip install requests
  ```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests
```

## Configuration

1. Rename `relays.json.example` to `relays.json`
2. Populate with your relay mesh:

```json
[
  { "id": "relay1", "ip": "100.0.1.10", "port": 55665 },
  { "id": "relay2", "ip": "100.0.1.11", "port": 55666 },
  { "id": "relay3", "ip": "100.0.1.12", "port": 55667 }
]
```

Each relay must:

* Have a unique `RELAY_ID` in `main.py`
* Be excluded from its own peer list in `relays.json`

## Running

```bash
python main.py
```

On startup, the server will:

* Show its public IP
* Listen on the configured port
* Begin accepting client and relay messages

## Message Protocol

### From Client

```
target_id||{"text": "hello"}
```

### From Relay

```
RELAY||{full_message_json_with_id}
```

### Server Response

```json
{"status": "ok", "msg_id": "<sha256-id>"}
```

## Behavior

* Accepts incoming client connections and registers `peer_id`
* Stores and hashes each message for deduplication
* Broadcasts to other connected clients and relays
* Logs messages if `LOG_TO_DISK` is enabled

## Security Notes

* Rate limiting enforced per IP (is this acceptable?)
* No authentication by default

## Further Configuration Ideas

* Change the rate limiting policy (e.g., 5 messages every 30 seconds)
* Add peer banning for abuse or malformed messages
* Add a transaction protocol
* Enable TLS encryption using Python’s `ssl` module
* Add authenticated relay peering using shared keys or signatures
* Extend the protocol to support structured message types: `transaction`, `block`, `vote`, etc.
* Implement a replay protection cache (e.g., time-expiring message cache)
* Add optional WebSocket or REST interface for monitoring and interaction

---
# Next Steps

* Add a client implementation
* Design a consensus layer on top of this relay network
* Integrate post-quantum cryptographic signatures
