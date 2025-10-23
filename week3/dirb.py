# week3/dirb.py
"""
Simple directory brute-forcer (HTTP) using requests.
Usage:
  python -m week3.dirb http://127.0.0.1:8000 --wordlist wordlist.txt --threads 10 --timeout 1.0
"""
import argparse
import requests
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.parse
import json

def probe_path(base_url: str, path: str, timeout: float = 1.0) -> dict:
    url = urllib.parse.urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))
    try:
        r = requests.get(url, timeout=timeout, allow_redirects=False)
        return {"path": path, "status": r.status_code, "length": len(r.content)}
    except Exception as e:
        return {"path": path, "error": str(e)}

def dirb_scan(base_url: str, words: List[str], timeout: float = 1.0, threads: int = 10) -> List[dict]:
    found = []
    with ThreadPoolExecutor(max_workers=threads) as ex:
        futures = {ex.submit(probe_path, base_url, w, timeout): w for w in words}
        for fut in as_completed(futures):
            res = fut.result()
            # consider 200 and 301/302 as interesting; you can adjust
            if res.get("status") in (200, 301, 302):
                found.append(res)
    return found

def main():
    parser = argparse.ArgumentParser(description="Simple directory brute-forcer")
    parser.add_argument("base_url", help="Base URL e.g. http://127.0.0.1:8000")
    parser.add_argument("--wordlist", required=True, help="Path to wordlist file")
    parser.add_argument("--threads", type=int, default=10)
    parser.add_argument("--timeout", type=float, default=1.0)
    parser.add_argument("--output", help="Output JSON file")
    args = parser.parse_args()

    with open(args.wordlist, "r", encoding="utf-8") as fh:
        words = [line.strip() for line in fh if line.strip()]

    results = dirb_scan(args.base_url, words, timeout=args.timeout, threads=args.threads)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as of:
            json.dump({"base_url": args.base_url, "found": results}, of, indent=2)
    else:
        for r in results:
            print(f"{r['path']} -> {r.get('status')} (len={r.get('length')})")

if __name__ == "__main__":
    main()
