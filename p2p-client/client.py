import socket

PEER_IP = '35.177.203.48'   #example relay ip
PEER_PORT = 55665           #example relay port

def connect_to_peer(ip, port):
    message = input("Enter message to send: ")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"Connecting to {ip}:{port}...")
            s.connect((ip, port))
            print("Connected!")

            s.sendall(message.encode())

            response = s.recv(4096)
            print("Response from peer:", response.decode())

    except (ConnectionRefusedError, TimeoutError, socket.gaierror):
        print("Could not connect to the peer. Is the server running?")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

connect_to_peer(PEER_IP, PEER_PORT)
