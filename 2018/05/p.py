#!/usr/bin/env pypy3

import itertools
import math
import string
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
#    lines = [int(_) for _ in lines]
    return lines[0]

def react(data):
    while 1:
        remove = []
        for i in range(len(data)-1):
            if data[i].lower() == data[i+1].lower() and data[i] != data[i+1]:
                if not (remove and remove[-1] == i-1):
                    remove.append(i)

        if not remove:
            break

        remove.reverse()

        for i in remove:
            data = data[:i] + data[i+2:]

    return len(data)

def part1(data):
    print(react(data))

def part2(data):
    mn = sys.maxsize

    for c in string.ascii_lowercase:
        s = ''.join(_ for _ in data if _.lower() != c)
        x = react(s)
        if x < mn:
            mn = x
        
    print(mn)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
