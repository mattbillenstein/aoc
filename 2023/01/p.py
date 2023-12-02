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
    nums = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    tot = 0
    for line in data:
        mn, mx = 1000, -1
        a = b = None
        for num in nums:
            idx = line.find(num)
            if idx >= 0:
                if idx < mn:
                    mn = idx
                    a = num

            idx = line.rfind(num)
            if idx >= 0:
                if idx > mx:
                    mx = idx
                    b = num

        a = int(a) if a.isdigit() else nums.index(a) + 1
        b = int(b) if b.isdigit() else nums.index(b) + 1

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
