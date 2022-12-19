#!/usr/bin/env pypy3

import sys
import time
from collections import defaultdict
from pprint import pprint

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return [int(_) for _ in lines[0].split(',')]

def part(fish, days=80):
    d = defaultdict(int)
    for f in fish:
        d[f] += 1

    for i in range(days):
        newd = defaultdict(int)
        for age, cnt in d.items():
            if age == 0:
                newd[6] += cnt
                newd[8] += cnt
            else:
                newd[age-1] += cnt
        d = newd

    print(sum(d.values()))

def main(argv):
    data = parse_input()

    part(data)
    part(data, days=256)

if __name__ == '__main__':
    main(sys.argv)
