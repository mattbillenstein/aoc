#!/usr/bin/env pypy3

import sys

from intcode import run

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return [int(_) for _ in lines[0].split(',')]

def part1(mem):
    for x in run(mem, [1]):
        print(x)

def part2(mem):
    for x in run(mem, [2]):
        print(x)

def test(mem):
    for v in run(mem):
        print(v)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)
    if 'test' in sys.argv:
        test(data)

if __name__ == '__main__':
    main()
