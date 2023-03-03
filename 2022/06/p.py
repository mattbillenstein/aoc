#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines[0]

def part(data, num):
    i, j = 0, num
    while len(set(data[i:j])) != num:
        i += 1
        j += 1

    print(j)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part(data, 4)
    if '2' in sys.argv:
        part(data, 14)

if __name__ == '__main__':
    main()
