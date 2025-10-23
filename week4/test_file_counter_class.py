# week4/test_file_counter_class.py
from week4.file_counter_class import FileStats

def test_file_stats_class(tmp_path):
    f = tmp_path / "demo.txt"
    f.write_text("abc def\n123")
    stats = FileStats(str(f)).count()
    assert stats.lines == 2
    assert stats.words == 3
    assert stats.chars == len("abc def\n123")
