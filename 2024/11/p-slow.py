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
def expand(stone, N=25):
    stones = [stone]
    for i in range(N):
        L = []
        for stone in stones:
            L.extend(convert(stone))
        stones = L
    return stones

def part1(stones):
    tot = 0
    for stone in stones:
        tot += len(expand(stone, 25))
    print(tot)

def part2(stones):
    tot = 0
    # interesting, 25/25/25 - about 5.5m
    #              15/30/30 - about 1.1m
    #              30/30/15 - hours
    for stone in stones:
        for stone1 in expand(stone, 15):
            for stone2 in expand(stone1, 30):
                tot += len(expand(stone2, 30))
    print(tot)
                    
def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
