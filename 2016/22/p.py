#!/usr/bin/env pypy3

import sys

from graph import bfs
from grid import Grid

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    nodes = []
    for line in lines[2:]:
        name, size, used, avail, _ = line.split()
        _, x, y = name.split('-')
        x = int(x[1:])
        y = int(y[1:])
        size = int(size[:-1])
        used = int(used[:-1])
        avail = int(avail[:-1])

        nodes.append({
            'pt': (x, y),
            'size': size,
            'used': used,
            'avail': avail,
        })
        
    return nodes

def part1(nodes):
    cnt = 0
    for n1 in nodes:
        for n2 in nodes:
            if n1 is n2:
                continue
            if n1['used'] and n1['used'] <= n2['avail']:
                cnt += 1
    print(cnt)

def print_nodes(nodes):
    rx = max([_['pt'][0] for _ in nodes.values()]) + 1
    ry = max([_['pt'][1] for _ in nodes.values()]) + 1

    for y in range(ry):
        s = ''
        for x in range(rx):
            n = nodes[(x, y)]
            s += f'{n["used"]}/{n["size"]} '
        print(s)
            
def part2(nodes):
    d = {}
    for n in nodes:
        d[n['pt']] = n
    nodes = d

    sx = max([_['pt'][0] for _ in nodes.values()]) + 1
    sy = max([_['pt'][1] for _ in nodes.values()]) + 1

    g = Grid(['.' * sx] * sy, {'.': 0, '#': 1, '0': 2, 'G': 3, 'E': 4})

    end = (0, 0)
    goal = (sx-1, 0)

#    print_nodes(nodes)

    debug(d[end])
    debug(d[goal])

    for pt in g:
        n = nodes[pt]
        if n['used'] > 100:
            g.setc(pt, '#')
        elif n['used'] == 0:
            g.setc(pt, '0')
            zero = pt

    g.setc(goal, 'G')
    g.setc(end, 'E')

    if DEBUG:
        g.print()

    def neighbors(pt):
        for npt in g.neighbors4(pt):
            if g.getc(npt) in ('.', 'G'):
                yield npt

    # move hole into G - 72 steps
    dist = bfs(zero, neighbors, goal)
    debug('bfs', dist)

    # takes 5 steps to move G one - shuffle the hole around, G has moved 1
    # after the hole takes its place, and we can just walk it over to y=0
    tot = dist + 5 * (goal[0] - 1 - end[0])

    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
