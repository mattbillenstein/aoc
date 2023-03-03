#!/usr/bin/env pypy3

import sys
from collections import defaultdict

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

def run(prg, regs):
    pc = 0

    def load(x):
        if isinstance(x, str):
            x = regs[x]
        return x

    while 0 <= pc < len(prg):
        cmd, *rest = prg[pc]
        pc += 1

        if cmd == 'cpy':
            x, r = rest
            regs[r] = load(x)
        elif cmd == 'inc':
            r = rest[0]
            regs[r] += 1
        elif cmd == 'dec':
            r = rest[0]
            regs[r] -= 1
        elif cmd == 'jnz':
            x, off = rest
            x = load(x)
            if x != 0:
                pc -= 1
                pc += off
        else:
            assert 0, (cmd, rest)

def part1(prg):
    regs = defaultdict(int)
    run(prg, regs)
    print(regs['a'])

def part2(prg):
    regs = defaultdict(int)
    regs['c'] = 1
    run(prg, regs)
    print(regs['a'])

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
