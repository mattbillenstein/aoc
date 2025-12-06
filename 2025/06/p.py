#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return (lines,)

def math(op, nums):
    x = None
    if op == '*':
        x = 1
        for y in nums:
            x *= y
    elif op == '+':
        x = sum(nums)

    assert x is not None
    return x

def part1(lines):
    nums = []
    ops = None
    for line in lines:
        if '*' in line or '+' in line:
            assert ops is None
            ops = line.split()
        else:
            nums.append([int(_) for _ in line.split()])

    tot = 0
    for op, L in zip(ops, zip(*nums)):
        tot += math(op, L)

    print(tot)

def part2(lines):
    tot = 0
    nums = []
    op = None
    for col in zip(*lines):
        if all(_ == ' ' for _ in col):
            tot += math(op, nums)
            op = None
            nums = []
        else:
            if col[-1] != ' ':
                op = col[-1]
            nums.append(int(''.join(_ for _ in col[:-1] if _ != ' ')))

    tot += math(op, nums)
    print(tot)
    
def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
