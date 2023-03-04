#!/usr/bin/env python3

import hashlib
import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines[0]

def part1(salt, stretch=False):
#    salt = 'abc'
    hashes = []
    for i in range(50_000):
        s = salt + str(i)
        h = hashlib.md5(s.encode('utf8')).hexdigest()
        if stretch:
            for _ in range(2016):
                h = hashlib.md5(h.encode('utf8')).hexdigest()
        hashes.append(h)

    cnt = 0
    for i, h in enumerate(hashes):
        c3 = None
        for ci in range(len(h)-2):
            if h[ci] == h[ci+1] == h[ci+2]:
                c3 = h[ci]
                for h2 in hashes[i+1:i+1001]:
                    if c3*5 in h2:
                        cnt += 1
                        if cnt == 64:
                            print(i)
                break

        if cnt >= 64:
            break

def part2(data):
    part1(data, stretch=True)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
