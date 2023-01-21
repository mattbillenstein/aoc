#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return [int(_) for _ in lines[0].split('-')]

def run(a, b):
    p1cnt = 0
    p2cnt = 0
    for i in range(a, b + 1):
        digits = [int(_) for _ in str(i)]
        if all(digits[_] <= digits[_+1] for _ in range(len(digits)-1)) and \
            any(digits[_] == digits[_+1] for _ in range(len(digits)-1)):
            p1cnt += 1

            # must contain at least one run of repeated exactly length 2, pad
            # and check...
            digits = [-1] + digits + [-1]
            if any(digits[_] != digits[_+1] == digits[_+2] != digits[_+3] for _ in range(len(digits)-3)):
                p2cnt += 1

    print(p1cnt)
    print(p2cnt)

def main():
    data = parse_input()
    run(*data)

if __name__ == '__main__':
    main()
