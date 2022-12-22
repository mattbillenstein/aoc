#!/usr/bin/env pypy3

import re
import sys
import time
from collections import defaultdict
from pprint import pprint

EMPTY = 0
TILE = 1
WALL = 2

class State:
    def __init__(self, x, y, dir, grid):
        self.x = x
        self.y = y
        self.dir = dir
        self.grid = grid

    def move(self):
        # move forward one space or stop if we hit a wall, or wrap if needed
        dx = dy = 0
        if self.dir == '>':
            dx = 1
        elif self.dir == '<':
            dx = -1
        elif self.dir == '^':
            dy = -1
        elif self.dir == 'v':
            dy = 1
        else:
            assert 0, self.dir

        while 1:
            nx = self.x
            ny = self.y
            while 1:
                nx += dx
                ny += dy
                ny = ny % len(self.grid)
                nx = nx % len(self.grid[0])
                v = self.grid[ny][nx]
                if v != EMPTY:
                    break

            if v == WALL:
                # we didn't move
                break
            elif v == TILE:
                self.x = nx
                self.y = ny
                break

            # else, empty, keep looping...
            self.x = nx
            self.y = ny

    def turn(self, dir):
        self.dir = {
            'R': {'>': 'v', 'v': '<', '<': '^', '^': '>'},
            'L': {'>': '^', '^': '<', '<': 'v', 'v': '>'},
        }[dir][self.dir]

    def password(self):
        return ((self.y+1) * 1000) + ((self.x+1) * 4) + '>v<^'.index(self.dir)

    def print(self):
        for y in range(len(self.grid)):
            s = ''
            for x in range(len(self.grid[y])):
                if self.x == x and self.y == y:
                    s += self.dir
                else:
                    s += ' .#'[self.grid[y][x]]
            print(s)

    def __repr__(self):
        return f'State({self.x}, {self.y}, {self.dir})'

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]

    gridx = max(len(_) for _ in lines[:-2])
    gridy = len(lines)-2
    grid = [[EMPTY] * gridx for _ in range(gridy)]
    for y, line in enumerate(lines[:-2]):
        for x, c in enumerate(line):
            n = EMPTY
            if c == '.':
                n = TILE
            elif c == '#':
                n = WALL
            grid[y][x] = n

    directions = re.findall('\d+|[LR]', lines[-1])
    directions = [int(_) if not _ in 'LR' else _ for _ in directions]
    
    return grid, directions

def part1(grid, directions):
    # move to start
    state = State(0, 0, '>', grid)
    if grid[0][0] == EMPTY:
        state.move()
#    state.print()

    for cmd in directions:
        if cmd in ('L', 'R'):
            state.turn(cmd)
        else:
            for i in range(cmd):
                state.move()

#        print()
#        print(i, cmd)
#        state.print()

    print(state)
#    state.print()
    print(state.password())

def main():
    grid, directions = parse_input()
    part1(grid, directions)

if __name__ == '__main__':
    main()
