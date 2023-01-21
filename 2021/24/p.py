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

def recurse(num, prog, z):
    # eh, this is slow, we could pick apart the asm and optimize, but yolo
    digit = len(num)
    for w in range(1, 10):
        sw = str(w)
        regs = {_: 0 for _ in 'wxy'}
        regs['z'] = z
        run(prog[digit], sw, regs)
        if digit == 13 and regs['z'] == 0:
            yield num + sw
        # hard-code number here - if it's too small, we won't find z=0 at the
        # end...
        elif digit < 13: # and regs['z'] < 500_000:
            for x in recurse(num + sw, prog, regs['z']):
                yield x

def part(prog):
    DIGITS = 14
    N = len(prog) // DIGITS
    assert len(prog) % N == 0

    prog = [prog[_*N:_*N+N] for _ in range(DIGITS)]

    mn = '9' * DIGITS
    mx = '1' * DIGITS
    cnt = 0
    for x in recurse('', prog, 0):
        cnt += 1
        print(x)
        if x < mn:
            mn = x
        elif x > mx:
            mx = x

    print(mn, mx, cnt)

def do_bin(prog):
    for i in range(10):
        regs = run(prog, str(i))
        print(i, regs)

def test_monad(prog):
    x = sys.argv[2]
    regs = run(prog, x)
    print(regs)

def test_alu():
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

def main():
    if 'bin' in sys.argv:
        data = parse_input()
        do_bin(data)
    elif 'monad' in sys.argv:
        data = parse_input()
        monad(data)
    elif 'test' in sys.argv:
        test_alu()
    else:
        data = parse_input()
        part(data)

if __name__ == '__main__':
    main()
