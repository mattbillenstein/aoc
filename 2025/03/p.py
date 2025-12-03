#!/usr/bin/env pypy3

import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return (lines,)

def part1(data):
    # Find biggest digit except last, then biggest digit after that digit...
    L = []
    for bank in data:
        a = max(bank[:-1])
        idx = bank.find(a)
        b = max(bank[idx+1:])
        s = a + b

        debug(bank, s)
        L.append(int(s))

    print(sum(L))

def part2(data):
    # take the max digit in the part of the bank after our last batt turned on
    # and the number of batts we need to make 12 digits...
    L = []
    for bank in data:
        # Negate the index here so we take the first max digit L to R order for
        # equal digits
        chars = [(c, -i) for i, c in enumerate(bank)]

        s = ''
        i, j = 0, len(chars) - 11
        for _ in range(12):
            c, idx = max(chars[i:j])
            s += c
            i = -idx + 1  # undo negation
            j += 1

        debug(bank, s)
        L.append(int(s))

    print(sum(L))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
