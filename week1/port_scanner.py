# week1/port_scanner.py
"""
Simple synchronous TCP port scanner (module style).
Usage:
    python -m week1.port_scanner 127.0.0.1 --start 1 --end 1024 --timeout 0.5
"""

import argparse
import socket
from typing import List

def validate_port_range(start: int, end: int):
    if start < 1 or end > 65535 or start > end:
        raise ValueError('Invalid port range')

def scan_ports(host: str, start: int, end: int, timeout: float = 0.5) -> List[int]:
    """Scan ports synchronously and return list of open ports."""
    validate_port_range(start, end)
    open_ports = []
    # try to resolve host to ensure early fail on bad hostname
    try:
        socket.gethostbyname(host)
    except socket.gaierror:
        raise
    for port in range(start, end + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            res = s.connect_ex((host, port))
            if res == 0:
                open_ports.append(port)
        finally:
            s.close()
    return open_ports

def main():
    parser = argparse.ArgumentParser(description='Simple TCP port scanner')
    parser.add_argument('host', help='Hostname or IP to scan')
    parser.add_argument('--start', type=int, default=1, help='Start port (default 1)')
    parser.add_argument('--end', type=int, default=1024, help='End port (default 1024)')
    parser.add_argument('--timeout', type=float, default=0.5, help='Socket timeout in seconds')
    args = parser.parse_args()

    try:
        ports = scan_ports(args.host, args.start, args.end, args.timeout)
        if ports:
            print('Open ports:', ','.join(map(str, ports)))
        else:
            print('No open ports found in range')
    except ValueError as e:
        print('Error:', e)
    except socket.gaierror:
        print('Error: Hostname could not be resolved')

if __name__ == '__main__':
    main()