# week4/file_counter_class.py

class FileStats:
    def __init__(self, path):
        self.path = path
        self.lines = 0
        self.words = 0
        self.chars = 0

    def count(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                for line in f:
                    self.lines += 1
                    self.words += len(line.split())
                    self.chars += len(line)
        except FileNotFoundError:
            print(f"Error: File not found -> {self.path}")
        except PermissionError:
            print(f"Error: Permission denied -> {self.path}")
        return self

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="FileStats class counter")
    parser.add_argument("path", help="Path to text file")
    args = parser.parse_args()

    stats = FileStats(args.path).count()
    print({"path": stats.path, "lines": stats.lines, "words": stats.words, "chars": stats.chars})
