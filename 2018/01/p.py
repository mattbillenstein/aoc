#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    lines = [int(_) for _ in lines]
    return lines

def part1(data):
    print(sum(data))

def part2(data):
    visited = set()
    i = 0
    freq = 0
    while 1:
        if freq in visited:
            break
        visited.add(freq)
        freq += data[i % len(data)]
        i += 1

    print(freq)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
