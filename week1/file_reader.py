import argparse

def count_file(path):
    lines = 0
    words = 0
    chars = 0
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            lines += 1
            words += len(line.split())
            chars += len(line)
    return lines, words, chars

def main():
    parser = argparse.ArgumentParser(description="Count file statistics")
    parser.add_argument("path", help="Path to text file")
    args = parser.parse_args()

    try:
        l, w, c = count_file(args.path)
        print(f"Lines: {l}, Words: {w}, Characters: {c}")
    except FileNotFoundError:
        print(f"Error: File not found -> {args.path}")
    except PermissionError:
        print(f"Error: Permission denied -> {args.path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        sys.argv.append("demo.txt")
    main()

