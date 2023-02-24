#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines[0]

def part1(data):
    x = y = 0
    visited = set()
    visited.add((x, y))
    for c in data:
        if c == '^':
            y -= 1
        elif c == 'v':
            y += 1
        elif c == '<':
            x -= 1
        elif c == '>':
            x += 1
        visited.add((x, y))

    print(len(visited))

def part2(data):
    x = y = 0
    rx = ry = 0
    visited = set()
    visited.add((x, y))

    for i, c in enumerate(data):
        if i % 2 == 0:
            if c == '^':
                y -= 1
            elif c == 'v':
                y += 1
            elif c == '<':
                x -= 1
            elif c == '>':
                x += 1
            visited.add((x, y))
        else:
            if c == '^':
                ry -= 1
            elif c == 'v':
                ry += 1
            elif c == '<':
                rx -= 1
            elif c == '>':
                rx += 1
            visited.add((rx, ry))

    print(len(visited))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
