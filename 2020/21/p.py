#!/usr/bin/env pypy3

import itertools
import math
import random
import sys
import time
from collections import defaultdict
from pprint import pprint

DEBUG = '--debug' in sys.argv

class Conflict(Exception):
    pass

class Food:
    def __init__(self, ingredients, allergens):
        self.allergens = set(allergens)
        self.ingredients = {}
        for i in ingredients:
            self.ingredients[i] = set(self.allergens | set([None]))

    def __repr__(self):
        return f'Food({self.ingredients}, {self.allergens})'

    def set_allergen(self, ingredient, allergen):
        L = []

        for i, s in self.ingredients.items():
            # if allergen set on another ingredient, conflict
            if i != ingredient and allergen in s and len(s) == 1:
                raise Conflict()

        # if we don't have the ingredient, nothing else to do...
        allergens = self.ingredients.get(ingredient)
        if not allergens:
            return L

        if allergen not in allergens:
            # if ingredient isn't marked none or allergen isn't marked in any
            # other ingredient...
            if None not in allergens:
                raise Conflict()

            # we can set to None if allergen isn't marked...
            allergens.intersection_update([None])
        else:
            # set the allergen here
            allergen = set([allergen])
            allergens.intersection_update(allergen)

            # we can remove the allergen from other ingredients, it's present
            # in exactly on ingredient globally...
            for i, s in self.ingredients.items():
                if i != ingredient:
                    s.difference_update(allergen)
                    assert len(s), s

            # check if we implictely set any other allergens and back-propagate
            # this set to the other fooods through the return value
            d = defaultdict(int)
            for i, s in self.ingredients.items():
                if None in s and len(s) == 2:
                    a = [_ for _ in s if _][0]
                    d[a] += 1

            for a, cnt in d.items():
                if cnt == 1:
                    for i, s in self.ingredients.items():
                        if a in s:
                            s.difference_update(set([None]))
                            L.append((i, a))
                            break

        # check all allergens are still covered...
        existing = set()
        for s in self.ingredients.values():
            existing.update(s)

        existing.discard(None)
        if existing != self.allergens:
            raise Conflict()

        return L

    def copy(self):
        return Food({k: set(v) for k, v in self.ingredients.items()}, list(self.allergens))

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]

    foods = []
    for line in lines:
        line = line.replace('(', '').replace(')', '').replace(',', '')
        ingredients, allergens = line.split(' contains ')
        ingredients = ingredients.split()
        allergens = allergens.split()
        foods.append(Food(ingredients, allergens))

    return foods

def part1(foods):
    # guess and check
    done = False
    while not done:
        L = [_.copy() for _ in foods]

        while 1:
            done = True
            for f in L:
                debug(f)
                if not all(len(_) == 1 for _ in f.ingredients.values()):
                    done = False

            if done:
                break

            q = []
            while 1:
                f = random.choice(L)
                i = random.choice(list(f.ingredients))
                s = f.ingredients[i]
                if len(s) > 1:
                    a = [_ for _ in s if _][0]
                    q.append((i, a))
                    debug(f'Select {i} {a} {f}')
                    break

            try:
                while q:
                    i, a = q.pop()
                    for f in L:
                        q.extend(f.set_allergen(i, a))
                        debug(f'Set {i} {a} {f}')
            except Conflict:
                debug(f'Conflict {i} {a}')
                break

    ingredients = defaultdict(set)
    for f in L:
        for i, s in f.ingredients.items():
            ingredients[i].update(s)

    pprint(ingredients)

    non_allergens = set()
    for i, s in ingredients.items():
        if s == {None}:
            non_allergens.add(i)

    cnt = 0
    for f in foods:
        for i in f.ingredients:
            if i in non_allergens:
                cnt += 1
    print(cnt)

def part2(data):
    pass

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
