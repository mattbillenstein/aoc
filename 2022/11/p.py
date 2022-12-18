#!/usr/bin/env python3

import functools
import math
import re
import sys

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


def main(argv):
    with open(argv[1]) as f:
        lines = [_.strip('\r\n') for _ in f]

    part = int(argv[2])

    monkies = {}
    divisors = []

    for line in lines:
        line = line.strip()
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

    if part == 1:
        rounds = 20
        handle_worry = lambda x: x // 3
    elif part == 2:
        rounds = 10000
        # you have to kinda guess at this part, or iterate through numbers
        # having guessed the correct function is modulus - rational for this is
        # the result grows super large super quick, but there's no real reason
        # simple mod is taken here vs any other function which cuts the growth
        # down fast...  Not a fan of this part of the problem.
        div = math.lcm(*divisors)
        handle_worry = lambda x: x % div
    else:
        assert 0

    for round in range(rounds):
        for id, m in monkies.items():
            for x, item in m.inspect(handle_worry):
                monkies[x].items.append(item)

    for id, m in monkies.items():
        print(m)

    business = sorted([_.inspected for _ in monkies.values()])[-2:]
    print(business[0] * business[1])

if __name__ == '__main__':
    main(sys.argv)
