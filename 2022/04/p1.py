#!/usr/bin/env python3

import sys
from collections import defaultdict

def main(argv):
    cnt = 0
    cnt2= 0
    with open(argv[1]) as f:
        
        for line in f:
            line = line.strip()
            a, b = line.split(',')
            a1, a2 = [int(_) for _ in a.split('-')]
            b1, b2 = [int(_) for _ in b.split('-')]

            # a contains b or b contains a
            if b1 >= a1 and b2 <= a2 or a1 >= b1 and a2 <= b2:
                cnt += 1

            # a and b overlap
            if b1 <= a1 <= b2 or b1 <= a2 <= b2 or a1 <= b1 <= a2 or a1 <= b2 <= a2:
                cnt2 += 1

    print(cnt)
    print(cnt2)

if __name__ == '__main__':
    main(sys.argv)
