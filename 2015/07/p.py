#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    cmds = []
    for line in lines:
        L = line.split()
        for i in range(len(L)):
            if L[i].isdigit():
                L[i] = int(L[i])
        if L[0] == 'NOT':
            cmds.append((L[0], (L[1], L[3])))
        elif L[1] == '->':
            cmds.append(('ASSIGN', (L[0], L[2])))
        else:
            cmds.append((L[1], (L[0], L[2], L[4])))
    return cmds

def run(cmds):
    ctx = {}

    def load(x):
        if isinstance(x, str):
            x = ctx.get(x)
        return x

    while cmds:
        ncmds = []
        for tup in cmds:
            cmd, opts = tup

            ins = [load(_) for _ in opts[:-1]]
            out = opts[-1]

            if None in ins:
                ncmds.append(tup)
                continue

            if cmd == 'ASSIGN':
                ctx[out] = ins[0]
            elif cmd == 'AND':
                ctx[out] = ins[0] & ins[1]
            elif cmd == 'OR':
                ctx[out] = ins[0] | ins[1]
            elif cmd == 'LSHIFT':
                ctx[out] = (ins[0] << ins[1]) & 0xffff
            elif cmd == 'RSHIFT':
                ctx[out] = ins[0] >> ins[1]
            elif cmd == 'NOT':
                ctx[out] = ~ins[0]
            else:
                assert 0, tup

        cmds = ncmds

    print(ctx['a'])
    return ctx['a']

def part(cmds):
    a = run(cmds)

    for i in range(len(cmds)):
        if cmds[i][0] == 'ASSIGN' and cmds[i][1][-1] == 'b':
            cmds[i] = ('ASSIGN', (a, 'b'))
            break

    run(cmds)

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
