#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    robots = []
    for line in lines:
        for c in '=,':
            line = line.replace(c, ' ')
        tup = line.split()
        L = [int(tup[_]) for _ in (1, 2, 4, 5)]
        robots.append(L)
    return robots

def part1(robots):
    # move robots 500 steps and take the product of the count in each
    # quadrant...
    gx, gy = 101, 103
    if len(robots) < 100:
        gx, gy = 11, 7

    mx = gx // 2
    my = gy // 2

    steps = 100

    quads = [0, 0, 0, 0]
    for robot in robots:
        px, py, vx, vy = robot
        npx = (px + vx * steps) % gx
        npy = (py + vy * steps) % gy

        if npx < mx:
            if npy < my:
                quads[0] += 1
            elif npy > my:
                quads[1] += 1
        elif npx > mx:
            if npy < my:
                quads[2] += 1
            elif npy > my:
                quads[3] += 1
        
    tot = 1
    for x in quads:
        tot *= x
    print(tot)

def part2(robots):
    # displays an xmas tree - construct text art and look for a horizontal
    # line...
    gx, gy = 101, 103

    mx = gx // 2
    my = gy // 2

    px, py, vx, vy = 0, 1, 2, 3

    for step in range(1, 1000000):
        g = [['.'] * gx for _ in range(gy)]
        for robot in robots:
            robot[px] = x = (robot[px] + robot[vx]) % gx
            robot[py] = y = (robot[py] + robot[vy]) % gy
            g[y][x] = '#'

        s = '\n'.join(''.join(_) for _ in g)
        if '################' in s:
            print(step)
            if '-v' in sys.argv:
                print(s)
            break

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1([list(_) for _ in data])
    if '2' in sys.argv:
        part2([list(_) for _ in data])

if __name__ == '__main__':
    main()
