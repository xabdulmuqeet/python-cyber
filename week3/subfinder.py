# week3/subfinder.py
"""
Simple subdomain enumeration using a wordlist and DNS A/AAAA lookups (dnspython).
Usage:
  python -m week3.subfinder example.com --wordlist wordlist.txt --timeout 2.0 --output out.json
"""
import argparse
import dns.resolver
import json
from typing import List, Dict

def query_host(name: str, timeout: float = 2.0) -> bool:
    resolver = dns.resolver.Resolver()
    resolver.lifetime = timeout
    try:
        answers = resolver.resolve(name, "A")
        return True
    except Exception:
        # no A record or resolution failed
        return False

def find_subdomains(domain: str, words: List[str], timeout: float = 2.0) -> List[str]:
    found = []
    for w in words:
        sub = f"{w.strip()}.{domain}"
        try:
            if query_host(sub, timeout=timeout):
                found.append(sub)
        except Exception:
            # ignore lookup exceptions per-subdomain
            pass
    return found

def main():
    parser = argparse.ArgumentParser(description="Subdomain finder (wordlist + DNS)")
    parser.add_argument("domain", help="Target domain (e.g. example.com)")
    parser.add_argument("--wordlist", required=True, help="Path to wordlist (one word per line)")
    parser.add_argument("--timeout", type=float, default=2.0, help="DNS query timeout seconds")
    parser.add_argument("--output", help="Write JSON output to file")
    args = parser.parse_args()

    with open(args.wordlist, "r", encoding="utf-8") as fh:
        words = [line.strip() for line in fh if line.strip()]

    results = find_subdomains(args.domain, words, timeout=args.timeout)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as of:
            json.dump({"domain": args.domain, "found": results}, of, indent=2)
    else:
        for r in results:
            print(r)

if __name__ == "__main__":
    main()
