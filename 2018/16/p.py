#!/usr/bin/env pypy3

import itertools
import json
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
    tests = []

    for i in range(2, len(lines)):
        if lines[i] != '' and lines[i-1] == '' and lines[i-2] == '':
            idx = i
            program = [tuple([int(_) for _ in x.split()]) for x in lines[i:]]
            break

    lines = lines[:idx]

    i = 0
    while i < len(lines):
        if lines[i].startswith('Before:'):
            before = json.loads(lines[i].split(': ')[1])
            instr = [int(_) for _ in lines[i+1].split()]
            after = json.loads(lines[i+2].split(': ')[1])
            tests.append((instr, before, after))
            i += 2

        i += 1

    return tests, program

OPS = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori', 'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']

def execute(inst, regs):
    op, a, b, c = inst

    op = OPS[op]

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

def run(tests, program):
    mapping = defaultdict(list)

    # part1 - number of tests that match 3 or more instructions
    tot = 0
    for t in tests:
        instr, before, after = t
        s = set()

        cnt = 0
        for op in range(16):
            i = [op] + instr[1:]
            regs = list(before)
            execute(i, regs)
            if regs == after:
                cnt += 1
                s.add(op)

        if s:
            mapping[instr[0]].append(s)

        if cnt >= 3:
            tot += 1

    print(tot)

    # part2 - compute actual instruction mapping from executed tests
    mapping = dict(mapping)

    # and together all sets of matching ops for each op, some instructions will
    # be fully matched after this...
    for op in list(mapping):
        L = mapping[op]
        s = L[0]
        for s2 in L[1:]:
            s &= s2
        mapping[op] = s

    # Remove set ops from non-set ones until we're fully mapped
    while any(isinstance(_, set) for _ in mapping.values()):
        remove = []
        for op in list(mapping):
            v = mapping[op]
            if isinstance(v, set) and len(v) == 1:
                mapping[op] = x = v.pop()
                remove.append(x)

        for x in remove:
            for v in mapping.values():
                if isinstance(v, set) and x in v:
                    v.remove(x)

    # set actual instruction mapping
    OPS[:] = [OPS[mapping[_]] for _ in range(16)]

    # execute test program and emit register0
    regs = [0, 0, 0, 0]
    for instr in program:
        execute(instr, regs)
    print(regs[0])

def main():
    data = parse_input()
    run(*data)

if __name__ == '__main__':
    main()
