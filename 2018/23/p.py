#!/usr/bin/env pypy3

import sys
from collections import defaultdict

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    bots = []
    for line in lines:
        for c in '<>,=':
            line = line.replace(c, ' ')
        L = line.split()
        x, y, z = [int(_) for _ in L[1:4]]
        r = int(L[-1])
        bots.append(((x, y, z), r))
    return bots

def manhattan_distance(a, b):
    return sum(abs(x-y) for x, y in zip(a, b))

def part1(bots):
    bots.sort(key=lambda x: x[1])

    b, r = bots[-1]

    cnt = 0
    for bot, r2 in bots:
        if manhattan_distance(b, bot) <= r:
            cnt += 1

    print(cnt)

def bot_in_range(box, bot, r):
    # compute manhattan distance from bot to box and then check if it's <= r
    d = 0
    for i in range(3):
        if not box[0][i] <= bot[i] <= box[1][i]:
            # min manhattan distance on this axis of the two box edges if the
            # bot is not inside the box on this axis...
            d += min(abs(box[0][i]-bot[i]), abs(box[1][i]-bot[i]))
    return d <= r

def count_in_range(box, bots):
    return sum(1 for b, r in bots if bot_in_range(box, b, r))

def split_box(box):
    x0, y0, z0 = box[0]
    x2, y2, z2 = box[1]
    x1 = x0 + (x2 - x0) // 2
    y1 = y0 + (y2 - y0) // 2
    z1 = z0 + (z2 - z0) // 2
    return [
        ((x0, y0, z0), (x1, y1, z1)),
        ((x0, y0, z1), (x1, y1, z2)),
        ((x0, y1, z0), (x1, y2, z1)),
        ((x1, y0, z0), (x2, y1, z1)),
        ((x0, y1, z1), (x1, y2, z2)),
        ((x1, y1, z0), (x2, y2, z1)),
        ((x1, y0, z1), (x2, y1, z2)),
        ((x1, y1, z1), (x2, y2, z2)),
    ]

def count_in_range_pt(pt, bots):
    return sum(1 for b, r in bots if manhattan_distance(pt, b) <= r)

def part2(bots):
    origin = (0, 0, 0)

    # make a large box in range of all bots
    size = 1
    while 1:
        box = ((-size, -size, -size), (size, size, size))
        if count_in_range(box, bots) == len(bots):
            break
        size *= 2

    # split the box into 8 sub-boxes and keep the best scoring ones by size -
    # as the boxes get smaller, they will be in range of less bots...
    boxes = [(count_in_range(box, bots), box)]

    while 1:
        newboxes = []
        for cnt, box in boxes:
            debug(box, cnt)
            for b in split_box(box):
                cnt = count_in_range(b, bots)
                debug('  ', b, cnt)
                newboxes.append((cnt, b))

        boxes = newboxes
        boxes.sort(reverse=True)
        boxes = [_ for _ in boxes if _[0] == boxes[0][0]]

        # box size 1, we can just inspect the first point of each box now
        cnt, box = boxes[0]
        if (box[1][0] - box[0][0]) == 1:
            break

    # find the max count and min manhattan distance of first corner of
    # remaining size 1 boxes
    pts = [_[1][0] for _ in boxes]
    L = [(count_in_range_pt(_, bots), -manhattan_distance(origin, _), _) for _ in pts]
    L.sort()
    cnt, dist, pt = L[-1]
    debug(pt, cnt)
    print(-dist)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
