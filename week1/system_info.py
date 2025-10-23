import platform
import getpass
import socket

def get_system_info():
    info = {}
    try:
        info['os'] = platform.system() + " " + platform.release()
    except Exception:
        info['os'] = 'unknown'
    try:
        info['python_version'] = platform.python_version()
    except Exception:
        info['python_version'] = 'unknown'
    try:
        info['user'] = getpass.getuser()
    except Exception:
        info['user'] = 'unknown'
    try:
        info['hostname'] = socket.gethostname()
    except Exception:
        info['hostname'] = 'unknown'
    return info

def main():
    info = get_system_info()
    print("System Information:")
    for key, value in info.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
