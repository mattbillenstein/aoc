#!/usr/bin/env python3

import copy
import functools
import math
import re
import sys

DEBUG = sys.argv.count('-v')

def parse_input():
    lines = [_.strip() for _ in sys.stdin]

    monkies = {}
    divisors = []

    for line in lines:
        if line.startswith('Monkey '):
            id = int(line.replace(':', '').split()[1])
            m = Monkey(id)
            monkies[id] = m
        elif line.startswith('Starting items:'):
            m.items = [Item(int(_)) for _ in line.split(':')[1].replace(' ', '').split(',')]
        elif line.startswith('Operation:'):
            s = line.split(':')[1].strip()
            mobj = re.match('new = old ([+*]) ([0-9]+|old)', s)
            oper, val = mobj.groups()
            m.operation = functools.partial(op, oper, val)
        elif line.startswith('Test:'):
            s = line.split(':')[-1].strip()
            assert s.startswith('divisible by ')
            div = int(s.split()[-1])
            divisors.append(div)
            m.test = functools.partial(test, div)
        elif line.startswith('If true:'):
            m.t = int(line.split()[-1])
        elif line.startswith('If false:'):
            m.f = int(line.split()[-1])

    return monkies, divisors

class Item:
    def __init__(self, worry):
        self.initial_worry = worry
        self.worry = worry

    def __str__(self):
        return f'Item({self.initial_worry}, {self.worry})'

    def __repr__(self):
        return self.__str__()


class Monkey:
    def __init__(self, id):
        self.id = id
        self.inspected = 0

    def __str__(self):
        return f'Monkey({self.id} {self.items} {self.inspected})'

    def __repr__(self):
        return self.__str__()

    def inspect(self, handle_worry):
        for item in self.items:
            self.inspected += 1

            item.worry = self.operation(item.worry)

            item.worry = handle_worry(item.worry)

            id = self.f
            if self.test(item.worry):
                id = self.t

            yield id, item

        self.items.clear()

def op(op, val, other):
    if op == '*':
        if val == 'old':
            x = other * other
        else:
            x = int(val) * other
    elif op == '+':
        x = int(val) + other
    return x

def test(div, other):
    return other % div == 0

def part(data, part):
    monkies, divisors = data

    rounds = 20
    handle_worry = lambda x: x // 3

    if part == 2:
        rounds = 10000
        # you have to kinda guess at this part, or iterate through numbers
        # having guessed the correct function is modulus - rational for this is
        # the result grows super large super quick, but there's no real reason
        # simple mod is taken here vs any other function which cuts the growth
        # down fast...  Not a fan of this part of the problem.

        # This part is the NOT the chinese remainder theorem... Just a property
        # of mod
        #
        # From https://instantiator.dev/post/8-bit-supercomputer/
        #
        # 1. The remainder theorem thing
        #
        # Aspect 1 caught me out at first, but once I’d grasped it, I was able to make progress:
        #
        #   if you have a very large number and you want to reduce it, but also
        #   need to preserve the remainder properties when divided by a
        #   collection of other numbers, get the product of those other
        #   numbers, divide the original by that, and take the remainder.
        #
        # For example:
        #
        # You have a large number: 5000
        # 5000 / 3 = 1666 r 2
        # 5000 / 5 = 1000 r 0
        # 5000 / 11 = 454 r 6
        # You can divide 5000 by (3 x 5 x 11 = 165) to preserve the remainders, ie.
        # 5000 / 165 = 30 r 50 (take the remainder)
        # 50 / 3 = 16 r 2 (the remainder is preserved)
        # 50 / 5 = 10 r 0 (the remainder is preserved)
        # 50 / 11 = 4 r 6 (the remainder is preserved)

        div = math.lcm(*divisors)
        handle_worry = lambda x: x % div

    for round in range(rounds):
        for id, m in monkies.items():
            for x, item in m.inspect(handle_worry):
                monkies[x].items.append(item)

    if DEBUG:
        for id, m in monkies.items():
            print(m)

    business = sorted([_.inspected for _ in monkies.values()])[-2:]
    print(business[0] * business[1])

def main():
    data = parse_input()
    if '1' in sys.argv:
        part(copy.deepcopy(data), 1)
    if '2' in sys.argv:
        part(copy.deepcopy(data), 2)

if __name__ == '__main__':
    main()
