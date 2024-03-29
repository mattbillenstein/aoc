#!/usr/bin/env pypy3

import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]

    prog = []
    ipreg = None

    for line in lines:
        if line[0] == '#':
            ipreg = int(line.split()[1])
        else:
            x = line.split()
            for i in range(1, 4):
                x[i] = int(x[i])
            prog.append(tuple(x))

    return ipreg, prog

def execute(inst, regs):
    op, a, b, c = inst

    if op[0] == 'a':
        if op == 'addi':
            regs[c] = regs[a] + b
        #elif op == 'addr':
        else:
            regs[c] = regs[a] + regs[b]
    elif op[0] == 'b':
        if op == 'bani':
            regs[c] = regs[a] & b
        elif op == 'banr':
            regs[c] = regs[a] & regs[b]
        elif op == 'borr':
            regs[c] = regs[a] | regs[b]
        #elif op == 'bori':
        else:
            regs[c] = regs[a] | b
    elif op[0] == 's':
        if op == 'seti':
            regs[c] = a
        #elif op == 'setr':
        else:
            regs[c] = regs[a]
    elif op[0] == 'm':
        if op == 'muli':
            regs[c] = regs[a] * b
        #elif op == 'mulr':
        else:
            regs[c] = regs[a] * regs[b]
    elif op[0] == 'g':
        if op == 'gtrr':
            regs[c] = int(regs[a] > regs[b])
        elif op == 'gtir':
            regs[c] = int(a > regs[b])
        #elif op == 'gtri':
        else:
            regs[c] = int(regs[a] > b)

    elif op[0] == 'e':
        if op == 'eqrr':
            regs[c] = int(regs[a] == regs[b])
        elif op == 'eqir':
            regs[c] = int(a == regs[b])
        #elif op == 'eqri':
        else:
            regs[c] = int(regs[a] == b)
    else:
        assert 0

def run(ipreg, prog, regs):
    ip = 0
    while 0 <= ip < len(prog):
        regs[ipreg] = ip
        if DEBUG:
            print(f'{ip:2d} {str(prog[ip]):25s} {regs}')
        if ip == 28:
            yield regs[4]
        execute(prog[ip], regs)
        ip = regs[ipreg]
        ip += 1

def part(ipreg, prog):
    # at instruction 28 is eqrr - we can just peek values out of the expected
    # value at reg4 until the sequence repeats...
    seen = set()
    last = None

    regs = [0] * 6
    for value in run(ipreg, prog, regs):
        if value in seen:
            print(last)
            return

        if last is None:
            print(value)

        last = value
        seen.add(value)
    
def main():
    data = parse_input()
    part(*data)

if __name__ == '__main__':
    main()
