#!/usr/bin/env pypy3

import sys

from grid import Grid

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    cmds = []
    for line in lines:
        if line.startswith('rect'):
            x, y = line.split()[1].split('x')
            x = int(x)
            y = int(y)
            cmds.append(('rect', (x, y)))
        elif line.startswith('rotate'):
            line = line.replace('=', ' ')
            L = line.split()
            axis = L[2]
            offset = int(L[3])
            amt = int(L[5])
            cmds.append(('rotate', (axis, offset, amt)))
    return cmds

def part(cmds):
    sizex, sizey = 50, 6
    g = Grid(['.' * sizex] * sizey)

    for cmd, opts in cmds:
        if cmd == 'rect':
            for x in range(opts[0]):
                for y in range(opts[1]):
                    g.set((x, y), 1)

        elif cmd == 'rotate':
            axis, offset, amt = opts
            if axis == 'y':
                y = offset
                xs = [g.get((_, y)) for _ in range(sizex)]
                xs = xs[-amt:] + xs[:-amt]
                for x, v in enumerate(xs):
                    g.set((x, y), v)
            else:
                x = offset
                ys = [g.get((x, _)) for _ in range(sizey)]
                ys = ys[-amt:] + ys[:-amt]
                for y, v in enumerate(ys):
                    g.set((x, y), v)

    print(sum(g.get(pt) for pt in g))
    g.print()

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
