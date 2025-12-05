#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]

    fresh = []
    ingredients = []

    for line in lines:
        if '-' in line:
            fresh.append(tuple([int(_) for _ in line.split('-')]))
        elif line:
            ingredients.append(int(line))

    return fresh, ingredients

def part1(fresh, ingredients):
    tot = 0
    for i in ingredients:
        for a, b in fresh:
            if a <= i <= b:
                tot += 1
                break
    print(tot)

def part2(fresh, _):
    # unique and sort
    fresh = sorted(set(fresh))

    found = True
    while found:
        found = False
        for i in range(len(fresh)):
            for j in range(len(fresh)):
                if i == j:
                    continue

                a1, a2 = fresh[i]
                b1, b2 = fresh[j]

                # a and b overlap, merge onto a and remove b
                if b1 <= a1 <= b2 or b1 <= a2 <= b2 or a1 <= b1 <= a2 or a1 <= b2 <= a2:
                    fresh[i] = (min(a1, b1), max(a2, b2))
                    fresh.pop(j)
                    found = True
                    break

            if found:
                break

    tot = 0
    for a, b in fresh:
        tot += b - a + 1
    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
