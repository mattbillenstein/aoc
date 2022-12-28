#!/usr/bin/env pypy3

import sys
import time
from collections import defaultdict
from pprint import pprint

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines

def run(data):
    seats = []
    for line in data:
        bn = line.translate(line.maketrans('FBLR', '0101'))
        row, col = bn[:-3], bn[-3:]
        row = int(row, 2)
        col = int(col, 2)
        seat_id = row * 8 + col
        seats.append(seat_id)

    seats = set(seats)
    print(max(seats))

    for i in range(min(seats), max(seats)):
        if i not in seats:
            print(i)
            break

def main():
    data = parse_input()
    run(data)

if __name__ == '__main__':
    main()
