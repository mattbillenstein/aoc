#!/usr/bin/env pypy3

import math
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
    mem = [int(_) for _ in lines[0].split(',')]
    return mem

def run(mem):
    pc = 0
    debug(pc, mem)
    while mem[pc] != 99:
        if mem[pc] == 1:
            mem[mem[pc+3]] = mem[mem[pc+1]] + mem[mem[pc+2]]
            pc += 4
        elif mem[pc] == 2:
            mem[mem[pc+3]] = mem[mem[pc+1]] * mem[mem[pc+2]]
            pc += 4
        else:
            assert 0, ('Invalid instruction', mem[pc])

        debug(pc, mem)

def part1(mem):
    mem = list(mem)
    mem[1] = 12
    mem[2] = 2
    run(mem)
    print(mem[0])

def part2(mem):
    for noun in range(100):
        for verb in range(100):
            nmem = list(mem)
            nmem[1] = noun
            nmem[2] = verb
            run(nmem)

            debug(noun, verb, nmem[0])

            if nmem[0] == 19690720:
                print(noun * 100 + verb)
                return

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
