# TCP Relay Client

This Python script `client.py` provides a simple TCP client for connecting to relay servers. It demonstrates basic socket programming concepts and network communication patterns.

## Overview

The client establishes a TCP connection to a specified relay server, sends a message, and receives a response. This is commonly used in distributed systems, peer-to-peer networks, or educational networking scenarios.

## Code Structure

### Key Components

**Socket Creation and Configuration**
```python
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
```
- `socket.AF_INET`: Specifies IPv4 addressing
- `socket.SOCK_STREAM`: Indicates TCP protocol (reliable, connection-oriented)
- Context manager (`with` statement) ensures automatic socket cleanup

**Connection Establishment**
```python
s.connect((ip, port))
```
- Initiates TCP three-way handshake with the target server
- Blocks until connection is established or timeout occurs

**Data Transmission**
```python
s.sendall(message.encode())
response = s.recv(4096)
```
- `sendall()`: Ensures complete message transmission (handles partial sends)
- `encode()`: Converts string to bytes (required for network transmission)
- `recv(4096)`: Receives up to 4096 bytes from the server
- `decode()`: Converts received bytes back to string

## Configuration

### Setting Your Relay Parameters

Before running the client, modify these variables to match your relay server:

```python
PEER_IP = '35.177.203.48'   # Replace with your relay server IP
PEER_PORT = 55665           # Replace with your relay server port
```

### Finding Your Relay Information

1. **IP Address**: Use your relay server's public IP address
   - For local testing: `127.0.0.1` or `localhost`
   - For remote servers: Obtain from your hosting provider or network administrator

2. **Port Number**: Use the port your relay server is listening on
   - Ensure the port is open and not blocked by firewalls
   - Common ranges: 1024-65535 (avoid well-known ports below 1024)

## Usage Instructions

### Basic Usage
1. Update `PEER_IP` and `PEER_PORT` with your relay server details
2. Run the script: `python client.py`
3. Enter your message when prompted
4. View the server's response

### Example Session
```
$ python client.py
Enter message to send: Hello, relay server!
Connecting to 192.168.1.100:8080...
Connected!
Response from peer: Message received successfully
```

## Error Handling

The client implements robust error handling for common network scenarios:

- **ConnectionRefusedError**: Server is not running or port is closed
- **TimeoutError**: Network timeout or server unresponsive
- **socket.gaierror**: DNS resolution failure or invalid IP address
- **General exceptions**: Catches unexpected errors for debugging

## Security Considerations

### Current Limitations
- **No encryption**: Messages are transmitted in plaintext
- **No authentication**: No verification of server identity
- **No input validation**: User input is sent directly to the server

## Troubleshooting

### Common Issues

**"Connection refused"**
- Verify the relay server is running
- Check IP address and port number
- Ensure firewall allows the connection

**"Network unreachable"**
- Verify network connectivity
- Check if IP address is correct
- Confirm routing to the target network

**"Operation timed out"**
- Server may be overloaded
- Network latency issues
- Consider increasing timeout values

### Testing Connectivity

Use these commands to verify network connectivity:

```bash
# Test basic connectivity
ping <relay_ip>

# Test port accessibility
telnet <relay_ip> <relay_port>
# or
nc -zv <relay_ip> <relay_port>
```

## Protocol Considerations

This client assumes a simple request-response protocol:
1. Client connects to server
2. Client sends one message
3. Server responds with one message
4. Connection closes

For different protocols, you may need to modify the communication pattern, handle multiple messages, or implement specific message framing.

## Notes

This implementation demonstrates several networking concepts:
- TCP socket programming fundamentals
- Client-server communication patterns
- Error handling in network applications
- Resource management with context managers

Understanding these concepts is essential for building more complex networked applications and distributed systems.