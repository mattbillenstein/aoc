#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    blocks = []
    for line in lines:
        a, b = [int(_) for _ in line.split('-')]
        blocks.append((a, b))
    return blocks

def part(blocks):
    merged = True
    while merged:
        merged = False
        blocks = sorted([_ for _ in blocks if _])
        for i in range(len(blocks)-1):
            a, b = blocks[i:i+2]
            if a is None or b is None:
                continue

            if a[0] <= b[0] <= b[1] <= a[1]:
                # b encloses a, remove b
                blocks[i+1] = None
                merged = True
            elif a[0] <= b[0] <= a[1] <= b[1]:
                # overlap, replace a, remove b
                blocks[i] = (a[0], b[1])
                blocks[i+1] = None
                merged = True

    # part 1, first ip
    for i in range(len(blocks)-1):
        a, b = blocks[i:i+2]
        if b[0] - a[1] > 1:
            print(a[1] + 1)
            break

    # part 2, how many ips
    # start of range
    cnt = blocks[0][0]

    # count ips between blocks
    for i in range(len(blocks)-1):
        a, b = blocks[i:i+2]
        cnt += b[0] - a[1] - 1

    # end of range
    cnt += 2**32-1 - blocks[-1][1]
    print(cnt)

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
