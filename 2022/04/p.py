#!/usr/bin/env pypy3

import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    data = []
    for line in lines:
        a, b = line.split(',')
        a1, a2 = [int(_) for _ in a.split('-')]
        b1, b2 = [int(_) for _ in b.split('-')]
        data.append(((a1, a2), (b1, b2)))
    return data

def part(data):
    cnt = 0
    cnt2= 0
    for a, b in data:
        a1, a2 = a
        b1, b2 = b

        # a contains b or b contains a
        if b1 >= a1 and b2 <= a2 or a1 >= b1 and a2 <= b2:
            cnt += 1

        # a and b overlap
        if b1 <= a1 <= b2 or b1 <= a2 <= b2 or a1 <= b1 <= a2 or a1 <= b2 <= a2:
            cnt2 += 1

    print(cnt)
    print(cnt2)

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
