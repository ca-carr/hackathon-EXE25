import socket
import threading
import time
import json
from collections import defaultdict, deque
import requests

# === Configuration ===
PORT = 55665
RELAY_PEERS = [("127.0.0.1", 55666)]  # Add other relay IPs and ports here
RATE_LIMIT = 10       # max messages
RATE_INTERVAL = 10    # per seconds
LOG_TO_DISK = True    # set to False to disable file logging

# === Server State ===
clients = {}              # peer_id -> socket
client_ips = {}           # peer_id -> IP
rate_tracker = defaultdict(lambda: deque())  # ip -> deque[timestamps]
message_log = []          # all messages

# === Utilities ===
def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except Exception:
        return "unknown"

def is_rate_limited(ip):
    now = time.time()
    timestamps = rate_tracker[ip]
    while timestamps and now - timestamps[0] > RATE_INTERVAL:
        timestamps.popleft()
    if len(timestamps) >= RATE_LIMIT:
        return True
    timestamps.append(now)
    return False

def store_message(entry):
    message_log.append(entry)
    if LOG_TO_DISK:
        with open("relay_log.jsonl", "a") as f:
            f.write(json.dumps(entry) + "\n")

def broadcast(message, sender=None):
    """Send message to all clients and relay peers"""
    # Clients
    for peer_id, sock in list(clients.items()):
        if peer_id != sender:
            try:
                sock.sendall(message.encode())
            except:
                print(f"[!] Failed to send to {peer_id}")
    # Other relays
    for host, port in RELAY_PEERS:
        try:
            with socket.create_connection((host, port), timeout=3) as rsock:
                rsock.sendall(f"RELAY||{message}".encode())
        except Exception as e:
            print(f"[!] Relay forwarding failed to {host}:{port} - {e}")

# === Main Client Handler ===
def client_handler(conn, addr):
    ip = addr[0]
    print(f"[+] New connection from {ip}")

    try:
        peer_id = conn.recv(1024).decode().strip()
        if not peer_id:
            conn.close()
            return
        clients[peer_id] = conn
        client_ips[peer_id] = ip
        print(f"[+] Registered peer: {peer_id} ({ip})")

        while True:
            data = conn.recv(4096)
            if not data:
                break

            if is_rate_limited(ip):
                conn.sendall(b"[!] Rate limit exceeded.\n")
                continue

            try:
                raw = data.decode()
                if raw.startswith("RELAY||"):
                    _, msg = raw.split("RELAY||", 1)
                    broadcast(msg)  # rebroadcast if needed
                    continue

                target, msg_json = raw.split("||", 1)
                message = {
                    "from": peer_id,
                    "to": target,
                    "body": msg_json,
                    "timestamp": time.time(),
                    "ip": ip
                }
                store_message(message)

                if target == "ALL":
                    broadcast(msg_json, sender=peer_id)
                elif target in clients:
                    clients[target].sendall(msg_json.encode())
                else:
                    conn.sendall(f"[!] Target '{target}' not found.\n".encode())

            except Exception as e:
                conn.sendall(f"[!] Malformed message: {e}\n".encode())
                continue

    except Exception as e:
        print(f"[!] Error with client {ip}: {e}")
    finally:
        print(f"[-] Disconnecting {peer_id} ({ip})")
        clients.pop(peer_id, None)
        client_ips.pop(peer_id, None)
        conn.close()

# === Server Entry Point ===
def main():
    print("[*] Starting P2P Relay Server")
    public_ip = get_public_ip()
    print(f"[*] Public IP: {public_ip}")
    print(f"[*] Listening on 0.0.0.0:{PORT}")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", PORT))
    server.listen(50)

    while True:
        conn, addr = server.accept()
        threading.Thread(target=client_handler, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
