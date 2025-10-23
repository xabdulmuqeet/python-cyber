# week5/port_scanner.py

from week5.socket_client import check_port

def scan_ports(host, ports):
    open_ports = []
    for port in ports:
        if check_port(host, port):
            open_ports.append(port)
    return open_ports

if __name__ == "__main__":
    host = "127.0.0.1"
    ports = range(20, 1025)  # common ports
    result = scan_ports(host, ports)
    print(f"Open ports on {host}: {result}")
