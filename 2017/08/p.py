#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    instr = []
    for line in lines:
        L = line.split()
        L[2] = int(L[2])
        L[6] = int(L[6])
        instr.append(L)
        
    return instr

def part(instr):
    regs = {}
    mx = 0
    for inst in instr:
        reg, op, amt, _, oreg, cmp, v = inst
        if not reg in regs:
            regs[reg] = 0
        if not oreg in regs:
            regs[oreg] = 0

        assert op in ('inc', 'dec')
        if op == 'dec':
            amt = -amt

        if cmp == '>=':
            if regs[oreg] >= v:
                regs[reg] += amt
        elif cmp == '<=':
            if regs[oreg] <= v:
                regs[reg] += amt
        elif cmp == '>':
            if regs[oreg] > v:
                regs[reg] += amt
        elif cmp == '<':
            if regs[oreg] < v:
                regs[reg] += amt
        elif cmp == '!=':
            if regs[oreg] != v:
                regs[reg] += amt
        elif cmp == '==':
            if regs[oreg] == v:
                regs[reg] += amt
        else:
            assert 0, cmp

        if regs[reg] > mx:
            mx = regs[reg]

    print(max(regs.values()))
    print(mx)

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
