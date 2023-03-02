#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]

    L = []
    for line in lines:
        a, _, b = line.split()
        a = tuple([int(_) for _ in a.split(',')])
        b = tuple([int(_) for _ in b.split(',')])
        L.append((a, b))
    return L

def part(data, skip_diagonals=True):
    minx = min(min(_[0][0], _[1][0]) for _ in data)
    maxx = max(max(_[0][0], _[1][0]) for _ in data) + 1
    miny = min(min(_[0][1], _[1][1]) for _ in data)
    maxy = max(max(_[0][1], _[1][1]) for _ in data) + 1

    grid = [[0] * maxx for _ in range(maxy)]

    for a, b in data:
        if skip_diagonals and a[0] != b[0] and a[1] != b[1]:
            continue

        dx = 1 if b[0] > a[0] else -1 if b[0] < a[0] else 0
        dy = 1 if b[1] > a[1] else -1 if b[1] < a[1] else 0
        x, y = a
        grid[y][x] += 1
        while (x, y) != b:
            x += dx
            y += dy
            grid[y][x] += 1
        
#    print('-' * len(grid[0]))
    cnt = 0
    for line in grid:
#        print(''.join(' ' if not _ else str(_) for _ in line))
        cnt += sum([1 if _ > 1 else 0 for _ in line])
#    print('-' * len(grid[0]))

    print(cnt)

def main(argv):
    data = parse_input()

    part(data)
    part(data, False)

if __name__ == '__main__':
    main(sys.argv)
