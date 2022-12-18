#!/usr/bin/env python3

import sys
from collections import defaultdict

def main(argv):
    with open(argv[1]) as f:
        line = f.read().strip()

    num = 14 # 4 for p1

    i, j = 0, num
    while len(set(line[i:j])) != num:
        i += 1
        j += 1

    print(j)

if __name__ == '__main__':
    main(sys.argv)
