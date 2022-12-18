#!/usr/bin/env python3

import sys
import string

priorities = ' ' + string.ascii_letters

def main(argv):
    tot = 0
    L = []
    with open(argv[1]) as f:
        for line in f:
            line = line.strip()
            L.append(line)
            if len(L) == 3:
                common = set(L[0]) & set(L[1]) & set(L[2])
                assert len(common) == 1
                common = common.pop()
                tot += priorities.index(common)
                L.clear()

    print(tot)

if __name__ == '__main__':
    main(sys.argv)
