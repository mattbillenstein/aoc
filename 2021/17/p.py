#!/usr/bin/env pypy3

import sys

from grid import SparseGrid

DEBUG = sys.argv.count('-v')

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    target = lines[0].replace(',', '').replace('=', ' ').replace('.', ' ')
    target = target.split()[3:]
    xs = sorted([int(_) for _ in target[:2]])
    ys = sorted([int(_) for _ in target[3:]])
    target = ((xs[0], ys[0]), (xs[1], ys[1]))
    return target

def run(target):
    g = SparseGrid([], {'.': 0, '#': 1, 'T': 2})

    g.set((0, 0), 1)

    for y in range(target[0][1], target[1][1]+1):
        for x in range(target[0][0], target[1][0]+1):
            g.set((x, y), 2)
    
    if DEBUG:
        g.print()

    velocities = []

    MAX = (0,)

    # these ranges were came up with by guess and check...
    for DX in range(1, 500):
        for DY in range(-200, 150):
            dx = DX
            dy = DY
            maxy = 0

            e = g.copy()

            pt = (0, 0)
            last = (0, 0)
            while dx or (                                   # still moving in x or
                    target[0][0] <= pt[0] <= target[1][0]   # x in target and
                        and pt[1] > target[0][1]):          # y above bottom of target

                last = pt
                pt = (pt[0] + dx, pt[1] + dy)
                e.set(pt, 1)

                if pt[1] > maxy:
                    maxy = pt[1]

                if target[0][0] <= pt[0] <= target[1][0] and target[0][1] <= pt[1] <= target[1][1]:
                    if maxy > MAX[0]:
                        MAX = (maxy, DX, DY)
                    velocities.append((DX, DY, maxy))
                    if DEBUG:
                        print(DX, DY, maxy, MAX)
                        e.flip_x()
                        e.print()
                    break

                if dx < 0:
                    dx += 1
                elif dx > 0:
                    dx -= 1
                dy -= 1


    if DEBUG:
        velocities.sort()
        for v in velocities:
            print(v)
        print()

    print(MAX[0])
    print(len(velocities))
    
def main():
    data = parse_input()
    run(data)

if __name__ == '__main__':
    main()
