#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines[0]

def part1(num, times=40):
    for _ in range(times):
        s = []
        i = 0
        while i < len(num):
            cnt = 0
            j = i+1
            while j < len(num) and num[j] == num[i]:
                j += 1
            s.append(str(j-i))
            s.append(num[i])
            i = j

        num = ''.join(s)

    print(len(num))

def part2(num):
    part1(num, times=50)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
