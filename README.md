# P2P Relay Server

This repository provides a Python-based peer-to-peer relay server that supports distributed messaging, message deduplication, client broadcasting, and relay-to-relay synchronization.

## 🚀 Features

- TCP-based message relay for P2P clients
- Unique message ID assignment (SHA-256)
- Broadcast to all clients and other relays
- Relay federation using JSON config (`relays.json`)
- Per-IP rate limiting (10 messages per 10 seconds)
- Message persistence (in-memory + optional `relay_log.jsonl`)
- Client acknowledgment with `msg_id`
- Clean modular structure and fully cross-platform

## 📁 Files

- `relay_server.py`: Main server script
- `relays.json`: Config file listing known peer relays
- `relay_log.jsonl`: Log file of all accepted messages (appended only)

## 🧪 Requirements

- Python 3.12+
- One external dependency:
  ```bash
  pip install requests
  pip install cryptography
  ```

## Setup
- python3 -m venv venv
- source venv/bin/activate


## ⚙️ Configuration

### `relays.json`
List all relays in the network:

```json
[
  { "id": "relay1", "ip": "100.0.1.10", "port": XXXX },
  { "id": "relay2", "ip": "100.0.1.10", "port": XXXX },
  { "id": "relay3", "ip": "100.0.1.10", "port": XXXX }
]
```

Ensure that each relay sets its own ID via `RELAY_ID` inside `relay_server.py`.

## ▶️ Running

```bash
python relay_server.py
```

Logs will show the server's public IP and relay port.

## 📤 Message Protocol

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

1. When a client sends a message:
   - It is assigned a `msg_id`.
   - It is stored locally.
   - It is broadcast to other clients and relays.

2. When a relay receives a message:
   - If `msg_id` is known: skip.
   - Else: broadcast to peers + clients, store locally.

## 🔐 Security Notes

- IP addresses are tracked for rate limiting.
- No authentication yet — suitable for trusted/federated deployments only.
- Future enhancements: TLS, signed messages, access control.

## 📦 TODO

- [ ] TLS support
- [ ] Message expiration and pruning
- [ ] REST or gRPC monitoring interface
- [ ] Admin commands

## TODO

- Client functionality


