#!/usr/bin/env python3

import itertools
import math
import sys
from pprint import pprint

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    moons = []
    for line in lines:
        for c in '<>,=xyz':
            line = line.replace(c, '')
        coords = [int(_) for _ in line.split()]
        moons.append(Moon(*coords))
    return moons

class Moon:
    def __init__(self, x, y, z, vx=0, vy=0, vz=0):
        self.pos = [x, y, z]
        self.vel = [vx, vy, vz]

    @property
    def energy(self):
        return sum(abs(_) for _ in self.pos) * sum(abs(_) for _ in self.vel)

    def copy(self):
        return Moon(*self.pos, *self.vel)

    def __repr__(self):
        return f'Moon({self.pos}, {self.vel})'

def sim(moons):
    for m1, m2 in itertools.combinations(moons, 2):
        # apply gravity
        for axis in range(3):
            if m1.pos[axis] < m2.pos[axis]:
                m1.vel[axis] += 1
                m2.vel[axis] -= 1
            elif m1.pos[axis] > m2.pos[axis]:
                m1.vel[axis] -= 1
                m2.vel[axis] += 1

    # apply velocity to position
    for m in moons:
        for axis in range(3):
            m.pos[axis] += m.vel[axis]

def part1(moons):
    moons = [_.copy() for _ in moons]

    for i in range(1000):
        sim(moons)

    if DEBUG:
        for m in moons:
            print(m)

    print(sum(_.energy for _ in moons))

def part2(moons):
    # compute the period of each component of position and velocity then take
    # the lcm of those components...

    moons = [_.copy() for _ in moons]

    initials = {}
    for axis in range(3):
        initials[axis] =      [_.pos[axis] for _ in moons]
        initials[axis + 10] = [_.vel[axis] for _ in moons]

    lasts = {_: [None, None] for _ in initials}

    i = 0
    while any(None in _ for _ in lasts.values()):
        for axis in range(3):
            if i and [_.pos[axis] for _ in moons] == initials[axis]:
                if lasts[axis][0] is None:
                    lasts[axis][0] = i
                elif lasts[axis][1] is None and (i - lasts[axis][0]) > 2:
                    lasts[axis][1] = i

            if i and [_.vel[axis] for _ in moons] == initials[axis + 10]:
                if lasts[axis + 10][0] is None:
                    lasts[axis + 10][0] = i
                elif lasts[axis + 10][1] is None and (i - lasts[axis][0]) > 2:
                    lasts[axis + 10][1] = i

        sim(moons)
        i += 1

    if DEBUG:
        pprint(lasts)

    periods = []
    for axis, L in lasts.items():
        period = L[1] - L[0]
        periods.append(period)

    print(math.lcm(*periods))

def main():
    moons = parse_input()
    if '1' in sys.argv:
        part1(moons)
    if '2' in sys.argv:
        part2(moons)

if __name__ == '__main__':
    main()
