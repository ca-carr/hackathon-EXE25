# P2P Relay Server Deployment Guide

This guide will help you deploy the P2P Relay Server to an AWS EC2 instance.

## Prerequisites

* AWS account with permissions to create EC2 instances
* Basic familiarity with command line tools
* SSH client (OpenSSH, PuTTY, etc.)

## 1. Preparing Your Code

Ensure your `main.py` and `relays.json` files are in a local folder. These will be uploaded to your EC2 instance to run the relay server.

## 2. Setting up an AWS EC2 Instance

1. **Log in to the AWS Management Console**

   * Go to [https://aws.amazon.com/console/](https://aws.amazon.com/console/)
   * Sign in with your credentials

2. **Launch a new EC2 instance**

   * Navigate to EC2 service
   * Click "Launch instance"

3. **Configure the instance**

   * Name: `p2p-relay-server`
   * AMI: Ubuntu Server 22.04 LTS
   * Instance type: t2.micro (Free tier eligible)
   * Key pair: Create a new key pair or select an existing one

     * If creating new: Name it `p2p-relay-keypair` and download the .pem file
     * Keep this key safe. DO NOT SHARE IT. You'll need it to access your instance

4. **Configure the security group**

   * Click to expand the security group settings
   * Create a new security group named `p2p-relay-sg`
   * Add the following inbound rules:

     * SSH (Port 22): Source = Your IP or 0.0.0.0/0 (anywhere)
     * Custom TCP (Port 55665): Source = 0.0.0.0/0 (anywhere)
     * You can select a different port, but ensure you update the `PORT` variable in `main.py`

> Q: What is SSH?

> Q: What is TCP?

5. **Review and launch**

   * Click "Launch instance"
   * Wait for the instance to initialize (about 1-2 minutes)
   * You can click on "Connect to instance" for instructions

6. **Note your instance's public IP**

   * Find it in the "Instances" section of the EC2 dashboard
   * It will look something like: `12.34.56.78`

## 3. Getting Your Code to your EC2 Instance

### Option 1: Connect via VS Code

1. **Install the Remote - SSH extension**

   * Open VS Code
   * Go to Extensions
   * Search for "Remote - SSH" and install it
   * Look for the extension by Microsoft

2. **Configure your SSH key**

   * For Windows:

     * Make sure your .pem file is in a location with restrictive permissions
     * You might need to convert the .pem to a .ppk file using PuTTYgen (maybe, try first without)
   * For macOS/Linux:

     * Run `chmod 400 /path/to/p2p-relay-keypair.pem` to set proper permissions

3. **Add your EC2 instance to VS Code**

   * Press F1 or Ctrl+Shift+P (Cmd+Shift+P on Mac)
   * Type "Remote-SSH: Add New SSH Host" and select it
   * Enter: `ssh -i /path/to/p2p-relay-keypair.pem ubuntu@YOUR_EC2_IP`
   * Select a config file to update (usually the first option)

4. **Connect to your EC2 instance**

   * Press F1 or Ctrl+Shift+P (Cmd+Shift+P on Mac)
   * Select "Remote-SSH: Connect to Host"
   * Choose your EC2 instance from the list
   * If prompted about host authenticity, click "Continue"
   * VS Code will connect to your EC2 instance
   * When prompted for platform, select Linux

5. **Open your terminal**

   * Once connected, click "Open Folder"
   * If you've uploaded files, navigate to where they are
   * If not, you can create a new folder and clone your repository later

### Option 2: Using SSH from Terminal

1. **Connect to your instance**

   ```bash
   # For Linux/Mac:
   ssh -i /path/to/p2p-relay-keypair.pem ubuntu@YOUR_EC2_IP
   ```

### Installing Git

2. **Install Git (if not already installed)**

   ```bash
   sudo apt update
   sudo apt install -y git
   ```

3. **Clone your repository**

   ```bash
   git clone https://github.com/ca-carr/hackathon-EXE25.git
   cd hackathon-EXE25/p2p-relay
   ```

   * You can open the folder in VSCode too

## 4. Running the Relay Server

1. **Install Python and create a virtual environment**

   ```bash
   sudo apt update
   sudo apt install -y python3 python3-venv
   python3 -m venv venv
   source venv/bin/activate
   pip install requests
   ```

2. **Update the Relay Configuration**

   ```bash
   cd ~/p2p-relay
   nano relays.json
   ```

   Replace the IPs in `relays.json` with the actual public IPs of your relay servers. Ensure the relay you are editing has a unique `RELAY_ID` and is not included in its own peer list.

3. **Run the Relay Server**

   ```bash
   python3 main.py
   ```

4. **View logs (if applicable)**

   * Messages will appear in the terminal
   * If enabled in code, logs are also written to `relay_log.jsonl`

## Running Multiple Relay Servers

If you want to run multiple relay servers (relay1, relay2, relay3), you'll need to:

1. Set up separate ports in your EC2 instance.
2. Update the `PORT` and `RELAY_ID` in `main.py`.
3. Update `relays.json` on all instances with the correct IPs and ports

## Additional Notes

* The relay server logs messages to `relay_log.jsonl` if `LOG_TO_DISK` is set to `True` in the code
* For long-running deployments, consider using `tmux` or `screen` to keep the server running after you disconnect

## Optional: Docker Packaging

Although this guide does not use Docker for deployment, you may optionally package your relay server as a Docker container, to share with your colleagues.

To build and run a Docker image (for later use or portability):

```bash
# Build
docker build -t p2p-relay .

# Run
docker run -d --name relay-server -p 55665:55665 p2p-relay
```

> Take a look at why we might use docker. What advantages does it have.
