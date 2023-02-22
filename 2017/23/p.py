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
    cnt = 0

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
            regs[r] *= load(x)
            cnt += 1
        elif cmd == 'add':
            r, x = rest
            regs[r] += load(x)
        elif cmd == 'sub':
            r, x = rest
            regs[r] -= load(x)
        elif cmd == 'jnz':
            x, off = rest
            x = load(x)
            off = load(off)
            if x != 0:
                pc -= 1
                pc += off
        else:
            assert 0, (cmd, rest)

    print(cnt)

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

    def load(x):
        if isinstance(x, str):
            x = regs[x]
        return x

    while 0 <= pc < len(prg):
        if DEBUG:
            print(f'{pc:2d} {str(prg[pc]):22s} {regs}')

        cmd, *rest = prg[pc]
        pc += 1

        if cmd == 'set':
            r, x = rest
            regs[r] = load(x)
        elif cmd == 'mul':
            r, x = rest
            regs[r] *= load(x)
        elif cmd == 'add':
            r, x = rest
            regs[r] += load(x)
        elif cmd == 'sub':
            r, x = rest
            regs[r] -= load(x)
        elif cmd == 'mod':
            r, x = rest
            regs[r] %= load(x)
        elif cmd == 'jnz':
            x, off = rest
            x = load(x)
            off = load(off)
            if x != 0:
                pc -= 1
                pc += off
        else:
            assert 0, (cmd, rest)

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
