#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    cmds = []
    for line in lines:
        line = line.replace(',', ' ').replace('turn ', '')
        L = line.split()
        cmds.append((L[0], (int(L[1]), int(L[2])), (int(L[4]), int(L[5]))))
    return cmds

def part1(cmds):
    g = [[0] * 1000 for _ in range(1000)]
    for cmd, pt1, pt2 in cmds:
        for y in range(pt1[1], pt2[1]+1):
            for x in range(pt1[0], pt2[0]+1):
                if cmd == 'on':
                    g[y][x] = 1
                elif cmd == 'off':
                    g[y][x] = 0
                elif cmd == 'toggle':
                    g[y][x] = 0 if g[y][x] else 1

    print(sum(sum(_) for _ in g))

def part2(cmds):
    g = [[0] * 1000 for _ in range(1000)]
    for cmd, pt1, pt2 in cmds:
        for y in range(pt1[1], pt2[1]+1):
            for x in range(pt1[0], pt2[0]+1):
                if cmd == 'on':
                    g[y][x] += 1
                elif cmd == 'off':
                    g[y][x] = max(0, g[y][x] - 1)
                elif cmd == 'toggle':
                    g[y][x] += 2

    print(sum(sum(_) for _ in g))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
