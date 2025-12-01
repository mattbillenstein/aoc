#!/usr/bin/env pypy3

import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    lines = [(_[0], int(_[1:])) for _ in lines]
    return (lines,)

def part1(data):
    code = 0
    x = 50
    for dir, n in data:
        if dir == 'L':
            n = -n
        x += n
        x %= 100
        if x == 0:
            code += 1
    print(code)

def part2(data):
    code = 0
    x = 50
    for dir, n in data:
        code += n // 100
        n %= 100

        if dir == 'L':
            n = -n

        # don't count crossing if already on zero
        if x != 0:
            # n=3, x=97 - lands on 0, don't count - counted below
            # n=4, x=91 - lands on 1, crossed 0, count
            if n > 0 and (x + n) > 100:
                debug('>', x, n)
                code += 1

            # n=-3, x=3 - lands on 0, don't count - counted below
            # n=-4, x=3 - lands on 99, crossed 0, count
            elif n < 0 and x != 0 and (x + n) < 0:
                debug('<', x, n)
                code += 1

        x += n
        x %= 100
        if x == 0:
            code += 1

    print(code)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
