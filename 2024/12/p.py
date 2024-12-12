#!/usr/bin/env pypy3

import sys
from collections import defaultdict

from grid import Grid

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines

def make_regions(g):
    visited = set()
    regions = []
    for pt in g:
        if pt in visited:
            continue

        c = g.getc(pt)
        region = {'plant': c, 'points': set(), 'perimeter': 0}  # area is just len(points)
        regions.append(region)

        q = [pt]
        while q:
            pt = q.pop()
            if pt in visited:
                # added to q multiple times
                continue

            visited.add(pt)
            region['points'].add(pt)

            npts = g.neighbors4(pt)

            # boundary perimeter
            region['perimeter'] += 4 - len(npts)

            for npt in npts:
                if g.getc(npt) == c:
                    q.append(npt)
                else:
                    # perimter to another region
                    region['perimeter'] += 1

    return regions
            
def part1(data):
    g = Grid(data)
    regions = make_regions(g)

    # part1 - cost is area * perimeter
    print(sum(len(_['points']) * _['perimeter'] for _ in regions))

def part2(data):
    g = Grid(data)
    regions = make_regions(g)

    # part2 - cost is area * sides

    # for each region, group boundary points by direction and coordinate, tnen
    # sort by other coordinate and count groups of contiguous coordinates...
    # Ie, a side.

    tot = 0
    for region in regions:
        plant = region['plant']
        points = region['points']

        # hash (direction, coord, pt[coord]) -> [...points...]
        sides = defaultdict(list)

        # directions we step and the x or y coordinate we hash to
        dircoords = [('^', 1), ('>', 0), ('v', 1), ('<', 0)]
        for dir, coord in dircoords:
            for pt in points:
                npt = g.step(pt, dir)
                # if on boundary, or bordering different plant, hash to proper
                # x/y and append
                if not npt or g.getc(npt) != plant:
                    sides[(dir, coord, pt[coord])].append(pt)

        # for each group count number of contiguious groups of points
        num_sides = 0
        for key, side in sides.items():
            dir, coord, _ = key

            # at least one side
            num_sides += 1

            # sort by other coord and scan for breaks
            coord = 0 if coord == 1 else 1
            side.sort(key=lambda _: _[coord])
            lastpt = side[0]
            for pt in side[1:]:
                if pt[coord] != lastpt[coord]+1:
                    # break, start another side
                    num_sides += 1
                lastpt = pt

        cost = len(region['points']) * num_sides
        tot += cost

    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
