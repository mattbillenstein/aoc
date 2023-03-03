#!/usr/bin/env pypy3

import sys
from collections import defaultdict

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    lines = [int(_) for _ in lines]
    return lines

def find_invalid(data):
    d = defaultdict(int)
    for i in data[0:25]:
        d[i] += 1

    for idx in range(25, len(data)):
        debug(d)
        i = data[idx]
        found = False
        for k, cnt in d.items():
            if k < i:
                j = i - k
                debug(i, k, j, cnt)
                debug(j in d)
                if j == i and d[j] >= 2:
                    found = True
                elif j in d:
                    found = True

                if found:
                    break

        if not found:
            break

        d[data[idx-25]] -= 1
        if d[data[idx-25]] <= 0:
            debug('remove', data[idx-25])
            del d[data[idx-25]]
        d[i] += 1

    return i

def part1(data):
    print(find_invalid(data))

def part2(data):
    num = find_invalid(data)

    i = 0
    j = 1
    s = data[i] + data[j]

    while s != num:
        while s < num:
            j += 1
            s += data[j]

        while s > num and i < j:
            s -= data[i]
            i += 1

    assert num == sum(data[i:j+1])
    print(min(data[i:j+1]) + max(data[i:j+1]))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
