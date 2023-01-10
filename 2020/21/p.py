#!/usr/bin/env pypy3

import itertools
import math
import random
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

    foods = []
    for line in lines:
        line = line.replace('(', '').replace(')', '').replace(',', '')
        ingredients, allergens = line.split(' contains ')
        ingredients = ingredients.split()
        allergens = allergens.split()
        foods.append((ingredients, allergens))

    return foods

class Ingredient:
    def __init__(self, name):
        self.name = name
        self.allergen = None

    def __repr__(self):
        return f'I({self.name}, {self.allergen})'

class Food:
    def __init__(self, ingredients, allergens):
        self.ingredients = ingredients
        self.allergens = set(allergens)

    def check(self):
        # return missing allergens to guide the guess-and-check
        u = set()
        for i in self.ingredients:
            if i.allergen:
                u.add(i.allergen)
        return self.allergens.difference(u)

    def __repr__(self):
        return f'Food({self.ingredients}, {self.allergens})'

def run(foods):
    ingredients = dict()
    allergens = set()
    for f in foods:
        for i in f[0]:
            ingredients[i] = Ingredient(i)
        for a in f[1]:
            allergens.add(a)

    Foods = []
    for f in foods:
        Foods.append(Food([ingredients[_] for _ in f[0]], f[1]))

    ingredients = list(ingredients.values())

    # assign initial allergens
    allergens = sorted(allergens)
    for i, a in zip(ingredients, allergens):
        i.allergen = a

    # until each food has ingredients with a valid set of allergens, swap a
    # missing allergen to any of the other ingredients of that food
    while any(_.check() for _ in Foods):
        f = random.choice(Foods)
        missing = f.check()
        if missing:
            for m in missing:
                other = random.choice(f.ingredients)
                while other.allergen == m:
                    other = random.choice(f.ingredients)

                for old in ingredients:
                    if old.allergen == m:
                        old.allergen = None
                        break

                other.allergen = m

    non_allergens = set()
    for i in ingredients:
        debug(i.name, i.allergen)
        if i.allergen is None:
            non_allergens.add(i.name)

    cnt = 0
    for f in Foods:
        debug(f)
        for i in f.ingredients:
            if i.name in non_allergens:
                cnt += 1

    print(cnt)

    print(','.join(_.name for _ in sorted([_ for _ in ingredients if _.allergen], key=lambda x: x.allergen)))

def main():
    data = parse_input()
    run(data)

if __name__ == '__main__':
    main()
