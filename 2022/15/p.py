#!/usr/bin/env pypy3

import re
import sys

from grid import manhattan_distance

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]

    sensors = {}
    beacons = set()
    for line in lines:
        mobj = re.match('Sensor at x=([-0-9]+), y=([-0-9]+): closest beacon is at x=([-0-9]+), y=([-0-9]+)', line)
        sx, sy, bx, by = [int(_) for _ in mobj.groups()]

        sensors[(sx, sy)] = manhattan_distance((sx, sy), (bx, by))
        beacons.add((bx, by))

    return sensors, beacons

def part1(sensors, beacons, y):
    minx = sys.maxsize
    maxx = 0

    for pt, dist in sensors.items():
        if pt[0] - dist < minx:
            minx = pt[0] - dist
        if pt[0] + dist > maxx:
            maxx = pt[0] + dist

    debug('Search x:', minx, maxx)

    cnt = 0
    for x in range(minx, maxx+1):
        if (x, y) in beacons:
            continue

        for sensor, dist in sensors.items():
            newdist = manhattan_distance((x, y), sensor)
            if newdist <= dist:
                cnt += 1
                break

    print(cnt)

def intersection(r1, r2):
    if r1[1] < r2[0] or r2[1] < r1[0]:
        return None
    return (max(r1[0], r2[0]), min(r1[1], r2[1]))

def merge_intervals(intervals):
    # Sort the array on the basis of start values of intervals.
    intervals.sort()
    stack = []
    # insert first interval into stack
    stack.append(intervals[0])
    for i in intervals[1:]:
        # Check for overlapping interval,
        # if interval overlap
        if stack[-1][0] <= i[0] <= stack[-1][-1]:
            stack[-1][-1] = max(stack[-1][-1], i[-1])
        else:
            stack.append(i)

    return stack

def part2(sensors, beacons, area):
    num_sensors = len(sensors)

    num_covered = lambda pt: sum(manhattan_distance(pt, s) <= d for s, d in sensors.items())

    pt = None
    for y in range(0, area + 1):
        if pt:
            break

        ranges = []
        for sensor, dist in sensors.items():
            # project sensor onto this row hopefully eliminating a bunch of
            # positions
            dx = dist - abs(sensor[1] - y) 
            if dx < 0:
                continue

            x0 = max(sensor[0] - dx, 0)
            x1 = min(sensor[0] + dx, area)

            ranges.append([x0, x1])

        ranges = merge_intervals(ranges)

        for i in range(1, len(ranges)):
            a = ranges[i-1]
            b = ranges[i]

            if a[1] >= b[0]:
                continue

            x0 = a[1]+1
            x1 = b[0]

            debug(f'Scan y={y} x={x0}-{x1}')
            for x in range(x0, x1+1):
                cnt = num_covered((x, y))
                if cnt == 0 and pt not in beacons:
                    pt = (x, y)
                    break

    debug(pt)
    print(pt[0] * area + pt[1])

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data, 2_000_000)
    if '2' in sys.argv:
        part2(*data, 4_000_000)

if __name__ == '__main__':
    main()
