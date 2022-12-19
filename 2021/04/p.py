#!/usr/bin/env pypy3

import sys
import time
from collections import defaultdict
from pprint import pprint

def parse_input():
    lines = [_.strip() for _ in sys.stdin]
    numbers = [int(_) for _ in lines[0].split(',')]
    games = []

    for line in lines[1:]:
        if not line:
            game = {'board': [], 'marked': []}
            games.append(game)
            continue

        game['board'].append([int(_) for _ in line.split()])
        game['marked'].append([0] * len(game['board'][-1]))

    return numbers, games

def mark(game, value):
    b = game['board']
    m = game['marked']
    for j in range(len(b)):
        for i in range(len(b[j])):
            if b[j][i] == value:
                m[j][i] = 1

def check(game):
    unmarked = 0
    won = False
    b = game['board']
    m = game['marked']
    for j in range(len(b)):
        if all(m[j]):
            won = True
        for i in range(len(b[j])):
            if not m[j][i]:
                unmarked += b[j][i]

    for i in range(len(m[0])):
        if all(m[j][i] for i in range(len(m))):
            won = True
            break

    return won, unmarked

def part1(data):
    # score of first winning game
    numbers, games = data

    for n in numbers:
        for g in games:
            mark(g, n)
            won, unmarked = check(g)
            if won:
                score = n * unmarked
                print(score)
                print()
                return

def part2(data):
    # score of last winning game
    numbers, games = data

    for g in games:
        g['won'] = False

    for n in numbers:
        if all(_['won'] for _ in games):
            print(score)
            break
        for g in games:
            if g['won']:
                continue
            mark(g, n)
            won, unmarked = check(g)
            if won:
                g['won'] = True
                score = n * unmarked

def main(argv):
    data = parse_input()

    part1(data)
    part2(data)

if __name__ == '__main__':
    main(sys.argv)
