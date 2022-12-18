#!/usr/bin/env python3

import sys
import string

priorities = ' ' + string.ascii_letters

def main(argv):
    tot = 0
    with open(argv[1]) as f:
        for line in f:
            line = line.strip()
            mid = len(line) // 2
            A, B = line[:mid], line[mid:]
            assert len(A) == len(B)
            common = set(A) & set(B)
            assert len(common) == 1
            common = common.pop()
            tot += priorities.index(common)

    print(tot)

if __name__ == '__main__':
    main(sys.argv)
