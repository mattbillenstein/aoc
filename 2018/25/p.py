#!/usr/bin/env pypy3

import sys

from grid import manhattan_distance

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return [tuple([int(x) for x in _.split(',')]) for _ in lines]

def part1(data):
    cons = [set()]
    cons[0].add(data[0])

    for pt in data:
        found = None
        for con in cons:
            for pt2 in con:
                if manhattan_distance(pt, pt2) <= 3:
                    found = con
                    break
            if found:
                break

        if found:
            found.add(pt)
        else:
            cons.append(set())
            cons[-1].add(pt)

    # lazy and slow, just merge two at a time and remove from list...
    while 1:
        found = None
        for con1 in cons:
            for con2 in cons:
                if con1 is con2:
                    continue
                for pt1 in con1:
                    for pt2 in con2:
                        if manhattan_distance(pt1, pt2) <= 3:
                            found = (con1, con2)
                            break
                    if found:
                        break
                if found:
                    break
            if found:
                break

        if not found:
            break

        con1, con2 = found
        con1.update(con2)
        cons.remove(con2)

    print(len(cons))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)

if __name__ == '__main__':
    main()
