# week3/test_subfinder.py
from week3.subfinder import find_subdomains

def test_find_subdomains_no_matches(tmp_path, monkeypatch):
    # Create a tiny wordlist file (not used directly here)
    words = ["nosubdoesnotexist", "alsonothere"]
    # Use an obviously non-existent domain to avoid accidental hits
    found = find_subdomains("example.invalid", words, timeout=0.5)
    assert isinstance(found, list)
    assert found == []
