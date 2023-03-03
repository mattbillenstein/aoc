#!/usr/bin/env pypy3

import sys
def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return [_.split() for _ in lines]

def part1(data):
    print(sum(1 for _ in data if len(_) == len(set(_))))

def part2(data):
    data = [[''.join(sorted(_)) for _ in line] for line in data]
    print(sum(1 for _ in data if len(_) == len(set(_))))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
