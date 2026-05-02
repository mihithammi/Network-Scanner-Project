# These are the imports -- We borrow python inbuilt tools.
import socket
import ipaddress
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime

# Color Codes for terminal outputs.
GREEN  = "\033[92m"   # for open ports
YELLOW = "\033[93m"   # for warnings
CYAN   = "\033[96m"   # for info messages
RESET  = "\033[0m"    # resets colour back to normal
BOLD   = "\033[1m"    # makes text bold

# This lock stops two threads from printing at the same time.
print_lock = threading.Lock()

# FUNCTION 1: Scan one port on one host.
def scan_port(host,port,timeout):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a TCP Socket.
        sock.settimeout(timeout) #If no answer in X seconds, Give up.
        result = sock.connect_ex((host,port))
        sock.close()

        #Connect_ex return 0 if connected.
        if result == 0:
            return(host,port,True)
        else:
            return(host,port,False)
    except Exception:
        return(host,port,False)   

# FUNCTION 2: Get the name of a Service on a port.
def get_service(port):
    try:
        return socket.getservbyport(port,"tcp")
    except Exception:
        return "unknown"

# FUNCTION 3: Expand a subnet into a list of IPs.
def get_hosts(target):
    try:
        network = ipaddress.ip_network(target,strict=False)
        return[str(ip)for ip in network.hosts()] 
    except ValueError:
        try:
            ip = socket.gethostbyname(target)
            return[ip]
        except Exception:
            print(f"{YELLOW}Error: Cannot find host '{target}'{RESET}") 
            return[]

# FUNCTION 4: Parse port input.(This lets users type port like "22, 80, 443")
def parse_ports(port_input):
    ports = set()
    for part in port_input.split(","):
        part = set()
        for part in port_input.split(","):
            part = part.strip()
            if"-" in part:
                start,end = part.split("-")     # It is a range like 1-1024
                for p in range(int(start), int(end)+1):
                    ports.add(p)        # It is a single port like 80     
            else:
                ports.add(int(part))
        return sorted(ports)   

# FUNCTION 5: Run the full Scan.
def run_scan(hosts,ports,threads, timeout):
    open_ports = []
    all_tasks = [(h,p) for h in hosts for p in ports]
    total = len(all_tasks)

    print(f"\n {CYAN}Scanning {len(hosts)} hosts(s) across {len(ports)} port(s)"
          f" = {total} checks{RESET}")
    print(f"{CYAN}Threads:{threads} | Timeout: {timeout}s{RESET}\n") 

    with ThreadPoolExecutor(max_workers=threads) as pool:
        future_map = {
            pool.submit(scan_port,host,port,timeout):(host,port)
            for host,port in all_tasks
        }                
        done_count = 0

        for future in as_completed(future_map):
            done_count += 1
            host,port, is_open = future.result()

            if is_open:
                service = get_service(port)
                open_ports.append((host,port))
                with print_lock:
                    print(f" {GREEN}[OPEN]{RESET} {host:<18}"
                          f"Port {BOLD} {port:<6} {RESET} ({service})")

            pct = int(done_count / total * 40)
            bar = "█" * pct + "░" * (40 - pct) 
            with print_lock:
                print(f"\r [{bar}] {done_count}/{total}", end="",flush=True)

        print()  # new line after progress bar
        return sorted(open_ports)  

# FUNCTION 6: Print the banner at the top.
def print_banner():
    print(f"""
          {CYAN}{BOLD}
  ███╗   ██╗███████╗████████╗    ███████╗ ██████╗ █████╗ ███╗  ██╗
  ████╗  ██║██╔════╝╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗████╗ ██║
  ██╔██╗ ██║█████╗     ██║       ███████╗██║     ███████║██╔██╗██║
  ██║╚██╗██║██╔══╝     ██║       ╚════██║██║     ██╔══██║██║╚████║
  ██║ ╚████║███████╗   ██║       ███████║╚██████╗██║  ██║██║ ╚███║
  ╚═╝  ╚═══╝╚══════╝   ╚═╝       ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚══╝
          {RESET}
          {YELLOW}Network Discovery and Auditing Tool | Group 12 {RESET}
          """)  

### ___ MAIN SECTION ___ 
def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="Network Port Scanner - Group 12"
    )               

    parser.add_argument("target",
              help="IP address or subnet to scan (e.g. 192.168.1.1 or 192.168.1.0/24)")
    
    parser.add_argument("-p", "--ports", default="1-1024",
        help="Ports to scan. Examples: 80  or  22,80,443  or  1-1024")
    
    parser.add_argument("-t", "--threads", type=int, default=100,
        help="Number of threads (default: 100)")
    
    parser.add_argument("--timeout", type=float, default=1.0,
        help="Timeout per port in seconds (default: 1.0)")
    
    args = parser.parse_args()

    # Use our functions to prepare the scan
    hosts = get_hosts(args.target)
    ports = parse_ports(args.ports)

    if not hosts:
        print(f"{YELLOW}No valid hosts found. Exiting.{RESET}")
        return
    
    # Print a summary before starting
    start_time = datetime.now()
    print(f"  Target  : {args.target}")
    print(f"  Hosts   : {len(hosts)}")
    print(f"  Ports   : {ports[0]} to {ports[-1]}  ({len(ports)} total)")
    print(f"  Threads : {args.threads}")
    print(f"  Started : {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n  {'-' * 55}\n")

     # Run the scan
    results = run_scan(hosts, ports, args.threads, args.timeout)

     # Print the final summary
    elapsed = (datetime.now() - start_time).total_seconds()
    print(f"\n  {'-' * 55}")
    print(f"  Scan finished in {elapsed:.2f} seconds")
    print(f"  Open ports found: {GREEN}{BOLD}{len(results)}{RESET}\n")

# This means: only run main() if we run this file directly
if __name__ == "__main__":
    main()