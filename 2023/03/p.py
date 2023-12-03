#!/usr/bin/env pypy3

import sys
from collections import defaultdict

def parse_input():
    return [_.strip('\r\n') for _ in sys.stdin]

def get(data, x, y):
    try:
        return data[y][x]
    except IndexError:
        pass

def part(data):
    numbers = '0123456789'
    num = ''
    include = False
    tot = 0
    gears = defaultdict(list)
    gear = None

    # walk through char by char building runs of numbers and looking at
    # adjacent characters for each digit for a gear or other symbol.
    for y in range(len(data)):
        # len + 1 to intentionally run off the end here and terminate num run...
        for x in range(len(data[y]) + 1):
            c = get(data, x, y)
            if c and c in numbers:
                # we found a digit, add it to num and look at neighboring cells
                num += c
                for y2 in (y-1, y, y+1):
                    for x2 in (x-1, x, x+1):
                        c2 = get(data, x2, y2)
                        if c2 and c2 not in numbers and c2 != '.':
                            include = True
                            if c2 == '*':
                                gear = (x2, y2)
            else:
                # At the end of a run of digits, check if we saw a gear or
                # other symbol and count it if so.
                if num:
                    if include:
                        tot += int(num)
                    if gear:
                        gears[gear].append(int(num))

                    num = ''
                    include = False
                    gear = None

    print(tot)

    tot = 0
    for gear, L in gears.items():
        if len(L) == 2:
            tot += L[0] * L[1]

    print(tot)

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
