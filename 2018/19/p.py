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

    if op == 'addr':
        regs[c] = regs[a] + regs[b]
    elif op == 'addi':
        regs[c] = regs[a] + b
    elif op == 'mulr':
        regs[c] = regs[a] * regs[b]
    elif op == 'muli':
        regs[c] = regs[a] * b
    elif op == 'banr':
        regs[c] = regs[a] & regs[b]
    elif op == 'bani':
        regs[c] = regs[a] & b
    elif op == 'borr':
        regs[c] = regs[a] | regs[b]
    elif op == 'bori':
        regs[c] = regs[a] | b
    elif op == 'setr':
        regs[c] = regs[a]
    elif op == 'seti':
        regs[c] = a
    elif op == 'gtir':
        regs[c] = int(a > regs[b])
    elif op == 'gtri':
        regs[c] = int(regs[a] > b)
    elif op == 'gtrr':
        regs[c] = int(regs[a] > regs[b])
    elif op == 'eqir':
        regs[c] = int(a == regs[b])
    elif op == 'eqri':
        regs[c] = int(regs[a] == b)
    elif op == 'eqrr':
        regs[c] = int(regs[a] == regs[b])
    else:
        assert 0

def run(ipreg, prog, regs):
    ip = 0
    while 0 <= ip < len(prog):
        regs[ipreg] = ip
        execute(prog[ip], regs)
        ip = regs[ipreg]
        ip += 1

def part1(ipreg, prog):
    regs = [0] * 6
    run(ipreg, prog, regs)
    print(regs[0])
    
def part2(ipreg, prog):
    regs = [0] * 6
    regs[0] = 1

    # deduced this is adding the factors of 10551347 into register 0 from
    # watching registers...
    #
    # factors are:
    # 
    #  1 10551347
    # 73   144539
    #
    # sum([1, 10551347, 73, 144539]) = 10695960  <-- the answer

    ip = 0
    while 0 <= ip < len(prog):
        regs[ipreg] = ip

        if DEBUG:
            print(prog[ip], regs)

        # hack the two counter registers to skip a bunch of steps that don't
        # work...
        if regs[3] == 3 and regs[4] == 10551347:
            if regs[5] == 75:
                regs[5] = 144530
            elif regs[5] == 144550:
                regs[5] = 10551340

            if regs[1] == 75:
                regs[1] = 144530
            elif regs[1] == 144550:
                regs[1] = 10551340

        execute(prog[ip], regs)
        ip = regs[ipreg]
        ip += 1

    print(regs[0])

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)


if __name__ == '__main__':
    main()
