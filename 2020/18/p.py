#!/usr/bin/env pypy3

import math
import sys
import time
from collections import defaultdict
from pprint import pprint

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    exprs = []
    for line in lines:
        expr = line.replace('(', ' ( ').replace(')', ' ) ').split()
        expr = [int(_) if _.isdigit() else _ for _ in expr]
        exprs.append(expr)
    return exprs

def solve(expr, add_first=False):
    # solve expr left to right, recurse on ()
    expr = list(expr)
    debug(expr)

    # scan for subexpressions first
    subexpr = []
    level = 0
    for i, tok in enumerate(expr):
        if tok == '(':
            if level == 0:
                subexpr.append([i])
            level += 1
        elif tok == ')':
            level -= 1
            if level == 0:
                subexpr[-1].append(i)

    # reverse so as we mutate, the indexes used to replace are still valid...
    for start, end in reversed(subexpr):
        x = solve(expr[start+1:end], add_first)
        expr[start:end+1] = [x]

    if add_first and '+' in expr:
        found = True
        while found:
            found = False
            for i, tok in enumerate(expr):
                if tok == '+':
                    expr[i-1:i+2] = [expr[i-1] + expr[i+1]]
                    found = True
                    break

    # evaluate left to right and return result
    while len(expr) > 1:
        x, op, y = expr.pop(0), expr.pop(0), expr.pop(0)
        if op == '+':
            v = x + y
        elif op == '*':
            v = x * y
        else:
            assert 0, op

        expr.insert(0, v)

    return expr[0]

def run(data, add_first=False):
    tot = 0
    for expr in data:
        v = solve(expr, add_first)
        tot += v
        debug(''.join(str(_) for _  in expr), '=', v)

    return tot

def part1(data):
    print(run(data))

def part2(data):
    print(run(data, add_first=True))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
