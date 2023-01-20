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

    outputs = defaultdict(set)

    zs = set([0])
    for pc in range(0, 14):
        print(pc, zs)
        start = pc * N
        sprog = prog[start:start + N]
        for w in range(1, 10):
            for z in zs:
                regs = {_: 0 for _ in 'wxyz'}
                regs['z'] = z
                run(sprog, str(w), regs)
                if abs(regs['z']) < 200000:
                    outputs[pc].add(regs['z'])

        zs = outputs[pc]

    assert 0 in outputs[13]

    newoutputs = defaultdict(set)
    newoutputs[14] = set([0])

    # now go backwards constraining inputs on outputs
    for pc in range(13, -1, -1):
        inputs = outputs[pc-1]
        start = pc * N
        sprog = prog[start:start + N]
        for w in range(1, 10):
            for z in inputs:
                regs = {_: 0 for _ in 'wxyz'}
                regs['z'] = z
                run(sprog, str(w), regs)
                if regs['z'] in newoutputs[pc+1]:
                    newoutputs[pc].add(z)

    ws = defaultdict(set)

    # now forwards, every step that generates a valid z at that step is a valid
    # digit...
    zs = set([0])
    for pc in range(0, 14):
        start = pc * N
        sprog = prog[start:start + N]
        for w in range(1, 10):
            for z in zs:
                regs = {_: 0 for _ in 'wxyz'}
                regs['z'] = z
                run(sprog, str(w), regs)
                if regs['z'] in newoutputs[pc]:
                    ws[pc].add(w)

        zs = newoutputs[pc]

    print(ws)

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
