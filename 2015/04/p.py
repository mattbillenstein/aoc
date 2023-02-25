#!/usr/bin/env pypy3

import hashlib
import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines[0]

def part1(data, num=5):
    i = 0
    find = '0' * num
    while 1:
        s = data + str(i)
        b = s.encode('utf8')
        x = hashlib.md5(b).hexdigest()
        if x[:num] == find:
            break
        i += 1

    print(i)

def part2(data):
    part1(data, 6)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
