#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return [int(_) for _ in lines[0]]

def part1(data):
    tot = 0
    for i, v in enumerate(data):
        idx = (i+1) % len(data)
        if v == data[idx]:
            tot += v
    print(tot)

def part2(data):
    tot = 0
    for i, v in enumerate(data):
        idx = (i + len(data) // 2) % len(data)
        if v == data[idx]:
            tot += v
    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
