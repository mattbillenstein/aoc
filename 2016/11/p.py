#!/usr/bin/env pypy3

import copy
import itertools
import re
import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    floors = [set() for _ in range(4)]
    elems = set()
    for i, line in enumerate(lines):
        line = line.replace('-compatible', '')
        for s in re.findall('[a-z]+ (?:generator|microchip)', line):
            s = s.replace('microchip', 'M')
            s = s.replace('generator', 'G')
            floors[i].add(tuple(s.split()))
            elems.add(s.split()[0])

    elems = sorted(elems)
    d = dict(zip(elems, 'ABCDEFGHIJKLMNOP'))
    for i in range(4):
        floors[i] = set([d[_[0]] + _[1] for _ in floors[i]])
    return floors

def other(s):
    return s[0] + ('G' if s[1] == 'M' else 'M')

def check(floors):
    # return True if we're good...
    for s in floors:
        gens = [_ for _ in s if _[1] == 'G']
        if gens and any(other(_) not in gens for _ in s if _[1] == 'M'):
            return False
    return True

def move(floors, E, steps, best, visited):
    if not check(floors):
        return

    if steps > best[0]:
        return

    # use elevator position and the count of each type of item on each floor as
    # visited key
    types = [[_[1] for _ in s] for s in floors]
    state = (E, tuple([(_.count('M'), _.count('G')) for _ in types]))
    if visited.get(state, sys.maxsize) <= steps:
        return

    visited[state] = steps

    if DEBUG > 1:
        print(E, steps, best)
        for k, v in floors.items():
            print(k, v)
        print()

    if not any(floors[_] for _ in range(3)):
        if steps < best[0]:
            if DEBUG:
                print(steps)
            best[0] = steps
        return

    if E < 3:
        # move pairs up
        for tup in itertools.combinations(floors[E], 2):
            for x in tup:
                floors[E+1].add(x)
                floors[E].remove(x)

            move(floors, E+1, steps+1, best, visited)

            for x in tup:
                floors[E+1].remove(x)
                floors[E].add(x)

    if E > 0:
        # try moving every single item down
        for item in floors[E]:
            floors[E].remove(item)
            floors[E-1].add(item)

            move(floors, E-1, steps+1, best, visited)

            floors[E].add(item)
            floors[E-1].remove(item)

        # and pairs
        for tup in itertools.combinations(floors[E], 2):
            for x in tup:
                floors[E-1].add(x)
                floors[E].remove(x)

            move(floors, E-1, steps+1, best, visited)

            for x in tup:
                floors[E-1].remove(x)
                floors[E].add(x)

def part1(floors):
    best = [sys.maxsize]
    move(floors, 0, 0, best, {})
    print(best[0])

def part2(floors):
    # two new pairs added to floor 1
    floors[0].update(['FM', 'FG', 'GM', 'GG'])

    best = [sys.maxsize]
    move(floors, 0, 0, best, {})
    print(best[0])

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(copy.deepcopy(data))
    if '2' in sys.argv:
        part2(copy.deepcopy(data))

if __name__ == '__main__':
    main()
