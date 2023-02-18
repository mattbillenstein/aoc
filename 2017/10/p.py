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

def part1(data):
    data = [int(_) for _ in data.split(',')]
    nums = list(range(256))
    pos = skip = 0
    size = len(nums)
    for length in data:
        nums = nums * 2
        nums[pos:pos+length] = reversed(nums[pos:pos+length])
        nums[:pos] = nums[size:size+pos]
        nums = nums[:size]
        pos = (pos + length + skip) % size
        skip += 1

    print(nums[0] * nums[1])

def xor(L):
    x = L[0]
    for y in L[1:]:
        x ^= y
    return x

def part2(data):
    data = [ord(_) for _ in data] + [17, 31, 73, 47, 23]
    nums = list(range(256))
    pos = skip = 0
    size = len(nums)
    for _ in range(64):
        for length in data:
            nums = nums * 2
            nums[pos:pos+length] = reversed(nums[pos:pos+length])
            nums[:pos] = nums[size:size+pos]
            nums = nums[:size]
            pos = (pos + length + skip) % size
            skip += 1

    L = [xor(nums[_:_+16]) for _ in range(0, len(nums), 16)]
    s = ''.join([f'{_:02x}' for _ in L])
    print(s)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
