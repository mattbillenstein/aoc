#!/usr/bin/env pypy3

import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return int(lines[0])

def power(gsn, x, y):
    rack_id = x + 10
    p = rack_id * y
    p += gsn
    p *= rack_id
    p = p // 100 % 10
    p -= 5
    return p

def find_max_power(grid_serial_number, size):
    mxpt = None
    mx = -sys.maxsize

    for x in range(1, 301 - size):
        tot = None
        for y in range(1, 301 - size):
            if tot is None:
                tot = 0
                for dx in range(x, x + size):
                    for dy in range(y, y + size):
                        tot += power(grid_serial_number, dx, dy)
            else:
                # subtract trailing edge, add leading edge
                for dx in range(x, x + size):
                    tot -= power(grid_serial_number, dx, y-1)
                    tot += power(grid_serial_number, dx, y + size-1)

            if tot > mx:
                mx = tot
                mxpt = (x, y)

    return mxpt, mx

def part1(grid_serial_number):
    mxpt, mx = find_max_power(grid_serial_number, 3)
    debug(mx)
    print('%s,%s' % mxpt)

def part2(grid_serial_number):
    mxpt = None
    mx = -sys.maxsize
    mxsize = 1
    for size in range(1, 300):
        pt, p = find_max_power(grid_serial_number, size)
        if p > mx:
            mx = p
            mxpt = pt
            mxsize = size
            debug('%s,%s,%s' % (mxpt[0], mxpt[1], mxsize), mx)

    print('%s,%s,%s' % (mxpt[0], mxpt[1], mxsize))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
