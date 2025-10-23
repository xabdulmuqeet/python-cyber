# week5/socket_client.py

import socket

def check_port(host, port, timeout=1):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (ConnectionRefusedError, TimeoutError, OSError):
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simple TCP client test")
    parser.add_argument("host", help="Target host")
    parser.add_argument("port", type=int, help="Target port")
    args = parser.parse_args()

    if check_port(args.host, args.port):
        print(f"{args.host}:{args.port} is open")
    else:
        print(f"{args.host}:{args.port} is closed")
