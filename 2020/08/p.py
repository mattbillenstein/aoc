#!/usr/bin/env pypy3

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
    lines = [_.split() for _ in lines]
    lines = [(_[0], int(_[1])) for _ in lines]
    return lines

def run(prog):
    executed = []
    acc = 0
    pc = 0
    while 1:
        if pc >= len(prog):
            return pc, acc, 0, executed

        instr, v = prog[pc]
        if pc in executed:
            return pc, acc, 1, executed
            break

        executed.append(pc)

        if instr == 'nop':
            pass
        elif instr == 'acc':
            acc += v
        elif instr == 'jmp':
            pc += v
            continue
        else:
            assert 0, instr

        pc += 1


def part1(prog):
    pc, acc, loop, executed = run(prog)
    assert loop
    print(acc)

def part2(prog):
    # Just loop over all jmp/nop instructions and swap them one at a time until
    # the program terminates...
    for i, item in enumerate(prog):
        if item[0] == 'jmp':
            prog[i] = ('nop', item[1])
        elif item[0] == 'nop':
            prog[i] = ('jmp', item[1])

        pc, acc, loop, _ = run(prog)
        if not loop:
            print(acc)
            break

        prog[i] = item

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
