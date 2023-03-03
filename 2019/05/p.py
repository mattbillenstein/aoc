#!/usr/bin/env pypy3

import sys

from intcode import run

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    mem = [int(_) for _ in lines[0].split(',')]
    return mem

def part1(mem):
    for x in run(mem, [1]):
        if x:
            print(x)

def part2(mem):
    for x in run(mem, [5]):
        if x:
            print(x)

def test(mem):
    for x in run(mem, [7]):
        print(x)
    print()
    for x in run(mem, [7]):
        print(x)
    print()
    for x in run(mem, [7]):
        print(x)

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
