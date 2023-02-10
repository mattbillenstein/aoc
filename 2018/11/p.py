#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def find_max_power(grid_serial_number, size):
    mxpt = None
    mx = -sys.maxsize

    for x in range(1, 301 - size):
        for y in range(1, 301 - size):
            tot = 0
            for dx in range(x, x + size):
                for dy in range(y, y + size):
                    rack_id = dx + 10
                    power = rack_id * dy
                    power += grid_serial_number
                    power *= rack_id
                    power = power // 100 % 10
                    power -= 5

                    tot += power

            if tot > mx:
                mx = tot
                mxpt = (x, y)

    return mxpt, mx

def part1():
    grid_serial_number = 7400
    mxpt, mx = find_max_power(grid_serial_number, 3)
    print('%s,%s' % mxpt, mx)

def part2():
    grid_serial_number = 7400

    mxpt = None
    mx = -sys.maxsize
    mxsize = 1
    for size in range(1, 300):
        a, b = find_max_power(grid_serial_number, size)
        if b > mx:
            mx = b
            mxpt = a
            mxsize = size
            debug('%s,%s,%s' % (mxpt[0], mxpt[1], mxsize), mx)

    print('%s,%s,%s' % (mxpt[0], mxpt[1], mxsize), mx)

def main():
    if '1' in sys.argv:
        part1()
    if '2' in sys.argv:
        part2()

if __name__ == '__main__':
    main()
