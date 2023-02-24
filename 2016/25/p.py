#!/usr/bin/env pypy3

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
        elif cmd == 'jnz':
            x, off = rest
            x = load(x)
            off = load(off)
            if x != 0:
                pc -= 1
                pc += off
        elif cmd == 'out':
            r = rest[0]
            yield load(r)
        else:
            assert 0, (cmd, rest)

def part1(prg):
    # just sweeping values works...
    for a in range(1000):
        regs = {_: 0 for _ in 'abcd'}
        regs['a'] = a
        out = 0
        cnt = 0
        for x in run(prg, regs):
            if x != out:
                break
            cnt += 1
            if cnt > 1000:
                break
            out = 0 if out else 1

        if cnt > 1000:
            break

    print(a)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)

if __name__ == '__main__':
    main()
