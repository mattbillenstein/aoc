#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    times = [int(_) for _ in lines[0].split()[1:]]
    dists = [int(_) for _ in lines[1].split()[1:]]
    return times, dists

def part1(times, dists):
    tot = 1
    for time, dist in zip(times, dists):
        wins = 0
        for speed in range(time+1):
            traveled = (time - speed) * speed
            if traveled > dist:
                wins += 1
        tot *= wins
    print(tot)

def part2(times, dists):
    time = int(''.join(str(_) for _ in times))
    dist = int(''.join(str(_) for _ in dists))

    wins = 0
    for speed in range(time+1):
        traveled = (time - speed) * speed
        if traveled > dist:
            wins += 1
    print(wins)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
