# week4/file_counter.py

def count_file(path):
    lines = 0
    words = 0
    chars = 0
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                lines += 1
                words += len(line.split())
                chars += len(line)
        return {"path": path, "lines": lines, "words": words, "chars": chars}
    except FileNotFoundError:
        print(f"Error: File not found -> {path}")
        return None
    except PermissionError:
        print(f"Error: Permission denied -> {path}")
        return None

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Count file statistics")
    parser.add_argument("path", help="Path to text file")
    args = parser.parse_args()

    stats = count_file(args.path)
    if stats:
        print(stats)
