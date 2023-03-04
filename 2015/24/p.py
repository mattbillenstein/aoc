#!/usr/bin/env pypy3

import random
import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    lines = [int(_) for _ in lines]
    return lines

def qe(L):
    x = 1
    for item in L:
        x *= item
    return x

def balance(pkgs, N):
    # just random search - optimisitcally moving pkgs from heaviest group to
    # lightest one or randomnly if all the same...

    best = (len(pkgs), sys.maxsize)

    groups = [[] for _ in range(N)]
    for i, p in enumerate(pkgs):
        groups[i % len(groups)].append(p)

    for i in range(4_000_000):
        weights = [sum(_) for _ in groups]
        if all(_ == weights[0] for _ in weights[1:]):
            score = min((len(_), qe(_)) for _ in groups)
            if score < best:
                best = score
                debug([(len(_), sum(_), qe(_)) for _ in groups])
                debug(best)

            # randomly swap
            g1 = random.choice(groups)
            g2 = random.choice(groups)
            while g2 is g1:
                g2 = random.choice(groups)

            x = random.choice(g1)
            g1.remove(x)
            g2.append(x)

        else:
            # take random item from heaviest and put it in one of the other
            # groups
            i = weights.index(max(weights))
            j = weights.index(min(weights))

            x = random.choice(groups[i])
            groups[i].remove(x)
            groups[j].append(x)

    debug(best)
    print(best[-1])

def part1(pkgs):
    balance(pkgs, 3)

def part2(pkgs):
    balance(pkgs, 4)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
