#!/usr/bin/env pypy3

import sys

try:
    # the hotness...
    from z3 import *
except ImportError:
    pass

from algo import cramers_rule

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

COST_A = 3
COST_B = 1

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    games = []
    for line in lines:
        if not line:
            continue

        line = line.replace(':', '').replace(',', '').replace('+', ' ').replace('=', ' ')
        tup = line.split()
        if tup[0] == 'Button':
            if tup[1] == 'A':
                game = {}
                games.append(game)
            game[tup[1].lower()] = (int(tup[3]), int(tup[5]))
        if tup[0] == 'Prize':
            game['prize'] = (int(tup[2]), int(tup[4]))

    return games

def part1(games):
    tot = 0
    for game in games:
        a = game['a']
        b = game['b']
        prize = game['prize']
        best = (1e9, None)

        for pressed_a in range(100):
            for pressed_b in range(100):
                pt = (a[0] * pressed_a + b[0] * pressed_b, a[1] * pressed_a + b[1] * pressed_b)
                if pt == prize:
                    cost = COST_A * pressed_a + COST_B * pressed_b
                    if cost < best[0]:
                        best = (cost, pt)
    
        if best[1]:
            tot += best[0]

    print(tot)

def z3_optimize_cost(game):
    # uze z3 optimizer to optimize cost of pressed-a "pa" and pressed-b "pb" -
    # return cost of best solution...
    a = game['a']
    b = game['b']
    prize = game['prize']

    opt = Optimize()

    pa = Int('pa')
    pb = Int('pb')

    opt.add(pa >= 0)
    opt.add(pb >= 0)
    opt.add(a[0] * pa + b[0] * pb == prize[0])
    opt.add(a[1] * pa + b[1] * pb == prize[1])

    opt.minimize(pa * COST_A + pb * COST_B)

    cost = 0
    if opt.check() == sat:
        model = opt.model()
        pa = model[pa].as_long()
        pb = model[pb].as_long()
        cost = pa * COST_A + pb * COST_B
        debug(game, pa, pb, cost)
    else:
        debug(game, 'no solution')

    return cost

def cramers_rule_cost(game):
    a = game['a']
    b = game['b']
    prize = game['prize']

    # AX = B
    A = [[a[0], b[0]], [a[1], b[1]]]
    B = [prize[0], prize[1]]
    X = cramers_rule(A, B)

    # to int
    X = [int(round(_)) for _ in X]

    pa, pb = X

    cost = 0
    if pa * a[0] + pb * b[0] == prize[0] and pa * a[1] + pb * b[1] == prize[1]:
        cost = pa * COST_A + pb * COST_B
        debug(game, pa, pb, cost)
    else:
        debug(game, 'no solution')

    return cost

def part2(games):
    # Add 10000000000000 to x, y of each prize
    delta = 10000000000000
    for game in games:
        prize = game['prize']
        game['prize'] = (prize[0] + delta, prize[1] + delta)

    tot = 0
    for game in games:
        #tot += z3_optimize_cost(game)
        tot += cramers_rule_cost(game)
    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2([dict(_) for _ in data])

if __name__ == '__main__':
    main()
