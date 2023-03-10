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
    floors = {_+1: set() for _ in range(4)}
    elems = set()
    for i, line in enumerate(lines):
        line = line.replace('-compatible', '')
        for s in re.findall('[a-z]+ (?:generator|microchip)', line):
            s = s.replace('microchip', 'M')
            s = s.replace('generator', 'G')
            floors[i+1].add(tuple(s.split()))
            elems.add(s.split()[0])

    elems = sorted(elems)
    d = dict(zip(elems, 'ABCDEFGHIJKLMNOP'))
    for k in list(floors):
        floors[k] = set([d[_[0]] + _[1] for _ in floors[k]])
    return floors

def other(s):
    return s[0] + ('G' if s[1] == 'M' else 'M')

def check(floors):
    # return True if we're good...
    for f, s in floors.items():
        gens = [_ for _ in s if _[1] == 'G']
        if gens and any(other(_) not in gens for _ in s if _[1] == 'M'):
            return False
    return True

def canon(floors):
    map = {}
    found = []
    c = 'A'
    for i in (1, 2, 3, 4):
        for item in floors[i]:
            assert len(item) == 2
            if item not in found:
                oitem = other(item)
                found.append(item)
                found.append(oitem)

                x = c + item[1]
                y = c + oitem[1]
                c = chr(ord(c) + 1)

                map[item] = x
                map[oitem] = y

    return {k: set(map[_] for _ in v) for k, v in floors.items()}

def move(floors, E, steps, best, visited):
    if not check(floors):
        return

    if steps > best[0]:
        return

    poss = steps
    for i in (1, 2, 3):
        # leaving out a factor of 2 twice here, we carry two and need to go up
        # and down... Seems very approximately correct and speeds this all up,
        # but not tested thoroughly...
        poss += len(floors[i]) * (4-i)

    if poss > best[0]:
        return

    # any pair is interchangable, so we can remove a lot of intermediate states
    # by canonicalizing here...
    floors = canon(floors)

    state = hash((E, tuple([(k, frozenset(v)) for k, v in floors.items()])))
    if visited.get(state, sys.maxsize) <= steps:
        return

    visited[state] = steps

    if DEBUG > 1:
        print(E, steps, best)
        for k, v in floors.items():
            print(k, v)
        print()

    if all(not floors[_] for _ in (1, 2, 3)):
        if steps < best[0]:
            if DEBUG:
                print(steps)
            best[0] = steps
        return

    if E < 4:
        for tup in itertools.combinations(floors[E], 2):
            for x in tup:
                floors[E+1].add(x)
                floors[E].remove(x)

            move(floors, E+1, steps+1, best, visited)

            for x in tup:
                floors[E+1].remove(x)
                floors[E].add(x)

    if E > 1:
        # try moving every single item down
        for item in floors[E]:
            floors[E].remove(item)
            floors[E-1].add(item)

            move(floors, E-1, steps+1, best, visited)

            floors[E].add(item)
            floors[E-1].remove(item)

        # and pairs
        for tup in itertools.combinations(floors[E], 2):
            # skip G/G, may not work on all inputs?
            if tup[0][1] == tup[1][1] == 'G':
                continue

            for x in tup:
                floors[E-1].add(x)
                floors[E].remove(x)

            move(floors, E-1, steps+1, best, visited)

            for x in tup:
                floors[E-1].remove(x)
                floors[E].add(x)

def part1(floors):
    best = [sys.maxsize]
    move(floors, 1, 0, best, {})
    print(best[0])

def part2(floors):
    # two new pairs added to floor 1
    floors[1].update(['FM', 'FG', 'GM', 'GG'])

    best = [sys.maxsize]
    move(floors, 1, 0, best, {})
    print(best[0])

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(copy.deepcopy(data))
    if '2' in sys.argv:
        part2(copy.deepcopy(data))

if __name__ == '__main__':
    main()
