import re

from config import DICT_FILE, CHARS


def load_dictionary():
    pat = re.compile(r"^[A-Za-z0-9]+$")
    seen = set()
    codes = []

    with open(DICT_FILE, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if line and line not in seen and pat.match(line):
                seen.add(line)
                codes.append(line)

    return codes


def brute_code_at(index, length):
    base = len(CHARS)
    chars = []
    for _ in range(length):
        chars.append(CHARS[index % base])
        index //= base
    return "".join(reversed(chars))


def total_combinations(length):
    return len(CHARS) ** length
