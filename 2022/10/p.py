#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    prog = []
    for line in lines:
        L = line.split()
        if len(L) > 1:
            L[1] = int(L[1])
        prog.append(L)
    return prog

def part(prog):
    # reverse and use pop to consume instructions
    prog.reverse()

    tot = 0
    crt = [['.'] * 40 for _ in range(6)]

    state = {'x': 1}
    instr = None
    cycle = 0
    while cycle := cycle + 1:
        if not instr and not prog:
            break

        if not instr:
            instr = prog.pop()
            if instr[0] == 'noop':
                instr.append(1)
            elif instr[0] == 'addx':
                instr.append(2)

        # importantly evaluate before the results of an instruction become
        # visible in the _next_ cycle...
        if (cycle + 20) % 40 == 0:
            tot += cycle * state['x']
#            print(cycle, state['x'], cycle * state['x'])

        row = (cycle-1) // 40
        col = (cycle-1) % 40
        if (state['x']-1) <= col <= (state['x']+1):
            crt[row][col] = '#'

        # decrement instruction counter and execute the instruction if it
        # reaches 0
        instr[-1] -= 1
        if instr[-1] == 0:
            if instr[0] == 'addx':
                state['x'] += int(instr[1])

            # clear to pick up new instruction...
            instr = None

    print(tot)

    for line in crt:
        print(''.join(line))

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
