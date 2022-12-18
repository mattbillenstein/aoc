#!/usr/bin/env python3

import re
import sys

def manhattan(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

def main(argv):
    with open(argv[1]) as f:
        lines = [_.strip('\r\n') for _ in f]

    sensors = {}
    beacons = set()
    minx = 1e18
    maxx = -1e18
    for line in lines:
        mobj = re.match('Sensor at x=([-0-9]+), y=([-0-9]+): closest beacon is at x=([-0-9]+), y=([-0-9]+)', line)
        sx, sy, bx, by = [int(_) for _ in mobj.groups()]

        sensors[(sx, sy)] = dist = manhattan((sx, sy), (bx, by))
        beacons.add((bx, by))

        if (sx - dist) < minx:
            minx = sx - dist
        if (sx + dist) > maxx:
            maxx = sx + dist

    print('Search x:', minx, maxx)

    y = int(sys.argv[2])
    cnt = 0
    for x in range(minx, maxx+1):
        if (x, y) in beacons:
            continue

        for sensor, dist in sensors.items():
            newdist = manhattan((x, y), sensor)
            if newdist <= dist:
                cnt += 1
                break

    print(cnt)

if __name__ == '__main__':
    main(sys.argv)
