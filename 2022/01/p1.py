#!/usr/bin/env python3

import sys
from collections import defaultdict

def main(argv):
    elves = defaultdict(int)
    i = 0

    with open(argv[1]) as f:
        for line in f:
            line = line.strip()
            if not line:
                i += 1
                continue
            elves[i] += int(line)

    elves = list(elves.items())
    elves.sort(key=lambda x: x[1])

    print(len(elves), elves[-1])

    # part two, sum of top 3
    print(elves[-3:])
    print(sum(_[1] for _ in elves[-3:]))

if __name__ == '__main__':
    main(sys.argv)
