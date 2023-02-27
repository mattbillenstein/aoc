#!/usr/bin/env pypy3

import json
import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return json.loads(lines[0])

def nums(o, nored=False):
    L = []
    if isinstance(o, int):
        L.append(o)
    elif isinstance(o, list):
        for item in o:
            L += nums(item, nored)
    elif isinstance(o, dict):
        if not nored or 'red' not in o.values():
            for item in o.values():
                L += nums(item, nored)
    return L

def part1(data):
    print(sum(_ for _ in nums(data)))

def part2(data):
    print(sum(_ for _ in nums(data, True)))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
