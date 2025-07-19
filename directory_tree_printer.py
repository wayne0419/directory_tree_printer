#!/usr/bin/env python3
import os
import sys
import fnmatch
import argparse

def load_ignore_patterns(ignore_file):
    patterns = []
    with open(ignore_file, 'r') as f:
        for line in f:
            line = line.strip()
            # ignore empty lines or comments
            if not line or line.startswith('#'):
                continue
            patterns.append(line)
    return patterns

def should_ignore(path, patterns):
    """Decide whether to ignore this file/directory based on patterns"""
    name = os.path.basename(path)
    for pat in patterns:
        if fnmatch.fnmatch(path, pat) or fnmatch.fnmatch(name, pat):
            return True
    return False

def tree(dir_path, patterns, prefix=''):
    """Recursively print the directory tree"""
    try:
        entries = sorted(os.listdir(dir_path))
    except PermissionError:
        return

    entries = [e for e in entries if not should_ignore(os.path.join(dir_path, e), patterns)]
    count = len(entries)
    for idx, entry in enumerate(entries):
        path = os.path.join(dir_path, entry)
        is_last = (idx == count - 1)
        branch = '└── ' if is_last else '├── '
        print(f"{prefix}{branch}{entry}")
        if os.path.isdir(path):
            extension = '    ' if is_last else '│   '
            tree(path, patterns, prefix + extension)

def main():
    parser = argparse.ArgumentParser(description="Print directory tree, filtering items by ignore file")
    parser.add_argument('directory', help='Root directory path to print')
    parser.add_argument('ignore_file', help='File containing ignore patterns (like .gitignore)')
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory.", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(args.ignore_file):
        print(f"Error: ignore file {args.ignore_file} not found.", file=sys.stderr)
        sys.exit(1)

    patterns = load_ignore_patterns(args.ignore_file)
    # print the root directory
    root_name = os.path.basename(os.path.abspath(args.directory.rstrip('/')))
    print(f"{root_name}/")
    # print the tree of its contents
    tree(args.directory, patterns, prefix='')

if __name__ == '__main__':
    main()

# Usage:
# python3 directory_tree_printer.py <directory path> <ignore file path>