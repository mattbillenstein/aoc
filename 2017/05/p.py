#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return [int(_) for _ in lines]

def part1(data):
    ip = 0
    i = 0
    while 0 <= ip < len(data):
        i += 1
        tmp = ip
        ip += data[ip]
        data[tmp] += 1

    print(i)

def part2(data):
    ip = 0
    i = 0
    while 0 <= ip < len(data):
        i += 1
        tmp = ip
        ip += data[ip]
        if data[tmp] >= 3:
            data[tmp] -= 1
        else:
            data[tmp] += 1

    print(i)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(list(data))
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
