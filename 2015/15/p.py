#!/usr/bin/env pypy3

import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    ingredients = []
    for line in lines:
        for c in ':,':
            line = line.replace(c, '')
        L = line.split()
        ingredient = {
            'name': L[0],
        }
        for i in range(1, len(L), 2):
            ingredient[L[i]] = int(L[i+1])
        ingredients.append(ingredient)
    
    return ingredients

def part(ingredients):
    best = 0
    best_cals = 0
    for a in range(1, 101, 1):
        for b in range(1, 101, 1):
            if a + b > 100:
                continue
            for c in range(1, 101, 1):
                if a + b + c > 100:
                    continue
                for d in range(1, 101, 1):
                    if a + b + c + d != 100:
                        continue

                    tot = 1
                    for k in ingredients[0]:
                        if k in ('name', 'calories'):
                            continue
                        x = 0
                        for amt, i in zip([a, b, c, d], ingredients):
                            x += i[k] * amt
                        x = max(0, x)
                        tot *= x

                        if tot > best:
                            best = tot

                        cals = 0
                        for amt, i in zip([a, b, c, d], ingredients):
                            cals += i['calories'] * amt

                        if cals == 500 and tot > best_cals:
                            best_cals = tot

    print(best)
    print(best_cals)

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
