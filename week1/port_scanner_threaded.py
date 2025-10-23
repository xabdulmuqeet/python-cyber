# week1/port_scanner_threaded.py
"""
Threaded TCP port scanner using ThreadPoolExecutor.

Usage examples:
  python -m week1.port_scanner_threaded 127.0.0.1 --start 1 --end 200 --concurrency 50
  python -m week1.port_scanner_threaded 127.0.0.1 --start 1 --end 200 --concurrency 50 --json
"""

import argparse
import socket
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

def validate_port_range(start: int, end: int):
    if start < 1 or end > 65535 or start > end:
        raise ValueError("Invalid port range")

def _probe_port(host: str, port: int, timeout: float) -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        res = s.connect_ex((host, port))
        return port if res == 0 else 0
    except Exception:
        return 0
    finally:
        try:
            s.close()
        except Exception:
            pass

def scan_ports_threaded(host: str, start: int, end: int, timeout: float = 0.5, concurrency: int = 50) -> List[int]:
    """
    Scan ports using a thread pool. Returns list of open ports.
    Raises socket.gaierror if host cannot be resolved, ValueError for bad ranges.
    """
    validate_port_range(start, end)
    # resolve early
    try:
        socket.gethostbyname(host)
    except socket.gaierror:
        raise
    open_ports = []
    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        futures = {ex.submit(_probe_port, host, p, timeout): p for p in range(start, end + 1)}
        for fut in as_completed(futures):
            try:
                res = fut.result()
                if res:
                    open_ports.append(res)
            except Exception:
                # swallow probe errors; non-fatal for individual ports
                pass
    open_ports.sort()
    return open_ports

def main():
    parser = argparse.ArgumentParser(description="Threaded TCP port scanner")
    parser.add_argument("host", help="Hostname or IP")
    parser.add_argument("--start", type=int, default=1, help="Start port")
    parser.add_argument("--end", type=int, default=1024, help="End port")
    parser.add_argument("--timeout", type=float, default=0.5, help="Socket timeout seconds")
    parser.add_argument("--concurrency", type=int, default=50, help="Thread pool size")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    try:
        ports = scan_ports_threaded(args.host, args.start, args.end, args.timeout, args.concurrency)
        if args.json:
            print(json.dumps({"open_ports": ports}))
        else:
            if ports:
                print("Open ports:", ",".join(map(str, ports)))
            else:
                print("No open ports found in range")
    except ValueError as e:
        print("Error:", e)
    except socket.gaierror:
        print("Error: Hostname could not be resolved")

if __name__ == "__main__":
    main()
