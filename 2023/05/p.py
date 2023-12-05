#!/usr/bin/env pypy3

import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    seeds = [int(_) for _ in lines[0].split(':')[1].strip().split()]
    maps = {}
    for line in lines[1:]:
        if line.endswith(' map:'):
            k = line.split()[0].split('-')
            k = (k[0], k[2])
            maps[k] = map = []
        elif line:
            x = tuple([int(_) for _ in line.split()])
            map.append(((x[1], x[1] + x[2] - 1), x[0] - x[1]))

    for map in maps.values():
        map.sort()

    return seeds, maps

def map_value(value, map):
    for src, delta in map:
        if src[0] <= value <= src[1]:
            return value + delta
    return value

def part1(seeds, maps):
    k = 'seed'
    L = seeds
    while k != 'location':
        for key, map in maps.items():
            if key[0] == k:
                L = [map_value(_, map) for _ in L]
                k = key[1]
                break
    return print(min(L))

def map_range(rng, map):
    # tricky bit is a given range can match multiple ranges in the map...
    ranges = [rng]
    res = []
    while ranges:
        matched = False
        start, end = rng = ranges.pop()
        for src, delta in map:
            # end in range
            if start < src[0] <= end <= src[1]:
                matched = True
                debug('end in range', (start, end), src, delta)
                ranges.append((start, src[0] - 1))
                res.append((src[0] + delta, end + delta))
            
            # start in range
            elif src[0] <= start <= src[1] < end:
                matched = True
                debug('start in range', (start, end), src, delta)
                ranges.append((src[1] + 1, end))
                res.append((start + delta, src[1] + delta))

            # start and end in range
            elif src[0] <= start <= end <= src[1]:
                matched = True
                debug('both in range', (start, end), src, delta)
                res.append((start + delta, end + delta))

            # start and end contain range
            elif start < src[0] <= src[1] < end:
                matched = True
                debug('contain range', (start, end), src, delta)
                ranges.append((start, src[0] - 1))
                res.append((src[0] + delta, src[1] + delta))
                ranges.append((src[1] + 1,  end))

        if not matched:
            debug('no overlap', (start, end))
            res.append(rng)

    res.sort()
    debug('result', res)
    return res

def test_map_range():
    # sanity checks

    # non-overlapping
    x = map_range((5, 10), [((15, 20), 100)])
    assert x == [(5, 10)], x

    x = map_range((25, 30), [((15, 20), 100)])
    assert x == [(25, 30)], x

    # edge-overlapping
    x = map_range((10, 15), [((15, 20), 100)])
    assert x == [(10, 14), (115, 115)], x

    x = map_range((20, 25), [((15, 20), 100)])
    assert x == sorted([(120, 120), (21, 25)]), x

    # map contains
    x = map_range((20, 25), [((15, 30), 100)])
    assert x == [(120, 125)], x

    # map edge-contains
    x = map_range((20, 25), [((20, 25), 100)])
    assert x == [(120, 125)], x

    # range contains
    x = map_range((15, 30), [((20, 25), 100)])
    assert x == sorted([(15, 19), (120, 125), (26, 30)]), x

    # range edge-contains
    x = map_range((20, 30), [((20, 30), 100)])
    assert x == [(120, 130)], x

def part2(seeds, maps):
    test_map_range()

    ranges = []
    for i in range(0, len(seeds), 2):
        start = seeds[i]
        end = seeds[i] + seeds[i+1] - 1
        ranges.append((start, end))

    k = 'seed'
    while k != 'location':
        debug()
        debug(k, ranges)
        for key, map in maps.items():
            if key[0] == k:
                nranges = []
                for x in ranges:
                    nranges.extend(map_range(x, map))
                ranges = nranges
                k = key[1]
                break

    debug(k, ranges)
    print(min([_[0] for _ in ranges]))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
