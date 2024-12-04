#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines

def part1(data):
    def pluck(d, pt, dx, dy):
        s = d[pt]
        for i in range(3):
            pt = (pt[0] + dx, pt[1] + dy)
            s += d.get(pt, '.')
        return s
    
    ys = range(len(data))
    xs = range(len(data[0]))

    d = {}
    for x in xs:
        for y in ys:
            d[(x, y)] = data[y][x]

    cnt = 0
    for x in xs:
        for y in ys:
            pt = (x, y)
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == dy == 0:
                        continue
                    if pluck(d, pt, dx, dy) == "XMAS":
                        cnt += 1

    print(cnt)

def part2(data):
    tokens = ("MAS", "SAM")
    def pluck_x(d, pt):
        x, y = pt
        s1 = d.get((x-1, y-1), '') + d[pt] + d.get((x+1, y+1), '')
        s2 = d.get((x-1, y+1), '') + d[pt] + d.get((x+1, y-1), '')
        return s1 in tokens and s2 in tokens
    
    ys = range(len(data))
    xs = range(len(data[0]))

    d = {}
    for x in xs:
        for y in ys:
            d[(x, y)] = data[y][x]

    cnt = 0
    for x in xs:
        for y in ys:
            pt = (x, y)
            if pluck_x(d, pt):
                cnt += 1

    print(cnt)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
