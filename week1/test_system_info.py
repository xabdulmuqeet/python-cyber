import week1.system_info as si

def test_get_system_info_non_empty():
    info = si.get_system_info()
    assert isinstance(info, dict)
    assert info.get('os') is not None and info['os'] != ''
    assert info.get('user') is not None and info['user'] != ''
    assert info.get('hostname') is not None and info['hostname'] != ''
