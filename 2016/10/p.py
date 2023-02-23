#!/usr/bin/env pypy3

import sys
from collections import defaultdict

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    cmds = []
    for line in lines:
        L = line.split()
        if 'gives' in L:
            cmds.append(('give', (int(L[1]), L[5], int(L[6]), L[10], int(L[11]))))
        else:
            cmds.append(('value', (int(L[1]), int(L[5]))))
    return cmds

def part(cmds):
    outputs = defaultdict(list)
    bots = defaultdict(list)

    for cmd, opts in cmds:
        if cmd == 'value':
            value, bot = opts
            bots[bot].append(value)

    found = True
    while found:
        found = False
        for cmd, opts in cmds:
            if cmd == 'give':
                bot, tlow, lowid, thigh, highid = opts
                if len(bots[bot]) == 2:
                    found = True
                    low, high = sorted(bots[bot])

                    if (low, high) == (17, 61):
                        botid = bot

                    bots[bot] = []
                    if tlow == 'bot':
                        bots[lowid].append(low)
                    else:
                        outputs[lowid].append(low)
                    if thigh == 'bot':
                        bots[highid].append(high)
                    else:
                        outputs[highid].append(high)

    print(botid)

    x = 1
    for i in (0, 1, 2):
        x *= outputs[i][0]
    print(x)

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
