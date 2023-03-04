#!/usr/bin/env pypy3

import sys
import time
from collections import defaultdict
from pprint import pprint

DEBUG = sys.argv.count('-v')

CHARS = '.#@'
CLEAR = CHARS.index('.')
NOT_PLACED = CHARS.index('@')
PLACED = CHARS.index('#')
LEFT = '<'
RIGHT = '>'

shapes = [
#   ####
    {
        (0, 0): 1, (1, 0): 1, (2, 0): 1, (3, 0): 1,
    },

#   .#.
#   ###
#   .#.
    {
        (0, 2): 0, (1, 2): 1, (2, 2): 0,
        (0, 1): 1, (1, 1): 1, (2, 1): 1,
        (0, 0): 0, (1, 0): 1, (2, 0): 0,
    },

#   ..#
#   ..#
#   ###
    {
        (0, 2): 0, (1, 2): 0, (2, 2): 1,
        (0, 1): 0, (1, 1): 0, (2, 1): 1,
        (0, 0): 1, (1, 0): 1, (2, 0): 1,
    },

#   #
#   #
#   #
#   #
    {
        (0, 3): 1,
        (0, 2): 1,
        (0, 1): 1,
        (0, 0): 1,
    },

#   ##
#   ##
    {
        (0, 1): 1, (1, 1): 1,
        (0, 0): 1, (1, 0): 1,
    },
]

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines[0]

def print_grid(grid):
    do_print = False
    for y in range(len(grid)-1, -1, -1):
        if any(grid[y]) or y < 3:
            do_print = True
        row = f'{y:<8}|' + ''.join(CHARS[_] for _ in grid[y]) + '|'
        if do_print:
            print(row)
    print('        +-------+')

def paint(x, y, rock, grid, override=None):
    for pt, v in rock.items():
        if v:
            if override is not None:
                v = override
            grid[y+pt[1]][x+pt[0]] = v

def collides(x, y, rock, grid):
    for pt, v in rock.items():
        newx = x + pt[0]
        if not 0 <= newx < len(grid[0]):
            return True

        newy = y + pt[1]
        if not 0 <= newy < len(grid):
            return True

        if v and grid[newy][newx] == PLACED:
            return True

    return False

def part1(JETS):
    grid = [[0] * 7 for _ in range(10000)]

    rocks = 0
    jets = 0
    step = 0
    height = 0

    while rocks < 2022:
        x, y = 2, height+3
        rock = dict(shapes[rocks % len(shapes)])
        rocks += 1

        paint(x, y, rock, grid, NOT_PLACED)

        while 1:
            jet = JETS[jets % len(JETS)]
            jets += 1

            dx = 1 if jet == RIGHT else -1
            if not collides(x + dx, y, rock, grid):
                paint(x, y, rock, grid, CLEAR)
                x += dx
                paint(x, y, rock, grid, NOT_PLACED)

            if collides(x, y-1, rock, grid):
                paint(x, y, rock, grid, PLACED)

                # can place the piece lower than the existing height...
                newheight = y + max(_[1] for _ in rock) + 1
                if newheight > height:
                    height = newheight

                break
            else:
                paint(x, y, rock, grid, CLEAR)
                y -= 1
                paint(x, y, rock, grid, NOT_PLACED)

    if DEBUG:
        print_grid(grid)

    print(height)

def find_run(grid, height):
    max_run = 0
    y_run = None
    for y1 in range(height):
        y2 = y1 + 1

        row1 = grid[y1]
        while y2 < height:
            row2 = grid[y2]
            if row1 == row2:
                break
            y2 += 1

        tmp = (y1, y2)
        run = 0
        while y1 < height and y2 < height:
            row1 = grid[y1]
            row2 = grid[y2]
#            print(y1, y2, row1, row2)
            if row1 != row2:
                break
            run += 1
            y1 += 1
            y2 += 1

        if run > max_run:
            max_run = run
            y_run = tmp
#            print(y_run, max_run)

            # if we run off the end, that's fine, but after 10k, stop
            # looking...
            if max_run > 100000:
                break

    return y_run, max_run

def part2(JETS):
    grid = [[0] * 7 for _ in range(10_000)]

    rocks = 0
    jets = 0
    step = 0
    height = 0

    height_rock = {}
    rock_height = {}

    while height < len(grid) - 10:
        x, y = 2, height+3
        rock = dict(shapes[rocks % len(shapes)])
        rocks += 1

        paint(x, y, rock, grid, NOT_PLACED)

        while 1:
            jet = JETS[jets % len(JETS)]
            jets += 1

            dx = 1 if jet == RIGHT else -1
            if not collides(x + dx, y, rock, grid):
                paint(x, y, rock, grid, CLEAR)
                x += dx
                paint(x, y, rock, grid, NOT_PLACED)

            if collides(x, y-1, rock, grid):
                paint(x, y, rock, grid, PLACED)

                # can place the piece lower than the existing height...
                newheight = y + max(_[1] for _ in rock) + 1
                if newheight > height:
                    height = newheight

                break
            else:
                paint(x, y, rock, grid, CLEAR)
                y -= 1
                paint(x, y, rock, grid, NOT_PLACED)

        height_rock[height] = rocks
        rock_height[rocks] = height

    y_run, max_run = find_run(grid, height)
#    print(y_run, max_run)

    ya, yb = y_run
    while ya not in height_rock:
        ya += 1
        yb += 1

    ra = height_rock[ya]
    rb = height_rock[yb]
    rocks_per_segment = rb - ra
    lines_per_segment = yb - ya

    target_rocks = 1_000_000_000_000

    tsegments = (target_rocks - ra) // rocks_per_segment
    trocks = tsegments * rocks_per_segment + ra
    theight = ya + tsegments * lines_per_segment
#    print(trocks, theight)

    # recompute from a new starting point where we end cleanly at target height
    rocks_left = target_rocks - trocks
    ra = ra + rocks_left
    ya = rock_height[ra]

    tsegments = (target_rocks - ra) // rocks_per_segment
    trocks = tsegments * rocks_per_segment + ra
    theight = ya + tsegments * lines_per_segment
#    print(trocks)
    print(theight)

def main(argv):
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main(sys.argv)
