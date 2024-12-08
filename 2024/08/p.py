#!/usr/bin/env pypy3

import sys

from collections import defaultdict

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines

def part1(data):
    nodes = defaultdict(list)
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            if c != '.':
                nodes[c].append((x, y))

    maxy = len(data)
    maxx = len(data[0])

    antinodes = set()
    for k, L in nodes.items():
        for a in L:
            for b in L:
                if a == b:
                    continue

                if a[0] > b[0]:
                    dx = a[0] - b[0]
                    an0x = a[0] + dx
                    an1x = b[0] - dx
                else:
                    dx = b[0] - a[0]
                    an1x = b[0] + dx
                    an0x = a[0] - dx

                if a[1] > b[1]:
                    dy = a[1] - b[1]
                    an0y = a[1] + dy
                    an1y = b[1] - dy
                else:
                    dy = b[1] - a[1]
                    an1y = b[1] + dy
                    an0y = a[1] - dy

                if 0 <= an0x < maxx and 0 <= an0y < maxy:
                    antinodes.add((an0x, an0y))
                if 0 <= an1x < maxx and 0 <= an1y < maxy:
                    antinodes.add((an1x, an1y))

    print(len(antinodes))

def part2(data):
    nodes = defaultdict(list)
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            if c != '.':
                nodes[c].append((x, y))

    maxy = len(data)
    maxx = len(data[0])

    antinodes = set()
    for k, L in nodes.items():
        for a in L:
            for b in L:
                if a == b:
                    continue

                dx = a[0] - b[0]
                dy = a[1] - b[1]

                ptx, pty = a
                while 0 <= ptx < maxx and 0 <= pty < maxy:
                    antinodes.add((ptx, pty))
                    ptx += dx
                    pty += dy

                ptx, pty = a
                while 0 <= ptx < maxx and 0 <= pty < maxy:
                    antinodes.add((ptx, pty))
                    ptx -= dx
                    pty -= dy

    # 1426 too high
    print(len(antinodes))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
