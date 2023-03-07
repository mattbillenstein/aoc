#!/usr/bin/env pypy3

import sys

from graph import dfs

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    repls = []
    for line in lines:
        if '=>' in line:
            L = line.split()
            repls.append((L[0], L[2]))
        elif line:
            molecule = line
    return repls, molecule

def replacements(repls, molecule):
    s = set()
    for k, v in repls:
        idx = 0
        while 1:
            idx = molecule.find(k, idx)
            if idx == -1:
                break

            m = molecule[:idx] + v + molecule[idx+len(k):]
            s.add(m)

            idx += 1

    return s

def part1(repls, molecule):
    s = replacements(repls, molecule)
    print(len(s))

class State:
    def __init__(self, molecule, steps, repls):
        self.molecule = molecule
        self.steps = steps
        self.repls = repls

    @property
    def done(self):
        # if we're done
        return self.molecule == 'e'

    @property
    def key(self):
        # the key into the visited dict
        return hash(self.molecule)

    @property
    def cost(self):
        # cost, lower is better
        return (len(self.molecule), self.steps)

    def next(self):
        # next states
        # greedy, take just a couple of the shortest substitutions...
        ms = list(replacements(self.repls, self.molecule))
        ms.sort(key=lambda x: (len(x), x))
        for m in ms[:2]:
            yield self.__class__(m, self.steps + 1, self.repls)

    def __repr__(self):
        return f'State({self.molecule}, {self.cost})'

def part2(repls, molecule):
    # ok, how about dfs backwards to lowest length and fewest number of steps?
    #
    # there are a huge number of intermediate states - this is a grammar that
    # can just be computed as a reduction, but a greedy dfs works as well...

    rrepls = [(b, a) for a, b in repls]

    # greedy, take longest substitutions first
    rrepls.sort(key=lambda x: (len(x[0]), x[0]), reverse=True)

    state = State(molecule, 0, rrepls)
    best = dfs(state)
    print(best.steps)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
