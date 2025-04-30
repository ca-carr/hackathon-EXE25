import socket
import threading
import time
import json
import hashlib
from collections import defaultdict, deque
import requests

# === Configuration ===
PORT = 55665
RELAY_ID = "relay1"  # Set uniquely per relay
RELAY_CONFIG_FILE = "relays.json"
RATE_LIMIT = 10  # messages
RATE_INTERVAL = 10  # seconds
LOG_TO_DISK = True

# === State ===
clients = {}  # peer_id -> socket
client_ips = {}  # peer_id -> IP
rate_tracker = defaultdict(lambda: deque())
stored_message_ids = set()
stored_messages = []
RELAY_PEERS = []  # populated from config

# === Helper Functions ===
def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "unknown"

def load_relay_peers():
    global RELAY_PEERS
    with open(RELAY_CONFIG_FILE, "r") as f:
        all_relays = json.load(f)
    RELAY_PEERS = [
        (entry["id"], entry["ip"], entry["port"])
        for entry in all_relays
        if entry["id"] != RELAY_ID
    ]

def is_rate_limited(ip):
    now = time.time()
    timestamps = rate_tracker[ip]
    while timestamps and now - timestamps[0] > RATE_INTERVAL:
        timestamps.popleft()
    if len(timestamps) >= RATE_LIMIT:
        return True
    timestamps.append(now)
    return False

def generate_message_id(entry):
    raw = json.dumps(entry, sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()

def store_and_id_message(entry):
    entry["msg_id"] = generate_message_id(entry)
    if entry["msg_id"] in stored_message_ids:
        return None
    stored_message_ids.add(entry["msg_id"])
    stored_messages.append(entry)
    if LOG_TO_DISK:
        with open("relay_log.jsonl", "a") as f:
            f.write(json.dumps(entry) + "\n")
    return entry["msg_id"]

def broadcast(msg, sender=None):
    for peer_id, sock in list(clients.items()):
        if peer_id != sender:
            try:
                sock.sendall(msg.encode())
            except:
                continue

def forward_to_peers(entry):
    for peer_id, host, port in RELAY_PEERS:
        try:
            with socket.create_connection((host, port), timeout=2) as sock:
                sock.sendall(f"RELAY||{json.dumps(entry)}".encode())
        except:
            print(f"[!] Relay forwarding failed to {peer_id} ({host})")

def client_handler(conn, addr):
    ip = addr[0]
    try:
        peer_id = conn.recv(1024).decode().strip()
        if not peer_id:
            conn.close()
            return
        clients[peer_id] = conn
        client_ips[peer_id] = ip
        print(f"[+] Registered peer: {peer_id} from {ip}")

        while True:
            data = conn.recv(4096)
            if not data:
                break
            if is_rate_limited(ip):
                conn.sendall(b"[!] Rate limit exceeded.\n")
                continue

            raw = data.decode()
            if raw.startswith("RELAY||"):
                relay_msg = json.loads(raw.split("RELAY||", 1)[1])
                if relay_msg["msg_id"] in stored_message_ids:
                    continue
                relay_msg["seen_by"].append(RELAY_ID)
                store_and_id_message(relay_msg)
                broadcast(json.dumps(relay_msg))
                forward_to_peers(relay_msg)
                continue

            try:
                target, msg_json = raw.split("||", 1)
                msg_obj = json.loads(msg_json)
                entry = {
                    "from": peer_id,
                    "to": target,
                    "body": msg_obj.get("text", ""),
                    "timestamp": time.time(),
                    "seen_by": [RELAY_ID]
                }
                msg_id = store_and_id_message(entry)
                if msg_id:
                    broadcast(json.dumps(entry), sender=peer_id)
                    forward_to_peers(entry)
                conn.sendall(json.dumps({"status": "ok", "msg_id": msg_id}).encode())
            except Exception as e:
                conn.sendall(f"[!] Malformed message: {e}\n".encode())
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        clients.pop(peer_id, None)
        client_ips.pop(peer_id, None)
        conn.close()
        print(f"[-] Disconnected {peer_id} from {ip}")

def main():
    load_relay_peers()
    public_ip = get_public_ip()
    print(f"[*] Relay Server {RELAY_ID} listening on 0.0.0.0:{PORT} (Public IP: {public_ip})")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', PORT))
    server.listen(50)

    while True:
        conn, addr = server.accept()
        threading.Thread(target=client_handler, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
