# week1/test_port_scanner_threaded.py
import pytest
from week1.port_scanner_threaded import validate_port_range, scan_ports_threaded

def test_validate_port_range_ok():
    validate_port_range(1, 1024)

def test_validate_port_range_bad():
    with pytest.raises(ValueError):
        validate_port_range(0, 70000)
    with pytest.raises(ValueError):
        validate_port_range(100, 10)

def test_scan_ports_threaded_returns_list():
    res = scan_ports_threaded("127.0.0.1", 1, 20, timeout=0.05, concurrency=10)
    assert isinstance(res, list)
