#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from graph import bfs
from grid import Grid

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    grid = Grid(lines)
    return grid

def ro(o):
    if isinstance(o, Unit):
        return (o.pt[1], o.pt[0])
    elif isinstance(o, tuple):
        return (o[1], o[0])
    else:
        assert 0

class Unit:
    def __init__(self, type, pt):
        self.type = type
        self.pt = pt

        self.hp = 200
        self.ap = 3

    def move(self, grid, units):
        for pt in grid.neighbors4(self.pt):
            c = grid.getc(pt)
            if c in 'GE' and c != self.type:
                # already in range, don't move
                return

        def neighbors(pt):
            return [_ for _ in grid.neighbors4(pt) if grid.get(_) == 0]

        done = True

        ends = set()
        for unit in units:
            if unit.hp > 0 and unit.type != self.type:
                ends.update(neighbors(unit.pt))
                done = False

        if done:
            return True
        
        pts = neighbors(self.pt)
        options = []
        for pt in pts:
            found = bfs(pt, neighbors, ends)
            if found:
                options.append((pt, min(_[1] for _ in found)))

        if options:
            options.sort(key=lambda x: (x[1], x[0][1], x[0][0]))
            grid.set(self.pt, 0)
            self.pt = options[0][0]
            grid.setc(self.pt, self.type)

        return False

    def attack(self, grid, units):
        pts = grid.neighbors4(self.pt)

        targets = []
        for unit in units:
            if unit.pt in pts and unit.type != self.type and unit.hp > 0:
                targets.append(unit)

        if not targets:
            return

        targets.sort(key=lambda x: (x.hp, x.pt[1], x.pt[0]))

        unit = targets[0]
            
        unit.hp -= self.ap
        if unit.hp <= 0:
            # remove from grid, will be skipped in units list
            grid.set(unit.pt, 0)

    def __repr__(self):
        return f'{self.type}({self.pt}, {self.hp})'

def run(grid, eap=3):
    units = []
    for pt in grid:
        c = grid.getc(pt)
        if c in 'GE':
            unit = Unit(c, pt)
            if c == 'E':
                unit.ap = eap
            units.append(unit)

    rounds = 0
    done = False
    while 1:
        units.sort(key=ro)

        if DEBUG:
            print()
            print(rounds)
            grid.print()

            for unit in units:
                if unit.hp <= 0:
                    continue
    #            print(unit)

        for unit in units:
            if unit.hp <= 0:
                continue

            done = unit.move(grid, units)
            if done:
                break
            unit.attack(grid, units)

        if done:
            break

        rounds += 1

    if DEBUG:
        print()
        print(rounds)
        grid.print()

    points = sum(_.hp for _ in units if _.hp > 0)

    for unit in units:
        if unit.hp > 0:
            winner = unit.type
            break

    return rounds, points, rounds * points, winner

def part1(grid):
    print(run(grid))

def part2(grid):
    eap = 3
    while 1:
        tup = run(grid.copy(), eap)
        print(tup, eap)
        if tup[-1] == 'E':
            break
        eap += 1


def main():
    grid = parse_input()
    if '1' in sys.argv:
        part1(grid.copy())
    if '2' in sys.argv:
        part2(grid.copy())

if __name__ == '__main__':
    main()
