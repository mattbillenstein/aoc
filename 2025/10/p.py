#!/usr/bin/env pypy3

import itertools
import math
import random
import sys
import time
from collections import defaultdict
from functools import lru_cache
from pprint import pprint

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    machines = []
    for line in lines:
        for c in '[](){}':
            line = line.replace(c, '')

        lights, *buttons, joltages = line.split()

        m = {}
        machines.append(m)
        m['lights'] = 0
        for i, c in enumerate(lights):
            if c == '#':
                m['lights'] = m['lights'] | (1 << i)

        m['buttons'] = []
        for b in buttons:
            x = 0
            for c in b.split(','):
                x |= 1 << int(c)
            m['buttons'].append(x)

        m['joltages'] = [int(_) for _ in joltages.split(',')]

    return (machines,)

def part1(machines):
    tot = 0
    for m in machines:
        lights = m['lights']
        found = -1
        for p in range(100):
            for buttons in itertools.product(m['buttons'], repeat=p):
                L = 0
                for b in buttons:
                    L ^= b
                if L == lights:
                    found = p
                    break
            if found > -1:
                break
        assert found > -1
        tot += found
    print(tot)

def it(x, i, j):
    for k in range(i, j+1):
        yield (x, k)

def compute_joltage(presses, N):
    J = [0] * N
    for b, p in presses:
        for i in range(N):
            if b & (1 << i):
                J[i] += p
    return J

def solve_joltages(idx, joltages, buttons, pressed, best):
    print(idx, joltages, buttons, pressed, best)

    joltage = joltages[idx]
    N = len(joltages)
    ranges = {_: joltage for _ in buttons if _ & (1 << idx)}
    other_buttons = [_ for  _ in buttons if _ not in ranges]

    last = None
    if len(ranges) > 1:
        last, _ = ranges.popitem()

    its = [it(b, 0, j) for b, j in ranges.items()]
    for tup in itertools.product(*its):
        if last:
            tup = tup + ((last, joltage - sum(_[1] for _ in tup)),)
        next_pressed = pressed + tup
        J = compute_joltage(next_pressed, N)
        if any(x > y for x, y in zip(J, joltages)):
            continue

        if J == joltages:
            tot = sum(_[1] for _ in next_pressed)
            if tot < best[0]:
                print('BEST', next_pressed, J, joltages)
                best[0] = tot

        elif J[idx] == joltages[idx]:
            solve_joltages(idx+1, joltages, other_buttons, next_pressed, best)

def part2(machines):
    tot = 0

    for m in machines:
        best = 1_000_000
        buttons = m['buttons']
        joltages = m['joltages']
        N = len(joltages)
        buttons_by_idx = {i: [_ for _ in buttons if _ & (1 << i)] for i in range(N)}

        # 20:
        #   20878
        #   20855
        #   20860
        #
        # 100:
        #   20796
        #
        # 1000:
        #   20772

        J = [0] * N
        presses = {b: 0 for b in buttons}

        runs = defaultdict(int)
        for _ in range(5000):
            if _ == 100 and len(runs) == 1:
                break

            b = random.choice(buttons)
            if presses[b] >= 2:
                p = presses[b] // 2
                presses[b] -= p
                for j in range(N):
                    if b & (1 << j):
                        J[j] -= p

            while J != joltages:
                #print(joltages, J, presses, sum(presses.values()))
                for i in range(N):
                    if J[i] < joltages[i]:
                        # press
                        b = random.choice(buttons_by_idx[i])
                        presses[b] += 1
                        for j in range(N):
                            if b & (1 << j):
                                J[j] += 1
                    elif J[i] > joltages[i]:
                        # unpress
                        b = random.choice(buttons_by_idx[i])
                        if presses[b] >= 1:
                            presses[b] -= 1
                            for j in range(N):
                                if b & (1 << j):
                                    J[j] -= 1

            p = sum(presses.values())
            runs[p] += 1

        best = min(runs)

        if 0:
            # sweep each button 10% around the number of total presses
            delta = best // 5
            print(joltages, J, presses, sum(presses.values()))

            its = []
            for b, n in presses.items():
                its.append(it(b, max(0, n-delta), n+delta))

            for tup in itertools.product(*its):
                J = compute_joltage(tup, N)
                p = sum(_[1] for _ in tup)
                if J == joltages and p < best:
                    print(J, joltages, best, p)

        print(buttons, joltages, best, runs)
        tot += best

    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
