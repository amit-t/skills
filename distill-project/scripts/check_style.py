#!/usr/bin/env python3
"""Check text files against simple style rules before saving them.

Flags em dashes, banned words or phrases, and (optionally) markdown emphasis.
Lines that list the banned words themselves (for example "Never use: ...") are
skipped for the word check, so a rules file can carry its own ban list.

Usage:
  python check_style.py FILE [FILE ...] [--banned-file words.txt] [--banned "a,b,c"]
                        [--no-markdown] [--allow-en-dash]

words.txt holds one word or phrase per line; lines starting with # are ignored.
Exit code 0 when clean, 1 when anything is flagged.
"""
import argparse
import re
import sys

LIST_LINE = re.compile(r"^\s*[-*]?\s*(never use|avoid these words|banned words?)\s*:", re.I)


def load_banned(args):
    words = []
    if args.banned_file:
        with open(args.banned_file, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#"):
                    words.append(line)
    if args.banned:
        words += [w.strip() for w in args.banned.split(",") if w.strip()]
    return words


def check(path, banned, no_markdown, allow_en_dash):
    problems = []
    in_code = False
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    for n, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            in_code = not in_code
        if "\u2014" in line:
            problems.append((n, "em dash", line))
        if not allow_en_dash and "\u2013" in line:
            problems.append((n, "en dash", line))
        if banned and not LIST_LINE.match(line):
            for w in banned:
                if re.search(r"(?<![\w-])" + re.escape(w) + r"(?![\w-])", line, re.I):
                    problems.append((n, f"banned: {w}", line))
        if no_markdown and not in_code:
            if re.search(r"\*\*[^*]+\*\*|(?<![\w*])\*[^*\s][^*]*\*(?!\w)", line):
                problems.append((n, "markdown emphasis", line))
            if re.match(r"^\s{0,3}#{1,6}\s", line):
                problems.append((n, "markdown heading", line))
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--banned-file")
    ap.add_argument("--banned", help="comma-separated words or phrases")
    ap.add_argument("--no-markdown", action="store_true", help="flag **bold**, *italic* and # headings")
    ap.add_argument("--allow-en-dash", action="store_true")
    args = ap.parse_args()
    banned = load_banned(args)
    total = 0
    for path in args.files:
        found = check(path, banned, args.no_markdown, args.allow_en_dash)
        total += len(found)
        print(f"{path}: {len(found)} issue(s)")
        for n, kind, line in found:
            print(f"  line {n} [{kind}]: {line.strip()[:110]}")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
