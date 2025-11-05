## Simples CMDs to research ports:

- `nmap -p- --open -sS -vvv -Pn -n --min-rate 5000 {IP/Domain}`
- `nmap -sC -sV -p{PORTS (There can be several ports separated by commas, ex: -p80,20,443,...)} {IP/Domain}`

## Explain each one parameters:

- `-p-`: Scan all Ports 1-65535.
- `--open`: Return only open Ports.
- `-sS`: Efficient Method for TCP SYN scan. It sends a SYN packet to the target port and waits for a SYN/ACK response to consider it open.
- `-vvv`: Verbose, maximum verbosity: prints very detailed, real-time progress and response info to the terminal.
- `-Pn`: 
 - `-Pn`: Treat target hosts as online and skip host discovery (no ICMP/ARP/port ping). Useful when ICMP/pings are blocked or hosts are behind firewalls, but may waste time scanning hosts that are actually down and increase false positives.
 - `-n`: No DNS resolution — do not try to resolve IPs to names. Speeds the scan and keeps output strictly IP-based. Useful for faster scans and when DNS is unreliable or unwanted.
 - `--min-rate <number>`: Ask Nmap to send packets at least at this rate (packets per second). Forces a faster, more aggressive scan; higher rates increase noise, packet loss, or the chance of being detected by IDS/IPS.
 - `-sC`: Run the default set of NSE (Nmap Scripting Engine) scripts. Performs common checks and probes (service info, simple vuln checks). Convenient for quick reconnaissance but increases scan time and network activity.
 - `-sV`: Service/version detection — probe open ports to identify the running service and its version string. Helpful for fingerprinting and prioritizing follow-ups; this also slows the scan and can make it noisier.
 - `-p{PORTS}`: Specify which ports to scan. Accepts single ports (e.g., `-p80`), comma-separated lists (`-p80,443,8080`), ranges (`-p1-1024`), or the special `-p-` (all ports). The scan protocol (TCP/UDP) depends on the scan flags you use (e.g., `-sS` is TCP SYN; combine with `-sU` for UDP).

 - (Tip) A common fast-recon combination is `-n -Pn --min-rate <num> -p-` when you need speed and hosts don't respond to pings — but be aware this increases false positives and detection risk. For safer, more complete reconnaissance, add `-sV` and `-sC` selectively or target specific ports with `-p`.