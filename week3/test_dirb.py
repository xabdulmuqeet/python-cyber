# week3/test_dirb.py
from week3.dirb import dirb_scan
import http.server
import socketserver
import threading
import time

def run_simple_server(tmp_path):
    # start a simple HTTP server that serves the tmp_path directory
    handler = http.server.SimpleHTTPRequestHandler
    port = 8000
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.2)
    return httpd

def test_dirb_scan_tmpdir(tmp_path):
    # create a file that should be discovered
    (tmp_path / "secret").write_text("pwned")
    cwd = tmp_path.cwd()
    # run server serving tmp_path
    import os
    old = os.getcwd()
    os.chdir(str(tmp_path))
    httpd = run_simple_server(tmp_path)
    try:
        words = ["secret", "nope"]
        found = dirb_scan("http://127.0.0.1:8000", words, timeout=0.5, threads=4)
        # Expect the 'secret' path to be found (200)
        hits = [r for r in found if r.get("path") == "secret"]
        assert len(hits) >= 1
    finally:
        httpd.shutdown()
        os.chdir(old)
