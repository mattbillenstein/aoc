#!/usr/bin/env pypy3

import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    lines = [int(_) for _ in lines]
    return lines

def part1(data):
    print(sum(_ // 3 - 2 for _ in data))

def part2(data):
    tot = 0
    for module in data:
        fuel = module // 3 - 2
        while fuel > 0:
            debug(fuel)
            tot += fuel
            fuel = fuel // 3 - 2

    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
