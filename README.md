A Python-based multi-threaded TCP port scanner built for internal network auditing in system. Developed as a University Coursework Project.

**Group 12** — Python Programming: Network Programming Design, 2026

## What does this tool do?
This tool scans a target IP address or a range of IP addresses and checks which TCP ports are open. Open ports reveal which services are running on a system(Computer/Laptops), which is useful for security auditing.

For example:
 - Port 22 being open means SSH is running.
 - Port 80 means a web server is running.
 - Port 443 means HTTPS is running.

## Requirements:
- Python 3.10 or Higher.
- No extra libraries needed - Uses Python inbuilt libraries only.

## How to Install?
```
git clone https://github.com/mihithammi/Network-Scanner-Project.git
cd Network-Scanner-Project
```

## How to use?
Run the scanner from the terminal:
```
python scanner.py <target> [options]
```
**Options:**

| Option    | What it does                  | Default   |
|-----------|-------------------------------|-----------|
| target    | IP address or subnet to scan  | required  |
| -p        | Ports to scan                 | 1-1024    |
| -t        | Number of threads             | 100       |
| --timeout | Seconds to wait per port      | 1.0       |

## Example:
- Scan one IP on default ports:
```
python scanner.py 192.168.1.1
```

- Scan specific ports only:
```
python scanner.py 192.168.1.1 -p 22,80,443
```

- Scan a full subnet fast:
```
python scanner.py 192.168.1.0/24 -p 1-1024 -t 200 --timeout 0.5
```

- Scan your own computer (safe for testing):
```
python scanner.py 127.0.0.1 -p 1-1024
```

## How the code works:
This scanner is built in four phases as required by the assignment.

*Phase 1 - Core Networking* The 'scan_port()' function uses Python's socket module to make a TCP connection attempt. If the connection returns 0, the port is open.

*Phase 2 - Subnet Parsing* The 'get_hosts()' function uses Python's ipaddress module to expand a CIDR subnet like 192.168.1.0/24 into a list of 254 individual IP addresses.

*Phase 3 - Multi-threading* The 'run_scan()' function uses ThreadPoolExecutor to scan many ports at the same time instead of one by one. This make the scanner much faster.

*Phase 4 - CLI Interface* The argphase module provides a professional command-line interface where users can set the target,ports,threads and timeout without editing the code.

## Important legal notice
Only scan networkds and computers that you own or have written permission to scan. Unauthorised scanning may be illegal.
This tool is for authorised internal auditing and education only.

## Troubleshooting **Problem: "python is not recognized"** Solution: Python is not added to PATH. Reinstall Python and tick "Add Python to PATH" during setup. **Problem: Scanner shows nothing, no error** Solution: Check the last two lines of scanner.py are: ``` if __name__ == "__main__": main() ``` These lines must have no extra spaces at the start. **Problem: "git is not recognized"** Solution: Git is not installed. Download from git-scm.com and install with default options. **Problem: Push rejected on git push** Solution: Use your Personal Access Token as the password, not your real GitHub password.


## Authors
*Group 12*
- COHNDNE251F-17
- COHNDNE251F-30
- COHNDNE251F-42
- COHNDNE251F-46





