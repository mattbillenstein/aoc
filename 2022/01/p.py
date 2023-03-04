#!/usr/bin/env pypy3

import sys
from collections import defaultdict

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    elves = defaultdict(int)
    i = 0
    for line in lines:
        if not line:
            i += 1
            continue
        elves[i] += int(line)
    return elves

def part(elves):
    elves = list(elves.items())
    elves.sort(key=lambda x: x[1])

    # part 1
    print(elves[-1][1])

    # part 2, sum of top 3
#    print(elves[-3:])
    print(sum(_[1] for _ in elves[-3:]))

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
