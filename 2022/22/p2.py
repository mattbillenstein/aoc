#!/usr/bin/env pypy3

import re
import sys
import time
from collections import defaultdict
from pprint import pprint

EMPTY = 0
TILE = 1
WALL = 2

DEBUG = '--debug' in sys.argv

class State:
    def __init__(self, x, y, dir, grid):
        self.x = x
        self.y = y
        self.dir = dir
        self.grid = grid

    def move(self):
        # move forward one space or stop if we hit a wall
        nx, ny, nd = self.translate(self.x, self.y, self.dir)
        if DEBUG:
            print(nx, ny, nd)

        v = self.grid[ny][nx]

        if v == TILE:
            found = False
            self.x = nx
            self.y = ny
            self.dir = nd

    def turn(self, dir):
        self.dir = {
            'R': {'>': 'v', 'v': '<', '<': '^', '^': '>'},
            'L': {'>': '^', '^': '<', '<': 'v', 'v': '>'},
        }[dir][self.dir]

    def dx_dy_from_dir(self, dir):
        dx = dy = 0
        if dir == '>':
            dx = 1
        elif dir == '<':
            dx = -1
        elif dir == '^':
            dy = -1
        elif dir == 'v':
            dy = 1
        return dx, dy

    def translate(self, x, y, dir):
        # translate a given x, y, dir into a new x, y, dir in the flat grid,
        # but considering cube wrapping...
        size = len(self.grid) // 3

        if dir == '<' and y < size and x == size*2:
            # Wrap Up to Left
            return size + y, size, 'v'

        if dir == '^' and y == size and size <= x < size*2:
            # Wrap Left to Up
            return size*2, x-size, '>'

        if dir == '>' and y < size and x == size * 3 - 1:
            # Wrap Up to Right
            return size*4-1, size*3-1-y, '<'

        if dir == '>' and y >= size*2 and x == size*4 - 1:
            # Wrap Right to Up
            return size*3 - 1, (size*3-1 - y), '<'

        if dir == '^' and y == 0 and size*2 <= x < size*3:
            # wrap Up to Back
            return size*3-1-x, size, 'v'

        if dir == '^' and y == size and 0 <= x < size:
            # Wrap Back to Up
            return size*2 + (size-1-x), 0, 'v'

        if dir == '<' and size <= y < size*2 and x == 0:
            # Back to Right
            return size*4-1-(y-size), size*3-1, '^'

        if dir == 'v' and y == size*3-1 and size*3 <= x < size*4:
            # Right to Back
            return 0, size + size*4-1-x, '>'

        if dir == 'v' and y == size*2-1 and 0 <= x < size:
            # Back to Down
            return size*3-1-x, size*3-1, '^'

        if dir == 'v' and y == size*3-1 and size*2 <= x < size*3:
            # Down to Back
            return size*3-1-x, size*2-1, '^'

        if dir == '>' and size <= y < size*2 and x == size*3-1:
            # Front to Right
            return size*4-1-(y-size), size*2, 'v'

        if dir == '^' and y == size*2 and size*3 <= x < size*4:
            # Right to Front
            return size*3-1, size*2 - 1 - (x-size*3), '<'

        if dir == 'v' and y == size*2-1 and size <= x < size*2:
            # Left to Down
            return size*2, size*3-1-(x-size), '>'

        if dir == '<' and size*2 <= y < size*3 and x == size*2:
            # Down to Left
            return size*2-1-(y-size*2), size*2-1, '^'

        # no translation
        dx, dy = self.dx_dy_from_dir(dir)
        return x+dx, y+dy, dir

    def password(self):
        return ((self.y+1) * 1000) + ((self.x+1) * 4) + '>v<^'.index(self.dir)

    def print(self, full=False):
        yr = range(len(self.grid))
        xr = range(len(self.grid[0]))
        if not full:
            yr = range(max(0, self.y-20), min(self.y+20 + 1, len(self.grid)))
            xr = range(len(self.grid[0]))
            
        for y in yr:
            s = f'{y:3} '
            for x in xr:
                if self.x == x and self.y == y:
                    s += self.dir
                else:
                    s += ' .#'[self.grid[y][x]]
            print(s)
        s = '    '
        for i in range(10, len(self.grid[0])+10, 10):
            s += f'{i:10}'
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

    assert ''.join(str(_) for _ in directions) == lines[-1]
    
    return grid, directions

