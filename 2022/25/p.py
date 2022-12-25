#!/usr/bin/env pypy3

import sys

ALPHABET = '=-012'
OFFSET = -2
BASE = len(ALPHABET)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines

def decode(snafu):
    x = 0
    for i, c in enumerate(reversed(snafu)):
        x += BASE**i * (ALPHABET.index(c) + OFFSET)
    return x

def encode(num):
    L = []
    while num:
        num, rem = divmod(num+2, BASE)
        L.append(ALPHABET[rem])
    return ''.join(reversed(L))

def part1(data):
    tot = 0
    for line in data:
        v = decode(line)
        s = encode(v)
        tot += v
#        print(line, v, s)
    print(encode(tot))

def main():
    data = parse_input()
    part1(data)

if __name__ == '__main__':
    main()
