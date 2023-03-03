#!/usr/bin/env pypy3

import random
import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from intcode import intcode

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    mem = [int(_) for _ in lines[0].split(',')]
    return mem

def next_input(prog):
    stuff = defaultdict(list)
    key = None

    s = ''
    while 1:
        try:
            o = next(prog)
        except StopIteration:
            return None

        if o is None:
            continue

        if o == 'INPUT':
            return stuff

        c = chr(o)
        if c == '\n':
            if s.startswith('Doors here lead:'):
                key = 'doors'
            elif s.startswith('Items here:'):
                key = 'items'
            elif s.startswith('Items in your inventory:'):
                key = 'items'
            elif s.startswith('- '):
                assert key
                stuff[key].append(s[2:])
            elif s.startswith('=='):
                stuff.clear()
                stuff['room'] = ' '.join(s.split()[1:-1])
                key = None

            print(s)
            s = ''
        else:
            s += c

def part1(mem):
    # Eh, couldn't figure out what I was supposed to do before random picking
    # up and dropping of items worked...

    prog = intcode(mem)
    inv = []

    def send(s):
        print('SEND:', s)
        for c in s:
            prog.send(ord(c))
        prog.send(ord('\n'))

    while 1:
        stuff = next_input(prog)
        if stuff is None:
            break

        print('Stuff:', dict(stuff))
        print('Items:', inv)

        if stuff['items'] and random.random() < 0.5:
            item = random.choice(stuff['items'])
            if item not in ('molten lava', 'infinite loop', 'photons', 'giant electromagnet', 'escape pod'):
                inv.append(item)
                send('take ' + item)
                next_input(prog)

        if inv and random.random() < 0.2:
            item = random.choice(inv)
            inv.remove(item)
            send('drop ' + item)
            next_input(prog)
            
        door = random.choice(stuff['doors'])
        send(door)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
