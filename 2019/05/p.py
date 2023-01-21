#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    mem = [int(_) for _ in lines[0].split(',')]
    return mem

def run(mem, input=None):
    mem = list(mem)
    input = input or []
    input.reverse()
    output = []

    pc = 0
    while mem[pc] != 99:
        instr = mem[pc]
        op = instr % 100
        mode = [instr // 100 % 10, instr // 1000 % 10, instr // 10000 % 10]

        debug(op, mode, mem[pc:pc+4])

        def param(i):
            v = mem[pc+i+1]
            if mode[i] == 0:
                v = mem[v]
            return v

        if op == 1:
            # add
            mem[mem[pc+3]] = param(0) + param(1)
            pc += 4
        elif op == 2:
            # mul
            mem[mem[pc+3]] = param(0) * param(1)
            pc += 4
        elif op == 3:
            # input
            mem[mem[pc+1]] = input.pop()
            pc += 2
        elif op == 4:
            # output
            x = param(0)
            debug('OUT', x)
            output.append(x)
            pc += 2
        elif op == 5:
            # jump if true
            if param(0) != 0:
                pc = param(1)
            else:
                pc += 3
        elif op == 6:
            # jump if false
            if param(0) == 0:
                pc = param(1)
            else:
                pc += 3
        elif op == 7:
            # <
            mem[mem[pc+3]] = int(param(0) < param(1))
            pc += 4
        elif op == 8:
            # ==
            mem[mem[pc+3]] = int(param(0) == param(1))
            pc += 4
        else:
            assert 0, ('Invalid instruction', op)

    return output

def part1(mem):
    out = run(mem, [1])
    print(out)

def part2(mem):
    out = run(mem, [5])
    print(out)

def test(mem):
    out = run(mem, [7])
    print(out)
    print()
    out = run(mem, [8])
    print(out)
    print()
    out = run(mem, [9])
    print(out)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)
    if 'test' in sys.argv:
        test(data)

if __name__ == '__main__':
    main()
