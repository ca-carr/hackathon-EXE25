# P2P Relay Server

This repository provides a Python-based peer-to-peer relay server that supports distributed messaging, message deduplication, client broadcasting, and relay-to-relay synchronization.

## Features

- TCP-based message relay for P2P clients
- Unique message ID assignment (SHA-256)
- Broadcast to all clients and other relays
- Relay federation using JSON config (`relays.json`)
- Per-IP rate limiting (10 messages per 10 seconds)
- Message persistence (in-memory + optional `relay_log.jsonl`)
- Client acknowledgment with `msg_id`
- Clean modular structure and fully cross-platform

## Files

- `main.py`: Main server script
- `relays.json`: Config file listing known peer relays
- `relay_log.jsonl`: Log file of all accepted messages (appended only)

## Requirements

- Python 3.12+
- One external dependency:
  ```bash
  pip install requests
  pip install cryptography
  ```

## Setup
```
- python3 -m venv venv
- source venv/bin/activate
```

## Configuration

### Change `relays.json.example` to `relays.json`

then list all relays in the network:

```json
[
  { "id": "relay1", "ip": "100.0.1.10", "port": XXXX },
  { "id": "relay2", "ip": "100.0.1.10", "port": XXXX },
  { "id": "relay3", "ip": "100.0.1.10", "port": XXXX }
]
```

Ensure that each relay sets its own ID via `RELAY_ID` inside `relay_server.py`.

## ▶Running

```bash
python3 main.py
```

Logs will show the server's public IP and relay port.

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

## 📡 Behavior

Starts a

## 🔐 Security Notes

- IP addresses are tracked for rate limiting.
- No authentication, you can add this in.
- Future enhancements: TLS, signed messages, access control.

## 📦 TODO

- [ ] TLS support
- [ ] Message expiration and pruning
- [ ] REST or gRPC monitoring interface
- [ ] Admin commands

## TODO

- Client functionality


# IDEA

Configure a consensus layer and use PQ crypto to sign and verify messages.