#!/usr/bin/env pypy3

import random
import itertools
import math
import sys
import time
from collections import defaultdict, deque
from pprint import pprint

from intcode import intcode

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    mem = [int(_) for _ in lines[0].split(',')]
    return mem

class Computer:
    def __init__(self, id, mem, bus):
        self.id = id
        self.prog = intcode(mem)
        self.bus = bus
        self.q = bus[id]

    def run(self):
        # run up to first yield
        next(self.prog)

        out = deque()
        def send(value):
            sent = False
            while not sent:
                x = self.prog.send(None)
                if x == 'INPUT':
                    x = self.prog.send(value)
                    sent = True

                if x != 'INPUT':
                    out.append(x)
                    if len(out) == 3:
                        addr = out.popleft()
                        other = self.bus[addr]
                        other.append(out.popleft())
                        other.append(out.popleft())
            
        send(self.id)

        while 1:
            if self.q:
                send(self.q.popleft())
                send(self.q.popleft())
            else:
                send(-1)

            yield
        
def part1(mem):
    N = 50
    bus = defaultdict(deque)
    progs = [Computer(_, mem, bus) for _ in range(N)]
    gens = [_.run() for _ in progs]

    while not bus[255]:
        for g in gens:
            next(g)
        
    print(bus[255][1])

def part2(mem):
    N = 50
    bus = defaultdict(deque)
    progs = [Computer(_, mem, bus) for _ in range(N)]
    gens = [_.run() for _ in progs]

    nat = bus[255]
    cnt = 0

    while 1:
        for g in gens:
            next(g)

        for i in range(3, len(nat), 2):
            if nat[i] == nat[i-2]:
                print(nat[i])
                return
        
        if not any(bus[_] for _ in range(N)) and nat:
            cnt += 1
            # make sure we've been been empty for more than just the last
            # cycle...
            if cnt > 3:
                cnt = 0

                # send the last packet to addr 0
                bus[0].append(nat[-2])
                bus[0].append(nat[-1])

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
