#!/usr/bin/env pypy3

import sys
import time
from collections import defaultdict
from pprint import pprint

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return set(sorted([tuple([int(x) for x in _.split(',')]) for _ in lines]))

def neighbors(cube):
    x, y, z = cube
    yield (x-1, y, z)
    yield (x+1, y, z)
    yield (x, y-1, z)
    yield (x, y+1, z)
    yield (x, y, z-1)
    yield (x, y, z+1)

def get_enclosed_cubes(cubes):
    enclosed = set()
    not_enclosed = set()

    mmin = min(min(_) for _ in cubes)
    mmax = max(max(_) for _ in cubes) + 1

    for x in range(mmin, mmax):
        for y in range(mmin, mmax):
            for z in range(mmin, mmax):
                cube = (x, y ,z)
                if cube in cubes:
                    continue

                L = [
                    any((_, y, z) in cubes for _ in range(mmin, x)),
                    any((_, y, z) in cubes for _ in range(x+1, mmax)),
                    any((x, _, z) in cubes for _ in range(mmin, y)),
                    any((x, _, z) in cubes for _ in range(y+1, mmax)),
                    any((x, y, _) in cubes for _ in range(mmin, z)),
                    any((x, y, _) in cubes for _ in range(z+1, mmax)),
                ]
                if all(L):
                    enclosed.add(cube)
                else:
                    not_enclosed.add(cube)

    # some enclosed see a cube in every direction, but are in a cave of some
    # shape, remove them iteratively by seeing if they have any not_enclosed
    # neighbors - probably a better algo for this whole thing? 3d bfs?
    while 1:
        size = len(enclosed)
        for ecube in list(enclosed):
            for n in neighbors(ecube):
                if n in not_enclosed:
                    not_enclosed.add(ecube)
                    enclosed.remove(ecube)

        if len(enclosed) == size:
            break

    return enclosed

def part1(cubes):
    surface_area = 0
    for cube in cubes:
        for n in neighbors(cube):
            if n not in cubes:
                surface_area += 1

    print(surface_area)

def part2(cubes):
    enclosed = get_enclosed_cubes(cubes)

    surface_area = 0
    for cube in cubes:
        for n in neighbors(cube):
            if n not in cubes and n not in enclosed:
                surface_area += 1

    print(surface_area)

def bfs(frontier, cubes, mmin, mmax):
    surface_area = 0
    visited = set()
    while frontier:
        next_frontier = set()
        for cube in frontier:
            visited.add(cube)
            for n in neighbors(cube):
                if n in cubes:
                    surface_area += 1
                elif n not in visited and all(mmin <= _ <= mmax for _ in n):
                    next_frontier.add(n)

        frontier = next_frontier

    return surface_area

def part2_bfs(cubes):
    mmin = min(min(_) for _ in cubes) - 1
    mmax = max(max(_) for _ in cubes) + 1

    surface_area = bfs({(mmin, mmin, mmin)}, cubes, mmin, mmax)
    print(surface_area)

def main(argv):
    data = parse_input()

    if '1' in sys.argv:
        part1(data)

    if '2a' in sys.argv:
        part2(data)

    if '2' in sys.argv:
        part2_bfs(data)

if __name__ == '__main__':
    main(sys.argv)
