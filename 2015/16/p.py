#!/usr/bin/env pypy3

import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    sues = []
    for line in lines:
        for c in ':,':
            line = line.replace(c, '')
        L = line.split()
        sue = {'id': L[1]}
        sues.append(sue)
        for i in range(2, len(L), 2):
            sue[L[i]] = int(L[i+1])
    return sues

def part(sues):
    params = {
        'children': 3,
        'cats': 7,
        'samoyeds': 2,
        'pomeranians': 3,
        'akitas': 0,
        'vizslas': 0,
        'goldfish': 5,
        'trees': 3,
        'cars': 2,
        'perfumes': 1,
    }
    for sue in sues:
        if all(sue.get(k, v) == v for k, v in params.items()):
            print(sue['id'])
            break

    others = [_ for _ in params if _ not in ('cats', 'trees', 'pomeranians', 'goldfish')]
    for sue in sues:
        if all(sue.get(k, params[k]+1) > params[k] for k in ('cats', 'trees')) and \
            all(sue.get(k, params[k]-1) < params[k] for k in ('pomeranians', 'goldfish')) and \
            all(sue.get(k, params[k]) == params[k] for k in others):
            print(sue['id'])
            break

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
