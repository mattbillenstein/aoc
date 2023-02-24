#!/usr/bin/env pypy3

import copy
import sys

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

def run(prg, regs):
    pc = 0

    def load(x):
        if isinstance(x, str):
            x = regs[x]
        return x

    while 0 <= pc < len(prg):
        cmd, *rest = prg[pc]
        debug(f'{pc:2d} {cmd} {str(rest):10s} {regs}')
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
        elif cmd == 'mul':
            x, r = rest
            regs[r] *= load(x)
        elif cmd == 'jnz':
            x, off = rest
            x = load(x)
            off = load(off)
            if x != 0:
                pc -= 1
                pc += off
        elif cmd == 'tgl':
            off = load(rest[0])
            try:
                instr = prg[pc - 1 + off]
                debug('TOGGLE before', instr)
                if len(instr) == 2:
                    if instr[0] == 'inc':
                        instr[0] = 'dec'
                    else:
                        instr[0] = 'inc'
                elif len(instr) == 3:
                    if instr[0] == 'jnz':
                        instr[0] = 'cpy'
                    else:
                        instr[0] = 'jnz'
                debug('TOGGLE after', instr)
            except IndexError:
                pass
        else:
            assert 0, (cmd, rest)

def part1(prg):
    regs = {_: 0 for _ in 'abcd'}
    regs['a'] = 7
    run(prg, regs)
    print(regs['a'])

def part2(prg):
    # use input-mod.txt for this one - basically the inner loop is doing a
    # multiply, so replace those instructions with a mul instruction, and put 0
    # in c and 1 in d to break the repeating loops behind that...
    regs = {_: 0 for _ in 'abcd'}
    regs['a'] = 12
    run(prg, regs)
    print(regs['a'])

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(copy.deepcopy(data))
    if '2' in sys.argv:
        part2(copy.deepcopy(data))

if __name__ == '__main__':
    main()
