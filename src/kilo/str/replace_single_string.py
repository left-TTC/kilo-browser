#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
replace_in_file.py

在指定文件中替换某个字符串或词组。
- 默认替换全部出现的位置
- 支持可选正则模式
- 返回替换次数
"""

import argparse
import re
from pathlib import Path
import sys


def replace_plain(text: str, old: str, new: str) -> int:
    """普通字符串替换"""
    count = text.count(old)
    if count == 0:
        return text, 0
    return text.replace(old, new), count


def replace_regex(text: str, pattern: str, replacement: str) -> int:
    """正则表达式替换"""
    return re.subn(pattern, replacement, text)


def replace_in_file(
    file_path: str,
    old: str,
    new: str,
    *,
    regex: bool = False,
    encoding: str = "utf-8"
) -> int:
    """
    在文件中执行替换

    :return: 替换次数
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    text = path.read_text(encoding=encoding)

    if regex:
        new_text, count = replace_regex(text, old, new)
    else:
        new_text, count = replace_plain(text, old, new)

    if count > 0:
        path.write_text(new_text, encoding=encoding)

    return count


def main():
    parser = argparse.ArgumentParser(
        description="在文件中替换字符串或词组（无备份）"
    )
    parser.add_argument("file", help="目标文件路径")
    parser.add_argument("old", help="要被替换的字符串 / 正则表达式")
    parser.add_argument("new", help="新字符串")
    parser.add_argument(
        "--regex",
        action="store_true",
        help="使用正则表达式替换"
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="文件编码(默认 utf-8)"
    )

    args = parser.parse_args()

    try:
        count = replace_in_file(
            args.file,
            args.old,
            args.new,
            regex=args.regex,
            encoding=args.encoding,
        )
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

    if count == 0:
        print("未找到需要替换的内容")
    else:
        print(f"替换完成，共替换 {count} 处")


if __name__ == "__main__":
    main()
