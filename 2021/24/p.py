#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    lines = [_.split() for _ in lines]
    for line in lines:
        if line[-1] not in 'wxyz':
            line[-1] = int(line[-1])
    return lines

def run(prog, inp, regs=None):
    if not regs:
        regs = {_: 0 for _ in 'wxyz'}

    idx = 0

    for instr in prog:
        op, reg, *rest = instr
        if rest:
            v = rest[0]
            if isinstance(v, str):
                v = regs[v]

        if op == 'inp':
            regs[reg] = int(inp[idx])
            idx += 1
        elif op == 'mul':
            regs[reg] *= v
        elif op == 'add':
            regs[reg] += v
        elif op == 'mod':
            regs[reg] %= v
        elif op == 'div':
            regs[reg] //= v
        elif op == 'eql':
            regs[reg] = int(regs[reg] == v)
        else:
            assert 0, op

        if DEBUG:
            print(' '.join(str(_) for _ in instr), ' -- ', ' '.join(f'{k}:{v}' for k, v in regs.items()), inp[idx] if idx < len(inp) else '')

    return regs

def part1(prog):
    # bisect 14-digit inputs made of digits 1-9
    N = len(prog) // 14
    assert len(prog) % N == 0

    inputs = defaultdict(dict)
    inputs[14] = {0: None}

    # project backwards from valid outputs, valid inputs of w, z for a
    # sufficiently large range of input z
    for pc in range(13, -1, -1):
        start = pc * N
        sprog = prog[start:start + N]
        print('PC', pc, start, inputs[pc+1])
        print(sprog)
        for w in range(1, 10):
            for z in range(0, 10000):
                regs = {_: 0 for _ in 'wxyz'}
                regs['z'] = z
                run(sprog, str(w), regs)
                if regs['z'] in inputs[pc+1]:
                    print('IN', pc, z, w)
                    print(regs)
                    inputs[pc][z] = w

#    print(inputs)
    print(inputs[0])

    # now remove inputs that aren't outputs of the previous stage
    for pc in range(0, 13):
        d1 = inputs[pc]
        d2 = inputs[pc+1]

        print(pc)
        print(d1)
        print(d2)
        duh

def part2(data):
    pass

def test():
    regs = run([
        ['inp', 'w'],
        ['inp', 'x'],
        ['add', 'x', 'w'],
    ], '34')
    assert regs == {'w': 3, 'x': 7, 'y': 0, 'z': 0}, regs

    regs = run([
        ['inp', 'w'],
        ['inp', 'x'],
        ['add', 'x', 14],
    ], '34')
    assert regs == {'w': 3, 'x': 18, 'y': 0, 'z': 0}, regs

    regs = run([
        ['inp', 'w'],
        ['inp', 'x'],
        ['mul', 'x', 'w'],
    ], '34')
    assert regs == {'w': 3, 'x': 12, 'y': 0, 'z': 0}, regs

    regs = run([
        ['inp', 'w'],
        ['inp', 'x'],
        ['mul', 'x', -1],
    ], '34')
    assert regs == {'w': 3, 'x': -4, 'y': 0, 'z': 0}, regs

    regs = run([
        ['inp', 'w'],
        ['inp', 'x'],
        ['mod', 'x', 'w'],
    ], '47')
    assert regs == {'w': 4, 'x': 3, 'y': 0, 'z': 0}, regs

    regs = run([
        ['inp', 'w'],
        ['inp', 'x'],
        ['eql', 'x', 'w'],
    ], '33')
    assert regs == {'w': 3, 'x': 1, 'y': 0, 'z': 0}, regs

    regs = run([
        ['inp', 'w'],
        ['inp', 'x'],
        ['eql', 'x', 'w'],
    ], '34')
    assert regs == {'w': 3, 'x': 0, 'y': 0, 'z': 0}, regs

def do_bin(prog):
    for i in range(10):
        regs = run(prog, str(i))
        print(i, regs)

def main():
#    test()

    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

    if 'bin' in sys.argv:
        do_bin(data)

if __name__ == '__main__':
    main()
