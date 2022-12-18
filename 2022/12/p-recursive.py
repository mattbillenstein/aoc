#!/usr/bin/env python3

import sys
import time

last = time.time()

letters = 'SabcdefghijklmnopqrstuvwxyzE'

START = letters.index('S')
END = letters.index('E')

def print_grid(grid):
    for row in grid:
        print(''.join(letters[_] for _ in row))


def print_path(path, sizex, sizey):
    for y in range(sizey):
        s = ''
        for x in range(sizex):
            s += ''.join(path.get((x, y), '.'))
        print(s)


def walk(grid, path, x, y):
    global last

    now = time.time()
    if now - last > 10:
        last = now
        print("\033c", end='')
        print(len(path))
        print_path(path, len(grid[0]), len(grid))

    height = grid[y][x]
    if height == END:
        d = dict(path)
        d[(x, y)] = 'E'
        return [d]

    paths = []
    for newx, newy, dir in [(x-1, y, '<'), (x+1, y, '>'), (x, y-1, '^'), (x, y+1, 'v')]:
        if (newx, newy) in path or newx < 0 or newy < 0 or newx >= len(grid[0]) or newy >= len(grid):
            continue

        if (grid[newy][newx] - height) > 1:
            continue

        path[(x, y)] = dir
        path[(newx, newy)] = '.'
        paths += walk(grid, path, newx, newy)
        path.pop((newx, newy))

    return paths


def main(argv):
    with open(argv[1]) as f:
        lines = [_.strip('\r\n') for _ in f]

    grid = []
    for y, line in enumerate(lines):
        row = [letters.index(c) for c in line]
        grid.append(row)
        if START in row:
            startpt = (row.index(START), y)
        if END in row:
            endpt = (row.index(END), y)

    print(startpt, endpt)

    print_grid(grid)

    paths = walk(grid, {startpt: 'S'}, startpt[0], startpt[1])
    paths.sort(key=lambda x: len(x))

    print()
    print(len(paths))

    for path in paths:
        print()
        print(len(path)-1, path)
        print_path(path, len(grid[0]), len(grid))


if __name__ == '__main__':
    main(sys.argv)
