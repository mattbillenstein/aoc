#!/usr/bin/env python3

import math
import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    instr = lines[0]
    map = {}
    for line in lines[2:]:
        for c in '=(,)':
            line = line.replace(c, '')
        a, b, c = line.split()
        map[a] = (b, c)
    return instr, map

def part1(instr, map):
    pos = 'AAA'
    steps = 0
    while pos != 'ZZZ':
        pos = map[pos][0 if instr[steps % len(instr)] == 'L' else 1]
        steps += 1
    print(steps)

def part2(instr, map):
    pos = [_ for _ in map if _[2] == 'A']
    steps = []
    for p in pos:
        step = 0
        while p[2] != 'Z':
            p = map[p][0 if instr[step % len(instr)] == 'L' else 1]
            step += 1
        steps.append(step)
    print(math.lcm(*steps))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
