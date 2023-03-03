#!/usr/bin/env pypy3

import itertools
import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    signal = [int(_) for _ in lines[0]]
    return signal

def base(n):
    i = 0
    base = [0, 1, 0, -1]
    while 1:
        for digit in base:
            for _ in range(n):
                if i > 0:
                    yield digit
                i += 1

def part1(data):
    for i in range(100):
        newdata = []
        for n in range(1, len(data)+1):
            digit = abs(sum(a*b for a, b in zip(data, base(n)))) % 10
            newdata.append(digit)
        data = newdata
    print(''.join(str(_) for _ in data[:8]))

def part2(data):
    # needed a hint for this part - since the offset falls in the second half
    # of a very long sequence, the coefficients at that point are all 1's and
    # we can ignore everything up to the offset... So we can just accumulate
    # mod 10 in reverse order...

    N = 10000

    offset = 0
    for d in data[:7]:
        offset *= 10
        offset += d

    data = data * N
    data = data[offset:]
    data.reverse()

    for i in range(100):
        data = list(itertools.accumulate(data, lambda a, b: (a+b) % 10))

    data.reverse()
    print(''.join(str(_) for _ in data[:8]))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
