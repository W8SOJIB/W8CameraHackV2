#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Multi-Country Camera Scanner - Combined IP Range Collector & Camera Scanner
Author: W8Team/W8SOJIB
GitHub: github.com/W8SOJIB
Description: Select from 44 countries → Auto-fetch IP ranges → Auto-scan cameras
License: MIT
Termux Compatible: Yes
One-Click Operation: Yes
"""

import socket
import requests
import threading
from queue import Queue
import ipaddress
import pyfiglet
from datetime import datetime
import time
import sys
import aiohttp
import asyncio
import signal
import os

# Try to import colorama, but work without it (Termux compatibility)
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    # Fallback color codes
    class Fore:
        GREEN = '\033[92m'
        RED = '\033[91m'
        YELLOW = '\033[93m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
    
    class Style:
        RESET_ALL = '\033[0m'

# Configuration
OUTPUT_FILE = "BDALLIP.txt"
APNIC_URL = "https://ftp.apnic.net/stats/apnic/delegated-apnic-latest"
CCTV_OUTPUT = "CCTV Found.txt"

# Supported Countries (All APNIC Region)
COUNTRIES = {
    '1': {'name': 'Afghanistan', 'code': 'AF', 'file': 'AF_IP.txt'},
    '2': {'name': 'Australia', 'code': 'AU', 'file': 'AU_IP.txt'},
    '3': {'name': 'Bangladesh', 'code': 'BD', 'file': 'BD_IP.txt'},
    '4': {'name': 'Brunei', 'code': 'BN', 'file': 'BN_IP.txt'},
    '5': {'name': 'Bhutan', 'code': 'BT', 'file': 'BT_IP.txt'},
    '6': {'name': 'China', 'code': 'CN', 'file': 'CN_IP.txt'},
    '7': {'name': 'Cook Islands', 'code': 'CK', 'file': 'CK_IP.txt'},
    '8': {'name': 'Fiji', 'code': 'FJ', 'file': 'FJ_IP.txt'},
    '9': {'name': 'Micronesia', 'code': 'FM', 'file': 'FM_IP.txt'},
    '10': {'name': 'Guam', 'code': 'GU', 'file': 'GU_IP.txt'},
    '11': {'name': 'Hong Kong', 'code': 'HK', 'file': 'HK_IP.txt'},
    '12': {'name': 'Indonesia', 'code': 'ID', 'file': 'ID_IP.txt'},
    '13': {'name': 'India', 'code': 'IN', 'file': 'IN_IP.txt'},
    '14': {'name': 'Japan', 'code': 'JP', 'file': 'JP_IP.txt'},
    '15': {'name': 'Cambodia', 'code': 'KH', 'file': 'KH_IP.txt'},
    '16': {'name': 'Kiribati', 'code': 'KI', 'file': 'KI_IP.txt'},
    '17': {'name': 'South Korea', 'code': 'KR', 'file': 'KR_IP.txt'},
    '18': {'name': 'Sri Lanka', 'code': 'LK', 'file': 'LK_IP.txt'},
    '19': {'name': 'Laos', 'code': 'LA', 'file': 'LA_IP.txt'},
    '20': {'name': 'Myanmar', 'code': 'MM', 'file': 'MM_IP.txt'},
    '21': {'name': 'Mongolia', 'code': 'MN', 'file': 'MN_IP.txt'},
    '22': {'name': 'Macau', 'code': 'MO', 'file': 'MO_IP.txt'},
    '23': {'name': 'Maldives', 'code': 'MV', 'file': 'MV_IP.txt'},
    '24': {'name': 'Malaysia', 'code': 'MY', 'file': 'MY_IP.txt'},
    '25': {'name': 'New Caledonia', 'code': 'NC', 'file': 'NC_IP.txt'},
    '26': {'name': 'Nepal', 'code': 'NP', 'file': 'NP_IP.txt'},
    '27': {'name': 'Nauru', 'code': 'NR', 'file': 'NR_IP.txt'},
    '28': {'name': 'New Zealand', 'code': 'NZ', 'file': 'NZ_IP.txt'},
    '29': {'name': 'French Polynesia', 'code': 'PF', 'file': 'PF_IP.txt'},
    '30': {'name': 'Papua New Guinea', 'code': 'PG', 'file': 'PG_IP.txt'},
    '31': {'name': 'Philippines', 'code': 'PH', 'file': 'PH_IP.txt'},
    '32': {'name': 'Pakistan', 'code': 'PK', 'file': 'PK_IP.txt'},
    '33': {'name': 'North Korea', 'code': 'KP', 'file': 'KP_IP.txt'},
    '34': {'name': 'Palau', 'code': 'PW', 'file': 'PW_IP.txt'},
    '35': {'name': 'Solomon Islands', 'code': 'SB', 'file': 'SB_IP.txt'},
    '36': {'name': 'Singapore', 'code': 'SG', 'file': 'SG_IP.txt'},
    '37': {'name': 'Thailand', 'code': 'TH', 'file': 'TH_IP.txt'},
    '38': {'name': 'Timor-Leste', 'code': 'TL', 'file': 'TL_IP.txt'},
    '39': {'name': 'Tonga', 'code': 'TO', 'file': 'TO_IP.txt'},
    '40': {'name': 'Taiwan', 'code': 'TW', 'file': 'TW_IP.txt'},
    '41': {'name': 'Vanuatu', 'code': 'VU', 'file': 'VU_IP.txt'},
    '42': {'name': 'Vietnam', 'code': 'VN', 'file': 'VN_IP.txt'},
    '43': {'name': 'Samoa', 'code': 'WS', 'file': 'WS_IP.txt'},
    '44': {'name': 'United States (APNIC)', 'code': 'US', 'file': 'US_IP.txt'},
}

# Current selected country
SELECTED_COUNTRY = None

# Set a default timeout for socket connections
socket.setdefaulttimeout(0.25)

# Set to store detected IPs
detected_ips = set()

# Global control flags
stop_scan = False
pause_scan = False


def print_banner():
    """Display main banner"""
    banner = f"""
