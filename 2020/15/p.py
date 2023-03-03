#!/usr/bin/env pypy3

import sys
from collections import defaultdict

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return [int(_) for _ in lines[0].split(',')]

def run(numbers, end):
    spoken = defaultdict(list)
    for i, n in enumerate(numbers):
        spoken[n].append(i+1)

    last = n
    for i in range(len(spoken)+1, end+1):
        debug(last, i, spoken)
        if len(spoken[last]) == 1:
            n = 0
        else:
            n = spoken[last][-1] - spoken[last][-2]
            
        spoken[n].append(i)
        last = n

    print(n)

def part1(numbers):
    run(numbers, 2020)
    
def part2(numbers):
    run(numbers, 30_000_000)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
