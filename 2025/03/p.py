#!/usr/bin/env pypy3

import sys

def parse_input():
    return [_.strip('\r\n') for _ in sys.stdin]

def part(banks, N):
    # take the max digit in the part of the bank after our last batt turned on
    # and the number of batts we need to make N digits...
    tot = 0
    for bank in banks:
        # Negate the index here so we take the first max digit L to R order for
        # equal digits
        chars = [(c, -i) for i, c in enumerate(bank)]

        s = ''
        i = 0
        for j in range(len(chars) - (N - 1), len(chars) + 1):
            c, idx = max(chars[i:j])
            s += c
            i = -idx + 1  # undo negation here

        tot += int(s)

    print(tot)

def main():
    banks = parse_input()
    if '1' in sys.argv:
        part(banks, 2)
    if '2' in sys.argv:
        part(banks, 12)

if __name__ == '__main__':
    main()
