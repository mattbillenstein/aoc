#!/usr/bin/env pypy3

import itertools
import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    machines = []
    for line in lines:
        line = line.translate({ord(_): None for _ in '[](){}'})

        lights, *buttons, joltages = line.split()

        m = {
            'lights': [1 if _ == '#' else 0 for _ in lights],
            'buttons': [tuple(int(_) for _ in b.split(',')) for b in buttons],
            'joltages': [int(_) for _ in joltages.split(',')],
        }
        machines.append(m)

    return (machines,)

def part1(machines):
    # just check all possible presses at p until we match lights
    tot = 0

    for m in machines:
        # convenient to turn buttons / lights into a single int here to use xor
        # to flip them
        lights = 0
        for i, v in enumerate(m['lights']):
            lights |= (v << i)

        buttons = []
        for b in m['buttons']:
            x = 0
            for el in b:
                x |= 1 << el
            buttons.append(x)

        found = -1
        for p in range(100):
            for pressed in itertools.product(buttons, repeat=p):
                L = 0
                for b in pressed:
                    L ^= b
                if L == lights:
                    found = p
                    break
            if found > -1:
                break
        assert found > -1
        tot += found

    print(tot)

def part2(machines):
    # Linear algebra, fixme, write some code that can solve systems of
    # equations like this...
    from z3 import Optimize, Int, Sum, sat

    tot = 0

    for m in machines:
        buttons = m['buttons']
        joltages = m['joltages']

        opt = Optimize()
        vars = [Int(f'b{i}') for i, _ in enumerate(buttons)]
        for v in vars:
            opt.add(v >= 0)
        
        for ji, j in enumerate(m['joltages']):
            vs = []
            for bi, b in enumerate(buttons):
                if ji in b:
                    vs.append(vars[bi])
            opt.add(Sum(vs) == j)

        opt.minimize(Sum(vars))

        assert opt.check() == sat

        model = opt.model()
        presses = sum(model[_].as_long() for _ in model)
        tot += presses

    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
