#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    cmds = lines[0].split(', ')
    return [(_[0], int(_[1:])) for _ in cmds]

def run(data, stop_at_second_visit=False):
    x = y = 0
    dir = 'N'
    visited = set((0, 0))
    for lr, dist in data:
        if dir == 'N':
            dir = {'L': 'W', 'R': 'E'}[lr]
        elif dir == 'E':
            dir = {'L': 'N', 'R': 'S'}[lr]
        elif dir == 'S':
            dir = {'L': 'E', 'R': 'W'}[lr]
        elif dir == 'W':
            dir = {'L': 'S', 'R': 'N'}[lr]
        else:
            assert 0, dir

        for i in range(dist):
            if dir == 'N':
                y += 1
            elif dir == 'S':
                y -= 1
            elif dir == 'E':
                x += 1
            elif dir == 'W':
                x -= 1
            else:
                assert 0, dir

            if stop_at_second_visit and (x, y) in visited:
                return (x, y)

            visited.add((x, y))

    return (x, y)

def part1(data):
    x, y = run(data)
    print(x, y, abs(x) + abs(y))

def part2(data):
    x, y = run(data, True)
    print(x, y, abs(x) + abs(y))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
