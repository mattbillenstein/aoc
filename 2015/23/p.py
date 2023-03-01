#!/usr/bin/env pypy3

import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    prg = []
    for line in lines:
        for c in ',+':
            line = line.replace(c, '')
        L = line.split()
        if L[0][0] == 'j':
            L[-1] = int(L[-1])
        prg.append(tuple(L))
    return prg

def run(prg, regs):
    pc = 0
    while 0 <= pc < len(prg):
        cmd, *rest = prg[pc]
        debug(pc, cmd, rest, regs)
        pc += 1

        if cmd == 'inc':
            regs[rest[0]] += 1
        elif cmd == 'tpl':
            regs[rest[0]] *= 3
        elif cmd == 'hlf':
            regs[rest[0]] //= 2
        elif cmd == 'jio':
            if regs[rest[0]] == 1:
                pc -= 1
                pc += rest[1]
        elif cmd == 'jie':
            if regs[rest[0]] % 2 == 0:
                pc -= 1
                pc += rest[1]
        elif cmd == 'jmp':
            pc -= 1
            pc += rest[0]
        else:
            assert 0, cmd

def part1(prg):
    regs = {'a': 0, 'b': 0}
    run(prg, regs)
    print(regs['b'])

def part2(prg):
    regs = {'a': 1, 'b': 0}
    run(prg, regs)
    print(regs['b'])

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
