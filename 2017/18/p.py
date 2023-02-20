#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict, deque
from pprint import pprint

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    prg = [_.split() for _ in lines]
    for instr in prg:
        for i, x in enumerate(instr):
            if i > 0:
                try:
                    instr[i] = int(x)
                except:
                    pass

    return prg

def part1(prg):
    pc = 0
    regs = defaultdict(int)
    snd = None

    def load(x):
        if isinstance(x, str):
            x = regs[x]
        return x

    while 0 <= pc < len(prg):
        cmd, *rest = prg[pc]
        pc += 1

        if cmd == 'set':
            r, x = rest
            regs[r] = load(x)
        elif cmd == 'mul':
            r, x = rest
            regs[r] = regs[r] * load(x)
        elif cmd == 'add':
            r, x = rest
            regs[r] = regs[r] + load(x)
        elif cmd == 'mod':
            r, x = rest
            regs[r] = regs[r] % load(x)
        elif cmd == 'jgz':
            x, off = rest
            x = load(x)
            off = load(off)
            if x > 0:
                pc -= 1
                pc += off
        elif cmd == 'snd':
            snd = load(rest[0])
        elif cmd == 'rcv':
            x = load(rest[0])
            if x != 0:
                print(snd)
                break
        else:
            assert 0, (cmd, rest)

def g(prg, pid):
    q = deque()
    pc = 0
    regs = defaultdict(int)
    if pid == 1:
        regs['p'] = 1

    def load(x):
        if isinstance(x, str):
            x = regs[x]
        return x

    while 0 <= pc < len(prg):
        cmd, *rest = prg[pc]
        pc += 1

        if cmd == 'set':
            r, x = rest
            regs[r] = load(x)
        elif cmd == 'mul':
            r, x = rest
            regs[r] = regs[r] * load(x)
        elif cmd == 'add':
            r, x = rest
            regs[r] = regs[r] + load(x)
        elif cmd == 'mod':
            r, x = rest
            regs[r] = regs[r] % load(x)
        elif cmd == 'jgz':
            x, off = rest
            x = load(x)
            off = load(off)
            if x > 0:
                pc -= 1
                pc += off
        elif cmd == 'snd':
            snd = load(rest[0])
            x = yield snd
            if x is not None:
                q.append(x)
        elif cmd == 'rcv':
            while not q:
                x = yield
                if x is not None:
                    q.append(x)
            regs[rest[0]] = q.popleft()
        else:
            assert 0, (cmd, rest)

def part2(prg):
    g0 = g(prg, 0)
    g1 = g(prg, 1)

    cnt = 0

    x = next(g0)
    y = next(g1)
    while not (x is None and y is None):
        if y is not None:
            cnt += 1
        tmp = y
        y = g1.send(x)
        x = g0.send(tmp)

    print(cnt)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
