#!/usr/bin/env pypy3

import math
import sys
import time
from collections import defaultdict
from pprint import pprint

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    lines = [int(_) for _ in lines]
    return lines

def part1(adapters):
    # I don't see the difficulty in this part - just take them sorted no?
    device = 3 + max(adapters)

    adapters = [0] + sorted(adapters) + [device]
    debug(adapters)

    diff = defaultdict(int)
    for i in range(0, len(adapters)):
        diff[adapters[i] - adapters[i-1]] += 1

    print(diff[1] * diff[3])

def part2(adapters):
    # I guess if the delta between adapters is < 3, we can potentially drop
    # adapters?

    device = 3 + max(adapters)
    adapters = [0] + sorted(adapters) + [device]

    removes = []

    for i in range(len(adapters)-2):
        remove = []
        for j in range(i+1, len(adapters)-1):
            if (adapters[j+1] - adapters[i]) <= 3:
                remove.append(j)
            else:
                break

        if remove:
            if not removes:
                removes.append(remove)
            else:
                if remove[0] == removes[-1][-1]:
                    removes[-1].extend([_ for _ in remove if _ not in removes[-1]])
                else:
                    removes.append(remove)

    cnt = 1
    for remove in removes:
        if len(remove) == 3:
            cnt *= 7   # 3 take 2 + 3 take 1 + 1
        elif len(remove) == 2:
            cnt *= 4   # remove none, one or the other, or both 
        elif len(remove) == 1:
            cnt *= 2
        else:
            assert 0, remove
        
    print(cnt)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
