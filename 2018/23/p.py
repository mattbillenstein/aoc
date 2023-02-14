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

def box_intersect(box, bot, r):
    # this little bit is cribbed - this manhattan distance intersection
    # requires a bit more study...
    d = 0
    for i in range(3):
        low, high = box[0][i], box[1][i] - 1
        d += abs(bot[i] - low) + abs(bot[i] - high)
        d -= high - low
    d //= 2
    return d <= r

def count_in_range(box, bots):
    return sum(1 for b, r in bots if box_intersect(box, b, r))

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

def box_size(box):
    return box[1][0] - box[0][0]

def part2(bots):
    # box solution
    origin = (0, 0, 0)

    # make a large box in range of all bots
    size = 1
    while 1:
        box = ((-size, -size, -size), (size, size, size))
        if count_in_range(box, bots) == len(bots):
            break
        size *= 2

    # split the box into 8 octants and keep the best scoring ones by size - as
    # the boxes get smaller, they will be in range of less bots...
    best = defaultdict(list)
    best[box_size(box)].append((count_in_range(box, bots), box))

    while 1:
        # examine all boxes with the same score at the smallest size
        size = min(best)
        boxes = best[size]
        boxes.sort(reverse=True)
        boxes = [_[1] for _ in boxes if _[0] == boxes[0][0]]

        # small enough, just spin through all left points
        if size < 8:
            break

        for box in boxes:
            debug(box_size(box), box, count_in_range(box, bots))
            for b in split_box(box):
                size = box_size(b)
                cnt = count_in_range(b, bots)
                debug('  ', box_size(b), b, count_in_range(b, bots))
                best[size].append((cnt, b))

    # now brute force search all points in remaining boxes keeping point with
    # best score and lowest manhattan distance to origin...
    pt = None
    cnt = 0
    dist = 0
    for box in boxes:
        debug(box_size(box), box, count_in_range(box, bots))

        for x in range(box[0][0], box[1][0]):
            for y in range(box[0][1], box[1][1]):
                for z in range(box[0][2], box[1][2]):
                    npt = (x, y, z)
                    ndist = manhattan_distance(origin, npt)
                    ncnt = sum(1 for b, r in bots if manhattan_distance(npt, b) <= r)
                    if ncnt > cnt or (ncnt == cnt and ndist < dist):
                        pt = npt
                        cnt = ncnt
                        dist = ndist

    print(pt, cnt, dist)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
