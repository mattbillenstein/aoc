#!/usr/bin/env pypy3

import re
import sys
import time
from collections import defaultdict
from pprint import pprint

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    prog = []
    for line in lines:
        if mobj := re.match('^mask = (.*)$', line):
            s = mobj.groups()[0]
            mask = {}
            for i, b in enumerate(reversed(s)):
                if b == 'X':
                    b = -1
                mask[i] = int(b)
            prog.append(('mask', mask))
        elif mobj := re.match('^mem\[([0-9]+)\] = ([0-9]+)$', line):
            addr, value = mobj.groups()
            addr = int(addr)
            value = int(value)
            prog.append(('mem', addr, value))
        else:
            assert 0
    return prog

def part1(prog):
    debug(prog)
    mask = 0
    mem = {}

    for cmd in prog:
        if cmd[0] == 'mask':
            mask = cmd[1]
        elif cmd[0] == 'mem':
            _, addr, value = cmd
            for i, b in mask.items():
                if b == 1:
                    value |= 1 << i
                elif b == 0:
                    value &= (2**36-1 ^ (1 << i))

            mem[addr] = value
        else:
            assert 0, cmd

    debug(mem)
    print(sum(mem.values()))

def part2(prog):
    mask = 0
    mem = {}

    for cmd in prog:
        if cmd[0] == 'mask':
            mask = cmd[1]
        elif cmd[0] == 'mem':
            _, addr, value = cmd

            for i, b in mask.items():
                if b == 1:
                    addr |= 1 << i
                elif b == 0:
                    # nothing
                    pass

            # spin through all 'floating' addresses...
            bits = [k for k, v in mask.items() if v == -1]
            debug(bits)
            k = 2**len(bits)
            assert k < 1_000_000, k
            for i in range(0, k):
                for j, b in enumerate(bits):
                    if (i >> j) & 1:
                        # bit set to 1
                        addr |= 1 << b
                    else:
                        # bit set to 0
                        addr &= (2**36-1 ^ (1 << b))

                debug(f'{i:4d} {bin(i):>10s} {bin(addr)}')
                mem[addr] = value
        else:
            assert 0, cmd

    debug(mem)
    print(sum(mem.values()))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
