#!/usr/bin/env python3

import sys

DEBUG = sys.argv.count('-v')

AIR = '.'
ROCK = '#'
SAND = 'o'

FAUCET = (500, 0)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]

    walls = []
    for line in lines:
        points = [tuple(int(x) for x in _.split(',')) for _ in line.split(' -> ')]
        for i in range(1, len(points)):
            wall = (points[i-1], points[i])
            walls.append(wall)

    return walls

def print_grid(grid, xs, ys):
    for y in range(*ys):
        s = ''
        for x in range(*xs):
            s += grid.get((x, y), AIR)
        print(''.join(s))

def count_sand(grid):
    return len([_ for _ in grid.values() if _ == SAND])

def move(grid, pt, maxy):
    for newpt in [(pt[0], pt[1]+1), (pt[0]-1, pt[1]+1), (pt[0]+1, pt[1]+1)]:
        x = grid.get(newpt)
        if not x:
            grid[newpt] = grid.pop(pt)
            return newpt

    return pt

def part(walls, part):
    grid = {}
    for w in walls:
        xs = sorted([_[0] for _ in w])
        ys = sorted([_[1] for _ in w])

        for x in range(xs[0], xs[1] + 1):
            for y in range(ys[0], ys[1] + 1):
                grid[(x, y)] = ROCK

    xs = [min(_[0] for _ in grid)-10, max(_[0] for _ in grid)+10]
    ys = [0, max(_[1] for _ in grid)+2]
    maxy = ys[1]-1

    if DEBUG:
        print(maxy)
        print(xs, ys)

    finished = False
    i = 0
    while not finished:
        i += 1
        if grid.get(FAUCET) == SAND:
            break

        pt = FAUCET
        grid[FAUCET] = SAND

        while 1:
            newpt = move(grid, pt, maxy)
            if newpt[0] < xs[0]:
                xs[0] = newpt[0] - 5
            elif newpt[0] > xs[1]:
                xs[1] = newpt[0] + 5

            if part == 1 and newpt[1] > maxy:
                # part1 - falls off bottom
                grid.pop(newpt)
                finished = True
                break

            # part2 - change to 0 for part1
            if part == 2 and newpt[1] == maxy:
                break

            # come to rest
            if newpt == pt:
                break

            pt = newpt

        if DEBUG and i % 100 == 0:
            print()
            print_grid(grid, xs, ys)
            print(count_sand(grid))

    if DEBUG:
        print()
        print_grid(grid, xs, ys)

    print(count_sand(grid))


def main():
    data = parse_input()
    if '1' in sys.argv:
        part(data, 1)
    if '2' in sys.argv:
        part(data, 2)

if __name__ == '__main__':
    main()
