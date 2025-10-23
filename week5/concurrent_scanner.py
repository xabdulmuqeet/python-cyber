# week5/concurrent_scanner.py

from week5.socket_client import check_port
from threading import Thread
from queue import Queue

def worker(host, queue, results):
    while not queue.empty():
        port = queue.get()
        if check_port(host, port):
            results.append(port)
        queue.task_done()

def scan_ports_concurrent(host, ports, threads=10):
    queue = Queue()
    for port in ports:
        queue.put(port)

    results = []
    for _ in range(threads):
        t = Thread(target=worker, args=(host, queue, results))
        t.daemon = True
        t.start()

    queue.join()
    return sorted(results)

if __name__ == "__main__":
    host = "127.0.0.1"
    ports = range(20, 1025)
    open_ports = scan_ports_concurrent(host, ports, threads=20)
    print(f"Open ports on {host}: {open_ports}")
