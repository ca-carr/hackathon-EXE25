# peer_client.py
import socket
import threading
import json

SERVER_IP = '11.111.11.111'  # Replace with the public IP of the relay server
SERVER_PORT = 12345 # Replace with the port of the relay server

def recv_loop(sock):
    while True:
        data = sock.recv(4096)
        if not data:
            print("[!] Disconnected from server.")
            break
        print("[Received]", data.decode())

def main():
    peer_id = input("Enter your peer ID: ")
    target_id = input("Enter target peer ID to chat with: ")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    sock.sendall(peer_id.encode())

    threading.Thread(target=recv_loop, args=(sock,), daemon=True).start()

    print("Type messages to send. Press Ctrl+C to exit.")
    try:
        while True:
            text = input("> ")
            message = json.dumps({"from": peer_id, "text": text})
            sock.sendall(f"{target_id}||{message}".encode())
    except KeyboardInterrupt:
        print("\n[!] Exiting...")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
