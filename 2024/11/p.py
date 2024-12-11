#!/usr/bin/env pypy3

import sys
from functools import lru_cache

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return [int(_) for _ in lines[0].split()]

def convert(stone):
    if stone == 0:
        return (1,)
    elif len(s := str(stone)) % 2 == 0:
        idx = len(s) // 2
        return (int(s[:idx]), int(s[idx:]))
    else:
        return (stone * 2024,)

@lru_cache(maxsize=None)
def count(stone, N):
    if N == 0:
        return 1
    return sum(count(_, N-1) for _ in convert(stone))

def part(stones, N=25):
    tot = 0
    for stone in stones:
        tot += count(stone, N)
    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part(data, 25)
    if '2' in sys.argv:
        part(data, 75)

if __name__ == '__main__':
    main()
