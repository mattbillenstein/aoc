#!/usr/bin/env pypy3

import sys
from collections import defaultdict

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    rooms = []
    for line in lines:
        line = line.replace(']', '')
        room, x = line.rsplit('-', 1)
        sid, cksum = x.split('[')
        sid = int(sid)
        rooms.append((room, cksum, sid))
    return rooms

def part1(data):
    tot = 0
    valid = []
    for room, cksum, sid in data:
        d = defaultdict(int)
        for c in room:
            if c != '-':
                d[c] += 1
        L = sorted([(v, -ord(c)) for c, v in d.items()], reverse=True)
        s = ''.join([chr(-c) for v, c in L[:5]])
        if s == cksum:
            tot += sid
            valid.append((room, cksum, sid))
    print(tot)
    return valid

def rotate(s, sid):
    o = ''
    base = ord('a')
    for c in s:
        if c == '-':
            o += ' '
        else:
            rot = (ord(c) - base + sid) % 26
            o += chr(base + rot)
    return o

def part2(data):
    assert rotate('qzmt-zixmtkozy-ivhz', 343) == 'very encrypted name'

    valid = part1(data)
    for room, cksum, sid in valid:
        s = rotate(room, sid)
        if 'north' in s:
            print(sid)
            break

def main():
    data = parse_input()
    part2(data)

if __name__ == '__main__':
    main()
