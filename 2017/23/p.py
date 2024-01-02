#!/usr/bin/env pypy3

import sys
from collections import defaultdict

DEBUG = sys.argv.count('-v')

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
    regs = {c: 0 for c in 'abcdefgh'}
    cmds = defaultdict(int)

    while 0 <= pc < len(prg):
        if DEBUG > 0:
            print(pc, prg[pc], regs)

        cmd, r, x = prg[pc]
        cmds[cmd] += 1
        x = regs.get(x, x)

        pc += 1

        if cmd == 'set':
            regs[r] = x
        elif cmd == 'sub':
            regs[r] -= x
        elif cmd == 'jnz':
            r = regs.get(r, r)
            if r != 0:
                pc += x - 1
        elif cmd == 'mod':
            regs[r] %= x
        elif cmd == 'mul':
            regs[r] *= x
        elif cmd == 'add':
            regs[r] += x
        else:
            assert 0, (cmd, rest)

    print(cmds['mul'])

def part2(prg):
    # the program basically counts all numbers [b..c] that are not prime, see
    # part2a
    #
    # Running input-mod.txt here, we shunt the outer loop and use the inner
    # loop with mod to compute if the current value of b is not prime and all
    # the other instructions work as normal to increment h on non-primes...

    pc = 0
    regs = {c: 0 for c in 'abcdefgh'}
    regs['a'] = 1

    cmds = defaultdict(int)

    while 0 <= pc < len(prg):
        if DEBUG:
            print(f'{pc:2d} {str(prg[pc]):22s} {regs}')
            cmds[cmd] += 1

        cmd, r, x = prg[pc]
        x = regs.get(x, x)

        pc += 1

        if cmd == 'sub':
            regs[r] -= x
        elif cmd == 'set':
            regs[r] = x
        elif cmd == 'jnz':
            r = regs.get(r, r)
            if r != 0:
                pc += x - 1
        elif cmd == 'mod':
            regs[r] %= x
        elif cmd == 'mul':
            regs[r] *= x
        elif cmd == 'add':
            regs[r] += x
        else:
            assert 0, (cmd, rest)

    if DEBUG:
        print(cmds)

    print(regs['h'])

def is_prime(n):
    """"pre-condition: n is a nonnegative integer
    post-condition: return True if n is prime and False otherwise."""
    if n < 2: 
         return False;
    if n % 2 == 0:             
         return n == 2  # return False
    k = 3
    while k*k <= n:
         if n % k == 0:
             return False
         k += 2
    return True

def part2a(prg):
    b = c = 81
    b *= 100
    b += 100_000
    c = b + 17_000

    print(sum(1 for _ in range(b, c+1, 17) if not is_prime(_)))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)
    if '2a' in sys.argv:
        part2a(data)

if __name__ == '__main__':
    main()
