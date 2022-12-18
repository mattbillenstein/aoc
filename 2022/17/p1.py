#!/usr/bin/env pypy3

import sys
import time
from collections import defaultdict
from pprint import pprint

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

def parse_input(fname):
    with open(fname ) as f:
        lines = [_.strip('\r\n') for _ in f]
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

    print_grid(grid)
    print(height)

def main(argv):
    jets = parse_input(argv[1])

    part1(jets)

if __name__ == '__main__':
    main(sys.argv)
