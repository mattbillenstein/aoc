#!/usr/bin/env pypy3

import re
import sys
from pprint import pprint

from graph import bfs, dfs

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]

    valves = {}
    edges = {}
    for line in lines:
        mobj = re.match('^Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ([ ,A-Z]+)$'
, line)
        assert mobj, line
        name, rate, others = mobj.groups()
        others = others.split(', ')

        valves[name] = int(rate)
        edges[name] = others

    return valves, edges

def simplify(valves, edges):
    keep = set([k for k, v in valves.items() if v > 0])
    if 'AA' not in keep:
        keep.add('AA')

    def neighbors(valve):
        return edges[valve]

    newedges = {}
    for valve in keep:
        newedges[valve] = L = bfs(valve, neighbors, keep)
        remove = []
        for tup in L:
            if tup[0] in ('AA', valve):
                remove.append(tup)
        for tup in remove:
            L.remove(tup)

    return newedges

class State:
    max_minutes = 30
    enable_elephant = False

    def __init__(self, pos, t, opened, valves, edges, is_elephant=False):
        self.pos = pos
        self.t = t
        self.opened = opened
        self.valves = valves
        self.edges = edges
        self.is_elephant = is_elephant

        self.score = 0
        for n, m in sorted(self.opened.items(), key=lambda x: x[1]):
            mins = max(self.max_minutes - m - 1, 0)
            x = mins * self.valves[n]
            self.score += x

    @property
    def done(self):
        # if we're done
        return self.t >= self.max_minutes or len(self.opened) == len(self.edges) or not any(_ for _ in self.next())

    @property
    def key(self):
        # the key into the visited dict
        return (self.t, ' '.join(sorted(self.opened)), self.is_elephant)

    @property
    def cost(self):
        # cost, lower is better
        return -self.score

    def next(self):
        # next states
        for k, v in self.edges[self.pos]:
            if k not in self.opened and self.t + v <= self.max_minutes:
                # check opening and not opening this valve in this step
                yield State(k, self.t + v, dict(self.opened), self.valves, self.edges, self.is_elephant)

                o = dict(self.opened)
                o[k] = self.t + v
                yield State(k, self.t + v + 1, o, self.valves, self.edges, self.is_elephant)

                if self.enable_elephant and not self.is_elephant:
                    # start the elephant with our opened valves
                    yield State('AA', 4, dict(o), self.valves, self.edges, True)

    def __repr__(self):
        return f'State({self.opened}, {self.cost})'

def part1(valves, edges):
    edges = simplify(valves, edges)
    if DEBUG:
        pprint(edges)

    state = State('AA', 0, {}, valves, edges)
    best = dfs(state)

    print(-best.cost)

def part2(valves, edges):
    edges = simplify(valves, edges)

    State.enable_elephant = True

    # start at t=4, had to teach the elephant
    state = State('AA', 4, {}, valves, edges)
    best = dfs(state)

    print(-best.cost)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()