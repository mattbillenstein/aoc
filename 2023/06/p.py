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

    # scan the range looking for min/max hold times where we still win
    jump = 1000
    mn = time + 1
    mx = -1
    for speed in range(0, time+1, jump):
        traveled = (time - speed) * speed
        if traveled > dist:
            if speed < mn:
                mn = speed
            if speed > mx:
                mx = speed

    # find start wher we win
    for speed in range(mn - jump, time+1, 1):
        traveled = (time - speed) * speed
        if traveled > dist:
            start = speed
            break

    # find end where we don't win
    for speed in range(mx, time+1, 1):
        traveled = (time - speed) * speed
        if traveled < dist:
            end = speed
            break

    # take difference
    print(end - start)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
