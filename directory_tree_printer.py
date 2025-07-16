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
            # 忽略空行或註解
            if not line or line.startswith('#'):
                continue
            patterns.append(line)
    return patterns

def should_ignore(path, patterns):
    """根據 patterns 判斷是否要忽略此檔案/目錄"""
    # 只用最後一級的名稱來比對，也可以改成比對整個相對路徑
    name = os.path.basename(path)
    for pat in patterns:
        if fnmatch.fnmatch(path, pat) or fnmatch.fnmatch(name, pat):
            return True
    return False

def tree(dir_path, patterns, prefix=''):
    """遞迴列印樹狀結構"""
    # 取得該目錄下所有項目，並排序
    try:
        entries = sorted(os.listdir(dir_path))
    except PermissionError:
        return

    # 過濾掉被忽略的
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
    parser = argparse.ArgumentParser(description="列印目錄樹，並根據 ignore 檔案過濾項目")
    parser.add_argument('directory', help='要列印的根目錄路徑')
    parser.add_argument('ignore_file', help='包含 ignore 模式的檔案 (類似 .gitignore)')
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"錯誤：{args.directory} 不是一個有效的目錄。", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(args.ignore_file):
        print(f"錯誤：{args.ignore_file} 找不到。", file=sys.stderr)
        sys.exit(1)

    patterns = load_ignore_patterns(args.ignore_file)
    # 列印根節點
    root_name = os.path.basename(os.path.abspath(args.directory.rstrip('/')))
    print(f"└── {root_name}/")
    tree(args.directory, patterns, prefix='    ')

if __name__ == '__main__':
    main()


# Usage:
# python3 directory_tree_printer.py <directory path> <ignore file path>