# week1/test_port_scanner.py
import pytest
from week1.port_scanner import validate_port_range, scan_ports

def test_validate_port_range_ok():
    validate_port_range(1, 1024)  # should not raise

def test_validate_port_range_bad():
    with pytest.raises(ValueError):
        validate_port_range(0, 70000)
    with pytest.raises(ValueError):
        validate_port_range(100, 10)

def test_scan_ports_returns_list():
    # Non-invasive test: just ensure it returns a list and doesn't raise when scanning a tiny localhost range
    res = scan_ports('127.0.0.1', 1, 10, timeout=0.05)
    assert isinstance(res, list)
