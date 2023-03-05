#!/usr/bin/env pypy3

import random
import sys
from collections import defaultdict

from intcode import intcode

DEBUG = sys.argv.count('-v')

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return [int(_) for _ in lines[0].split(',')]

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
            elif s.startswith('- '):
                assert key
                stuff[key].append(s[2:])
            elif s.startswith('=='):
                stuff.clear()
                stuff['room'] = ' '.join(s.split()[1:-1])
                key = None
            elif 'typing' in s:
                L = s.split()
                i = L.index('typing')
                print(L[i+1])

            if DEBUG:
                print(s)

            s = ''
        else:
            s += c

def select_item(key, visited, stuff, thing):
    mi = min(visited[(key, _)] for _ in stuff[thing])
    for item in stuff[thing]:
        if visited[(key, item)] == mi:
            visited[(key, item)] += 1
            return item

def part1(mem):
    # Eh, couldn't figure out what I was supposed to do before random picking
    # up and dropping of items worked...

    prog = intcode(mem)
    inv = []

    visited = defaultdict(int)

    def send(s):
        if DEBUG:
            print('SEND:', s)
        for c in s:
            prog.send(ord(c))
        prog.send(ord('\n'))

    while 1:
        stuff = next_input(prog)
        if stuff is None:
            break

        if DEBUG:
            print('Stuff:', dict(stuff))
            print('Items:', inv)

        key = tuple([(k, tuple(v) if isinstance(v, list) else v) for k, v in stuff.items()])

        if stuff['items'] and random.random() < 0.5:
            item = select_item(key, visited, stuff, 'items')
            if item not in ('molten lava', 'infinite loop', 'photons', 'giant electromagnet', 'escape pod'):
                inv.append(item)
                send('take ' + item)
                next_input(prog)

        if inv and random.random() < 0.1:
            item = select_item(key, visited, {'inv': inv}, 'inv')
            inv.remove(item)
            send('drop ' + item)
            next_input(prog)

        door = select_item(key, visited, stuff, 'doors')

        send(door)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)

if __name__ == '__main__':
    main()
