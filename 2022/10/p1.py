#!/usr/bin/env python3

import sys

def main(argv):
    with open(argv[1]) as f:
        lines = [_.strip('\r\n') for _ in f]

    # reverse and use pop to consume instructions
    lines.reverse()

    tot = 0
    crt = [['.'] * 40 for _ in range(6)]

    state = {'x': 1}
    instr = None
    cycle = 0
    while cycle := cycle + 1:
        if not instr and not lines:
            break

        if not instr:
            instr = lines.pop().split()
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
    print()

    for line in crt:
        print(''.join(line))

if __name__ == '__main__':
    main(sys.argv)