╔═══════════════════════════════════════╗
║   Multi-Country Camera Scanner        ║
║   W8Team - IP Scanner & Collector     ║
║   Credit: W8Team/W8SOJIB              ║
╚═══════════════════════════════════════╝
"""
    print(f"{Fore.RED}{banner}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[*] Developed by: {Fore.YELLOW}W8Team/W8SOJIB{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[*] GitHub: {Fore.YELLOW}github.com/W8SOJIB{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[*] Termux Supported ✓{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[*] Supports: {Fore.YELLOW}{len(COUNTRIES)} Countries{Style.RESET_ALL}\n")


def print_country_menu():
    """Display country selection menu"""
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Select Country (Total: {len(COUNTRIES)} Countries):{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    
    # Display in 3 columns for better organization
    countries_list = list(COUNTRIES.items())
    rows = (len(countries_list) + 2) // 3  # 3 columns
    
    for i in range(rows):
        row_str = ""
        for col in range(3):
            idx = i + (col * rows)
            if idx < len(countries_list):
                country = countries_list[idx]
                col_str = f"{Fore.YELLOW}{country[0]:2s}.{Style.RESET_ALL} {country[1]['name']:<22}"
                row_str += col_str
        print(f"  {row_str}")
    
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")


def select_country():
    """Allow user to select a country"""
    global SELECTED_COUNTRY, OUTPUT_FILE, CCTV_OUTPUT
    
    print_country_menu()
    
    while True:
        choice = input(f"{Fore.GREEN}Enter country number (1-{len(COUNTRIES)}):{Style.RESET_ALL} ").strip()
        
        if choice in COUNTRIES:
            SELECTED_COUNTRY = COUNTRIES[choice]
            OUTPUT_FILE = SELECTED_COUNTRY['file']
            CCTV_OUTPUT = f"{SELECTED_COUNTRY['code']}_CCTV_Found.txt"
            
            print(f"\n{Fore.GREEN}[✓] Selected:{Style.RESET_ALL} {Fore.YELLOW}{SELECTED_COUNTRY['name']}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[i]{Style.RESET_ALL} Country Code: {SELECTED_COUNTRY['code']}")
            print(f"{Fore.CYAN}[i]{Style.RESET_ALL} IP File: {OUTPUT_FILE}")
            print(f"{Fore.CYAN}[i]{Style.RESET_ALL} Output File: {CCTV_OUTPUT}\n")
            return True
        else:
            print(f"{Fore.RED}[!] Invalid choice. Please select 1-{len(COUNTRIES)}.{Style.RESET_ALL}")


def get_public_ip():
    """Get the public IP address"""
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        if response.status_code == 200:
            return response.text
        else:
            return "Unknown"
    except Exception as e:
        return "Unknown"


def get_country(ip):
    """Get the country based on IP address"""
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('country', 'Unknown')
        else:
            return "Unknown"
    except Exception as e:
        return "Unknown"


async def fetch_country_ipv4(country_code):
    """Fetch IPv4 ranges for specified country from APNIC"""
    ipv4_list = []
    
    if not country_code:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} No country selected!")
        return []
    
    try:
        async with aiohttp.ClientSession() as session:
            print(f"{Fore.YELLOW}[*]{Style.RESET_ALL} Connecting to APNIC server...")
            print(f"{Fore.CYAN}[i]{Style.RESET_ALL} Fetching IP ranges for: {Fore.YELLOW}{country_code}{Style.RESET_ALL}")
            
            async with session.get(APNIC_URL, timeout=aiohttp.ClientTimeout(total=60)) as resp:
                if resp.status != 200:
                    print(f"{Fore.RED}[!]{Style.RESET_ALL} Error: Server returned status {resp.status}")
                    return []
                
                print(f"{Fore.GREEN}[✓]{Style.RESET_ALL} Connected successfully!")
                print(f"{Fore.YELLOW}[*]{Style.RESET_ALL} Downloading and parsing data...\n")
                
                line_count = 0
                async for line_bytes in resp.content:
                    line = line_bytes.decode('utf-8', errors='ignore').strip()
                    
                    if not line or line.startswith('#'):
                        continue
                    
                    parts = line.split('|')
                    
                    # Filter country IPv4 entries
                    if len(parts) >= 7 and parts[1].upper() == country_code.upper() and parts[2].lower() == 'ipv4':
                        start_ip = parts[3]
                        count = int(parts[4])
                        ipv4_list.append(f"{start_ip}/{count}")
                        
                        # Show progress every 5 entries
                        if len(ipv4_list) % 5 == 0:
                            sys.stdout.write(f"\r{Fore.CYAN}[→]{Style.RESET_ALL} Found {len(ipv4_list)} {country_code} IPv4 ranges...")
                            sys.stdout.flush()
                    
                    line_count += 1
                
                print(f"\n{Fore.GREEN}[✓]{Style.RESET_ALL} Processing complete! Scanned {line_count} lines")
                
    except asyncio.TimeoutError:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} Error: Connection timeout")
        return []
    except aiohttp.ClientError as e:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} Network error: {e}")
        return []
    except Exception as e:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} Unexpected error: {e}")
        return []
    
    return ipv4_list


async def save_ip_ranges(ipv4_list):
    """Save IPv4 ranges to file"""
    if not ipv4_list:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} No data to save")
        return False
    
    try:
        print(f"\n{Fore.YELLOW}[*]{Style.RESET_ALL} Saving to {OUTPUT_FILE}...")
        
        with open(OUTPUT_FILE, 'w') as f:
            f.write('\n'.join(ipv4_list))
        
        print(f"{Fore.GREEN}[✓]{Style.RESET_ALL} Successfully saved {len(ipv4_list)} ranges")
        print(f"{Fore.CYAN}[i]{Style.RESET_ALL} File location: {OUTPUT_FILE}")
        return True
        
    except IOError as e:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} File error: {e}")
        return False


def cidr_to_ip_range(cidr_notation):
    """Convert CIDR notation (IP/count) to IP range"""
    try:
        # Parse the custom format: IP/count
        ip_str, count_str = cidr_notation.split('/')
        count = int(count_str)
        
        # Convert to standard CIDR
        # count represents the number of IPs
        # Calculate prefix length from count
        import math
        if count <= 0:
            return []
        
        # Find the prefix length: 32 - log2(count)
        prefix_len = 32 - int(math.log2(count))
        
        # Create network object
        network = ipaddress.IPv4Network(f"{ip_str}/{prefix_len}", strict=False)
        
        return [str(ip) for ip in network.hosts()]
    except Exception as e:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} Error parsing {cidr_notation}: {e}")
        return []


def scan(ip, port):
    """Scan a specific IP and port for cameras"""
    global stop_scan, pause_scan
    
    # Check if scan should stop
    if stop_scan:
        return
    
    # Wait while paused
    while pause_scan and not stop_scan:
        time.sleep(0.1)
    
    if stop_scan:
        return
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, port))
            sock.send(b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n')
            response = sock.recv(4096).decode()
            
            camera_found = False
            camera_type = ""
            url = f"http://{ip}:{port}" if port == 8080 else f"http://{ip}"
            
            if 'HTTP' in response and '<title>WEB SERVICE</title>' in response:
                if ip not in detected_ips:
                    detected_ips.add(ip)
                    camera_type = "Anjhua-Dahua Technology Camera"
                    camera_found = True
                    print(f"{Fore.GREEN}[✓] {camera_type} Found!{Style.RESET_ALL} at {Fore.CYAN}{url}{Style.RESET_ALL}")
                    
            elif 'HTTP' in response and 'login.asp' in response:
                if ip not in detected_ips:
                    detected_ips.add(ip)
                    camera_type = "HIK Vision Camera"
                    camera_found = True
                    print(f"{Fore.RED}[✓] {camera_type} Found!{Style.RESET_ALL} at {Fore.CYAN}{url}{Style.RESET_ALL}")
            
            # Live save to file
            if camera_found:
                try:
                    with open(CCTV_OUTPUT, 'a', encoding='utf-8') as file:
                        file.write(f"{'='*60}\n")
                        file.write(f"Camera Type: {camera_type}\n")
                        file.write(f"IP Address: {ip}\n")
                        file.write(f"Port: {port}\n")
                        file.write(f"URL: {url}\n")
                        file.write(f"Detection Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        file.write(f"{'='*60}\n\n")
                        file.flush()  # Force write to disk immediately (live save)
                except Exception as e:
                    pass
                    
    except Exception as e:
        pass


def execute(queue):
    """Execute the scan from the queue"""
    global stop_scan
    try:
        while not stop_scan:
            try:
                ip, port = queue.get(timeout=0.5)
                scan(ip, port)
                queue.task_done()
            except:
                if stop_scan:
                    break
                continue
    except KeyboardInterrupt:
        stop_scan = True
        return


def signal_handler_stop(signum, frame):
    """Handle Ctrl+C - Immediate stop"""
    global stop_scan
    stop_scan = True
    print(f"\n\n{Fore.RED}[!] Ctrl+C detected - STOPPING IMMEDIATELY...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Cleaning up threads...{Style.RESET_ALL}")
    sys.exit(0)


def signal_handler_pause(signum, frame):
    """Handle Ctrl+Z - Pause/Resume"""
    global pause_scan
    pause_scan = not pause_scan
    if pause_scan:
        print(f"\n\n{Fore.YELLOW}[⏸] SCAN PAUSED - Press Ctrl+Z again to resume...{Style.RESET_ALL}\n")
    else:
        print(f"\n\n{Fore.GREEN}[▶] SCAN RESUMED - Continuing...{Style.RESET_ALL}\n")


def load_ip_ranges():
    """Load IP ranges from BDALLIP.txt"""
    try:
        with open(OUTPUT_FILE, 'r') as f:
            ranges = [line.strip() for line in f if line.strip()]
        return ranges
    except FileNotFoundError:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} {OUTPUT_FILE} not found!")
        return None
    except Exception as e:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} Error reading file: {e}")
        return None


def run_scanner():
    """Run the IP scanner"""
    global stop_scan, pause_scan, SELECTED_COUNTRY
    
    # Reset flags
    stop_scan = False
    pause_scan = False
    
    # Register signal handlers
    try:
        signal.signal(signal.SIGINT, signal_handler_stop)  # Ctrl+C
        if hasattr(signal, 'SIGTSTP'):  # Unix/Linux/Mac
            signal.signal(signal.SIGTSTP, signal_handler_pause)  # Ctrl+Z
    except:
        pass  # Windows might not support SIGTSTP
    
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[*] Starting Camera Scanner{Style.RESET_ALL}")
    if SELECTED_COUNTRY:
        print(f"{Fore.CYAN}[i] Scanning Country:{Style.RESET_ALL} {Fore.YELLOW}{SELECTED_COUNTRY['name']} ({SELECTED_COUNTRY['code']}){Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}[*] Controls:{Style.RESET_ALL}")
    print(f"  {Fore.RED}Ctrl+C{Style.RESET_ALL} - Stop scan immediately")
    if hasattr(signal, 'SIGTSTP'):
        print(f"  {Fore.YELLOW}Ctrl+Z{Style.RESET_ALL} - Pause/Resume scan")
    print()
    
    # Load IP ranges
    ip_ranges = load_ip_ranges()
    if not ip_ranges:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} No IP ranges to scan. Exiting...")
        return
    
    print(f"{Fore.GREEN}[✓]{Style.RESET_ALL} Loaded {len(ip_ranges)} IP ranges from {OUTPUT_FILE}")
    print(f"{Fore.YELLOW}[*]{Style.RESET_ALL} Starting scan on ports 80 and 8080...")
    print(f"{Fore.CYAN}[i]{Style.RESET_ALL} Results will be saved to {Fore.GREEN}{CCTV_OUTPUT}{Style.RESET_ALL} (Live Save)\n")
    
    queue = Queue()
    start_time = time.time()
    
    # Create worker threads
    threads = []
    for _ in range(100):
        thread = threading.Thread(target=execute, args=(queue,), daemon=True)
        thread.start()
        threads.append(thread)
    
    # Enqueue IPs and ports for scanning
    try:
        total_ips = 0
        for idx, cidr in enumerate(ip_ranges, 1):
            if stop_scan:
                break
            
            print(f"\r{Fore.YELLOW}[*]{Style.RESET_ALL} Processing range {idx}/{len(ip_ranges)}: {cidr}...", end='')
            sys.stdout.flush()
            
            ips = cidr_to_ip_range(cidr)
            for ip in ips:
                if stop_scan:
                    break
                queue.put((ip, 80))
                queue.put((ip, 8080))
                total_ips += 1
        
        if not stop_scan:
            print(f"\n{Fore.GREEN}[✓]{Style.RESET_ALL} Queued {total_ips} IPs for scanning")
            print(f"{Fore.YELLOW}[*]{Style.RESET_ALL} Scanning in progress...\n")
            
            # Wait for all tasks to complete or stop signal
            while not stop_scan and not queue.empty():
                time.sleep(0.5)
        
    except KeyboardInterrupt:
        stop_scan = True
        print(f"\n\n{Fore.YELLOW}[!]{Style.RESET_ALL} Ctrl+C detected. Stopping...")
    except Exception as e:
        print(f"\n{Fore.RED}[!]{Style.RESET_ALL} Error: {e}")
    
    # Mark as stopped
    stop_scan = True
    time.sleep(1)  # Give threads time to finish
    
    elapsed_time = time.time() - start_time
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[✓] Scan Complete!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[i]{Style.RESET_ALL} Time taken: {elapsed_time:.2f} seconds")
    print(f"{Fore.CYAN}[i]{Style.RESET_ALL} Cameras found: {len(detected_ips)}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")


async def update_ip_ranges():
    """Fetch and update IP ranges from APNIC"""
    global SELECTED_COUNTRY
    
    if not SELECTED_COUNTRY:
        print(f"{Fore.RED}[!] No country selected! Please select a country first.{Style.RESET_ALL}")
        return False
    
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[*] Fetching {SELECTED_COUNTRY['name']} IP Ranges{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
    
    ipv4_list = await fetch_country_ipv4(SELECTED_COUNTRY['code'])
    
    if ipv4_list:
        await save_ip_ranges(ipv4_list)
        return True
    else:
        print(f"\n{Fore.RED}[!] Failed to fetch IP ranges{Style.RESET_ALL}")
        return False


def print_menu():
    """Print main menu"""
    global SELECTED_COUNTRY
    
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Main Menu:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    
    print(f"{Fore.YELLOW}1.{Style.RESET_ALL} Select Country & Scan")
    print(f"{Fore.YELLOW}2.{Style.RESET_ALL} Exit")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")


async def main():
    """Main function"""
    global SELECTED_COUNTRY
    
    print_banner()
    
    # Display system info
    try:
        public_ip = get_public_ip()
        country = get_country(public_ip)
        timestamp = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
        print(f"{Fore.GREEN}[i]{Style.RESET_ALL} Your IP: {Fore.YELLOW}{public_ip}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[i]{Style.RESET_ALL} Country: {Fore.YELLOW}{country}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[i]{Style.RESET_ALL} Time: {Fore.YELLOW}{timestamp}{Style.RESET_ALL}")
    except:
        pass
    
    while True:
        try:
            print_menu()
            choice = input(f"{Fore.GREEN}Enter your choice (1-2):{Style.RESET_ALL} ").strip()
            
            if choice == '1':
                # Select Country & Auto Scan
                select_country()
                if SELECTED_COUNTRY:
                    print(f"\n{Fore.CYAN}[*] Starting automatic update and scan...{Style.RESET_ALL}")
                    success = await update_ip_ranges()
                    if success:
                        run_scanner()
                    else:
                        print(f"{Fore.YELLOW}[!] Skipping scan due to update failure{Style.RESET_ALL}")
            elif choice == '2':
                # Exit
                print(f"\n{Fore.GREEN}[✓] Goodbye!{Style.RESET_ALL}\n")
                break
            else:
                print(f"{Fore.RED}[!] Invalid choice. Please select 1-2.{Style.RESET_ALL}")
        
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}[!] Interrupted by user{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"\n{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Interrupted by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}[!] Fatal error: {e}{Style.RESET_ALL}")
        sys.exit(1)

