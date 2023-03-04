#!/usr/bin/env pypy3

import sys

from grid import SparseGrid
from intcode import intcode

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    mem = [int(_) for _ in lines[0].split(',')]
    return mem

def part(mem):
    # program outputs chr(c) values, but only store non-empty
    chars = {_: ord(_) for _ in '#<>v^'}
    chars['.'] = 0
    g = SparseGrid([], chars)

    # run program and pull out the grid
    prog = intcode(mem)
    x, y = 0, 0
    for v in prog:
        c = chr(v)
        if c == '\n':
            x = 0
            y += 1
            continue
            
        if c != '.':
            g.set((x, y), v)
        x += 1

    if DEBUG:
        print()
        g.print()

    intersections = []
    for pt in g:
        if g.get(pt) == chars['#'] and all(g.get(g.step(pt, _)) == chars['#'] for _ in '<>v^'):
            intersections.append(pt)

    debug(intersections)
    # part 1, sum of all x*y intersections
    print(sum(x*y for x, y in intersections))

    # part 2
    #
    # trace backwards from the bot location until we visit the entire path,
    # first compute a turn, then step until we hit another corner - it works
    # out we never have to consider turning at an intersection, we can always
    # go straight...

    # initial conditions
    cnt = 0
    for pt in g:
        v = g.get(pt, 0)
        c = chr(v)
        if c in '<>^v':
            pos = pt
        if c == '#':
            cnt += 1

    dir = chr(g.get(pos))

    debug(pos, cnt, dir)

    turns = {
        '^': {'<': 'L', '>': 'R'},
        '<': {'v': 'L', '^': 'R'},
        'v': {'>': 'L', '<': 'R'},
        '>': {'^': 'L', 'v': 'R'},
    }

    directions = []
    visited = set()
    while len(visited) < cnt:
        # compute turn
        for ndir in '<>^v':
            pt = g.step(pos, ndir)
            if not pt in visited and g.get(pt):
                turn = turns[dir][ndir]
                directions.append(turn)
                dir = ndir
                break

        steps = 0
        while 1:
            npos = g.step(pos, dir)
            if not g.get(npos):
                break
            pos = npos
            visited.add(pos)
            steps += 1

        directions.append(steps)

    debug(directions, len(directions))

    # Try range of lengths for A, B, C consuming the directions...

    def consume(directions, seqs):
        L = []
        found = True
        while directions and found:
            found = False
            for name, tup in seqs.items():
                if directions[:len(tup)] == tup:
                    found = True
                    directions = directions[len(tup):]
                    L.append(name)
                    break
        return L, directions

    lengths = range(4, 14, 2)
    matched = None
    for alen in lengths:
        for blen in lengths:
            for clen in lengths:
                MAIN = []
                d = tuple(directions)
                seqs = {}

                assert len(d) >= alen
                seqs['A'] = d[:alen]
                L, d = consume(d, seqs)
                MAIN.extend(L)

                assert len(d) >= blen
                seqs['B'] = d[:blen]
                L, d = consume(d, seqs)
                MAIN.extend(L)

                assert len(d) >= clen
                C = d[:clen]
                seqs['C'] = d[:clen]
                L, d = consume(d, seqs)
                MAIN.extend(L)

                if not d:
                    matched = (MAIN, dict(seqs))

    assert matched

    MAIN, seqs = matched

    debug(MAIN)
    debug(seqs)

    # wake up bot and feed directions
    mem[0] = 2

    prog = intcode(mem)
    for L in (MAIN, seqs['A'], seqs['B'], seqs['C'], 'n'):
        s = ','.join(str(_) for _ in L) + '\n'
        if DEBUG:
            print(repr(s), [ord(_) for _ in s], len(s))

        x = next(prog)
        while x != 'INPUT':
            x = next(prog)

        for c in s:
            prog.send(ord(c))

    # read dust collected...
    for v in prog:
        if v > 128:
            print(v)

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
