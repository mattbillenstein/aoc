#!/usr/bin/env pypy3

import sys
try:
    from _md5 import md5
except ImportError:
    from hashlib import md5

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines[0]

def part(data):
    s = ''
    t = [''] * 8
    i = 0
    while len(s) < 8 or not all(t):
        h = md5((data + str(i)).encode()).hexdigest()
        if h[:5] == '00000':
            s += h[5]
            pos = int(h[5], 16)
            if pos < len(t) and not t[pos]:
                t[pos] = h[6]
        i += 1

    print(s[:8])
    print(''.join(t[:8]))

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
