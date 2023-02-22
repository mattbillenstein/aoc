#!/usr/bin/env pypy3

import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n').replace(':', '').replace('.', '') for _ in sys.stdin]
    d = {
        'state': lines[0].split()[-1],
        'steps': int(lines[1].split()[-2]),
        'states': {},
    }
    states = d['states']

    for i, line in enumerate(lines):
        if line.startswith('In state '):
            s = line.split()[-1]
            states[s] = state = []
            for offset in (i+2, i+6):
                x = [_.split()[-1] for _ in lines[offset:offset+3]]
                x[0] = int(x[0])
                x[1] = -1 if x[1] == 'left' else 1
                state.append(tuple(x))
    return d

def part1(data):
    tape = set()

    pos = 0
    state = data['state']
    states = data['states']
    steps = data['steps']

    for i in range(steps):
        v = 1 if pos in tape else 0
        write, dpos, nstate = states[state][v]

        tape.add(pos)
        if write == 0:
            tape.remove(pos)

        pos += dpos
        state = nstate

    print(len(tape))

def main():
    data = parse_input()
    part1(data)

if __name__ == '__main__':
    main()
