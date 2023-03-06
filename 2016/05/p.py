#!/usr/bin/env python3

import hashlib
import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines[0]

def part(data):
    s = ''
    t = [''] * 8
    i = 0
    while len(s) < 8 or not all(t):
        b = (data + str(i)).encode('utf8')
        h = hashlib.md5(b).hexdigest()
        if h[:5] == '00000':
            s += h[5]
            debug(b, h, s, t)
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
