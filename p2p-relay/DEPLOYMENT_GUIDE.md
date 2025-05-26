# P2P Relay Server Deployment Guide

This guide will help you deploy the P2P Relay Server to an AWS EC2 instance using Docker.

## Prerequisites

- AWS account with permissions to create EC2 instances
- Basic familiarity with command line tools
- SSH client (OpenSSH, PuTTY, etc.)

## 1. Packaging the Code into a Dockerfile

The Dockerfile has already been created for you in this directory. Here's what it does:

```
FROM python:3.9-slim      # Uses Python 3.9 as the base image
WORKDIR /app              # Sets the working directory in the container
COPY main.py .            # Copies your relay server code
COPY relays.json .        # Copies the relay configuration
RUN pip install requests  # Installs the required Python packages
EXPOSE 55665              # Exposes the port the relay listens on
CMD ["python", "main.py"] # Command to run when the container starts
```

## 2. Setting up an AWS EC2 Instance

1. **Log in to the AWS Management Console**
   - Go to https://aws.amazon.com/console/
   - Sign in with your credentials

2. **Launch a new EC2 instance**
   - Navigate to EC2 service
   - Click "Launch instance"

3. **Configure the instance**
   - Name: `p2p-relay-server`
   - AMI: Ubuntu Server 22.04 LTS
   - Instance type: t2.micro (Free tier eligible)
   - Key pair: Create a new key pair or select an existing one
     - If creating new: Name it `p2p-relay-keypair` and download the .pem file
     - Keep this key safe. DO NOT SHARE IT. You'll need it to access your instance

4. **Configure the security group**
   - Click to expand the security group settings
   - Create a new security group named `p2p-relay-sg`
   - Add the following inbound rules:
     - SSH (Port 22): Source = Your IP or 0.0.0.0/0 (anywhere)
     - Custom TCP (Port 55665): Source = 0.0.0.0/0 (anywhere). 
     - You can select a different port. How does that work?

> Q: What is SSH? 

> Q: WHat is TCP? 

5. **Review and launch**
   - Click "Launch instance"
   - Wait for the instance to initialize (about 1-2 minutes)
   - You can click on "Connect to instance" for instructions

6. **Note your instance's public IP**
   - Find it in the "Instances" section of the EC2 dashboard
   - It will look something like: `12.34.56.78`

## 3. Getting Your Code to your EC2 Instance

### Option 1: Connect via VS Code

1. **Install the Remote - SSH extension**
   - Open VS Code
   - Go to Extensions
   - Search for "Remote - SSH" and install it
   - Look for the extension by Microsoft

2. **Configure your SSH key**
   - For Windows: 
     - Make sure your .pem file is in a location with restrictive permissions
     - You might need to convert the .pem to a .ppk file using PuTTYgen
   - For macOS/Linux:
     - Run `chmod 400 /path/to/p2p-relay-keypair.pem` to set proper permissions

3. **Add your EC2 instance to VS Code**
   - Press F1 or Ctrl+Shift+P (Cmd+Shift+P on Mac)
   - Type "Remote-SSH: Add New SSH Host" and select it
   - Enter: `ssh -i /path/to/p2p-relay-keypair.pem ubuntu@YOUR_EC2_IP`
   - Select a config file to update (usually the first option)

4. **Connect to your EC2 instance**
   - Press F1 or Ctrl+Shift+P (Cmd+Shift+P on Mac)
   - Select "Remote-SSH: Connect to Host"
   - Choose your EC2 instance from the list
   - If prompted about host authenticity, click "Continue"
   - VS Code will connect to your EC2 instance
   - When prompted for platform, select Linux

5. **Open your terminal**
   - Once connected, click "Open Folder"
   - If you've uploaded files, navigate to where they are
   - If not, you can create a new folder and clone your repository later

### Option 2: Using SSH from Terminal

1. **Connect to your instance**
   ```bash
   # For Linux/Mac:
   ssh -i /path/to/p2p-relay-keypair.pem ubuntu@YOUR_EC2_IP
   ```

### Installing Git

2. **Install Git (if not already installed)**
   ```bash
   # On Ubuntu
   sudo apt update
   sudo apt install -y git
   ```

3. **Clone your repository**
   ```bash
   git clone https://github.com/ca-carr/hackathon-EXE25.git
   cd hackathon-EXE25/p2p-relay
   ```
   - You can open the folder in VSCode too

## 4. Setting Up Docker on EC2

1. **Install Docker**
   ```bash   
   # On Ubuntu
   sudo apt update
   sudo apt install -y docker.io
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -a -G docker ubuntu
   ```

2. **Log out and log back in for group changes to take effect**
   ```bash
   exit
   # Reconnect using the SSH command from step 3
   ```

## 5. Update the Relay Configuration

Before building the Docker image, update the `relays.json` file with the correct IP addresses:

```bash
cd ~/p2p-relay
nano relays.json
```

Replace `RELAY1_IP`, `RELAY2_IP`, and `RELAY3_IP` with the actual IP addresses of your relay servers. If you're only running one relay server, you can use your EC2 instance's public IP for all three.

Press Ctrl+X, then Y, then Enter to save your changes.

## 6. Building and Running the Docker Container

1. **Build the Docker image**
   ```bash
   cd ~/p2p-relay
   docker build -t p2p-relay .
   ```

2. **Run the container**
   ```bash
   docker run -d --name relay-server -p 55665:55665 p2p-relay
   ```

3. **Check if the container is running**
   ```bash
   docker ps
   ```
   You should see your container listed with status "Up".

4. **View logs if needed**
   ```bash
   docker logs relay-server
   ```

## Troubleshooting

1. **If the container stops unexpectedly:**
   ```bash
   docker logs relay-server
   ```
   Check the logs for any error messages.

2. **To restart the container:**
   ```bash
   docker restart relay-server
   ```

3. **To stop the container:**
   ```bash
   docker stop relay-server
   ```

4. **To remove the container and start fresh:**
   ```bash
   docker stop relay-server
   docker rm relay-server
   docker run -d --name relay-server -p 55665:55665 p2p-relay
   ```

## Running Multiple Relay Servers

If you're running multiple relay servers (relay1, relay2, relay3), you'll need to:

1. Set up separate EC2 instances for each relay
2. Update the PORT and RELAY_ID in main.py for each instance
3. Update relays.json on all instances with the correct IPs and ports
4. Expose the appropriate port in each Dockerfile (55665, 55666, or 55667)

## Additional Notes

- The relay server logs messages to `relay_log.jsonl` if `LOG_TO_DISK` is set to `True` in the code
- To make the container restart automatically if the EC2 instance reboots, add `--restart always` to your docker run command
- For production systems, consider using Docker Compose or container orchestration tools like ECS or Kubernetes 