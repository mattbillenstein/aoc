#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines[0]

def run(s):
    N = int(s)
    data = [3, 7]
    find = [int(_) for _ in s]

    a, b = 0, 1
    while 1:
        x = data[a] + data[b]
        debug(a, b, x, data)

        if x >= 10:
            data.append(x // 10)
            if data[-len(find):] == find:
                break
            data.append(x % 10)
            if data[-len(find):] == find:
                break
        else:
            data.append(x)
            if data[-len(find):] == find:
                break

        a = (a + data[a] + 1) % len(data)
        b = (b + data[b] + 1) % len(data)

    data = ''.join(str(_) for _ in data)

    print(data[N:N+10])

    idx = data.index(s)
    print(idx)

def main():
    data = parse_input()
    run(data)

if __name__ == '__main__':
    main()
