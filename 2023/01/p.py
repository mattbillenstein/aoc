#!/usr/bin/env pypy3

import sys

def parse_input():
    return [_.strip('\r\n') for _ in sys.stdin]

def part1(data):
    tot = 0
    for line in data:
        nums = [_ for _ in line if _ in '0123456789']
        tot += int(nums[0]) * 10 + int(nums[-1])
    print(tot)

def part2(data):
    nums = ['1', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', '2', '3', '4', '5', '6', '7', '8', '9']
    tot = 0
    for line in data:
        a = [(line.find(_), _) for _ in nums]
        a = min([_ for _ in a if _[0] != -1])[1]
        a = int(a) if a.isdigit() else nums.index(a)

        b = [(line.rfind(_), _) for _ in nums]
        b = max([_ for _ in b if _[0] != -1])[1]
        b = int(b) if b.isdigit() else nums.index(b)

        tot += a * 10 + b

    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
