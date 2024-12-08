#!/usr/bin/env pypy3

import itertools
import sys

def parse_input():
    L = []
    lines = [_.strip('\r\n') for _ in sys.stdin]
    nums = [
        [int(x) for x in _.replace(':', '').split()]
        for _ in lines
    ]
    return nums

def part1(data, ops=('+', '*')):
    tot = 0
    for L in data:
        test, nums = L[0], L[1:]
        for op in itertools.product(ops, repeat=len(nums)-1):
            v = nums[0]
            for x, o in zip(nums[1:], op):
                if o == '+':
                    v += x
                elif o == '*':
                    v *= x
                elif o == '||':
                    v = int(str(v) + str(x))

            if v == test:
                tot += test
                break

    print(tot)

def part2(data):
    part1(data, ('+', '*', '||'))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