def part2(grid, directions):
    # sigh, they've unfolded differently than in the test...

    # test is
    #   U
    # BLF
    #   DR

    # input is
    #  UR
    #  F
    # LD
    # B

    # WTF!
    
    # UFD are in the right spots, just shifted, lets just permute the other
    # sides to match the test...

    if len(grid) > 100:
        size = len(grid) // 4

        newgrid = [[0] * size * 4 for _ in range(size*3)]

        # copy UFD unchanged
        for stride in (0, 1, 2):
            for y in range(size*stride, size*(stride+1)):
                for x in range(size, size*2):
                    ny = y
                    assert size*stride <= ny < size*(stride+1), ny
                    nx = x+size
                    assert size*2 <= nx < size*3
                    newgrid[ny][nx] = grid[y][x]

        # copy L up rot CW
        for y in range(size*2, size*3):
            for x in range(0, size):
                ny = x+size
                assert size <= ny < size*2, ny
                nx = size-y-1 + size*3
                assert size <= nx < size*2
                newgrid[ny][nx] = grid[y][x]

    # test is
    #   U
    # BLF
    #   DR

    # input is
    #  UR
    #  F
    # LD
    # B

        # copy B up rot CW
        for y in range(size*3, size*4):
            for x in range(0, size):
                ny = x+size
                assert size <= ny < size*2, ny
                nx = size-y-1 + size*3
                assert 0 <= nx < size
                newgrid[ny][nx] = grid[y][x]

        # copy R down, flipY - duh!
        for y in range(0, size):
            for x in range(size*2, size*3):
                ny = size*3-y-1
                assert size*2 <= ny < size*3
                nx = size*6-x-1
                assert size*3 <= nx < size*4
                newgrid[ny][nx] = grid[y][x]

        grid = newgrid

        # FIXME, these translations need to be reversed on the way back!

    # move to start
    x = grid[0].index(TILE)
    state = State(x, 0, '>', grid)
    state.print(True)
    print(state)

    for cmd in directions:
        if cmd in ('L', 'R'):
            state.turn(cmd)
            if DEBUG:
                print()
                print(cmd)
                state.print()
                time.sleep(1)
        else:
            for i in range(cmd):
                state.move()
                if DEBUG:
                    print()
                    print(f'{i+1} / {cmd}')
                    state.print()
                    time.sleep(0.1)

    
#    state.print(True)
    state.print()
    print(state)
    print(state.password())

    # translate back to original coordinates
    state.x -= 50
    print(state)
    print(state.password())

def test(grid):
    state = State(0, 0, '>', grid)
    state.print()

    # Up to Left
    assert state.translate(8, 1, '<') == (5, 4, 'v')
    # Left to Up
    assert state.translate(5, 4, '^') == (8, 1, '>') 

    # Up to Right
    assert state.translate(11, 1, '>') == (15, 10, '<')
    # Right to Up
    assert state.translate(15, 10, '>') == (11, 1, '<')

    # Up to Back
    assert state.translate(9, 0, '^') == (2, 4, 'v')
    # Back to Up
    assert state.translate(2, 4, '^') == (9, 0, 'v')

    # Back to Right
    assert state.translate(0, 5, '<') == (14, 11, '^')
    # Right to Back
    assert state.translate(14, 11, 'v') == (0, 5, '>')

    # Back to Down
    assert state.translate(1, 7, 'v') == (10, 11, '^')
    # Down to Back
    assert state.translate(10, 11, 'v') == (1, 7, '^')

    # Front to Right
    assert state.translate(11, 5, '>') == (14, 8, 'v')
    # Right to Front
    assert state.translate(14, 8, '^') == (11, 5, '<') 

    # Left to Down
    assert state.translate(6, 7, 'v') == (8, 9, '>')
    # Down to Left
    assert state.translate(8, 9, '<') == (6, 7, '^') 


def main():
    grid, directions = parse_input()

    if len(grid) == 12:
        test(grid)

    part2(grid, directions)

if __name__ == '__main__':
    main()
