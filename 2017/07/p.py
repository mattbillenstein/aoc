#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    plates = {}
    weights = {}
    for line in lines:
        for c in '(),':
            line = line.replace(c, '')
        L = line.split()
        plates[L[0]] = x = []
        weights[L[0]] = int(L[1])
        if '->' in L:
            for item in L[3:]:
                x.append(item)

    return plates, weights

def part1(plates, weights):
    d = {}
    for t, L in plates.items():
        for item in L:
            d[item] = t

    for t, L in plates.items():
        if t not in d:
            print(t)
            break

def compute_weight(plate, plates, weights):
    weight = weights[plate]
    for p in plates[plate]:
        weight += compute_weight(p, plates, weights)
    return weight

def get_options(plates, weights):
    candidates = []
    for t, L in plates.items():
        ws = sorted([(compute_weight(_, plates, weights), _) for _ in L])
        if any(_[0] != ws[0][0] for _ in ws):
            delta = ws[-1][0] - ws[0][0]
            if ws[0][0] == ws[1][0]:
                new_weight = weights[ws[-1][1]] - delta
                candidates.append((ws[-1][1], new_weight))
            else:
                new_weight = weights[ws[0][1]] + delta
                candidates.append((ws[0][1], new_weight))
    return candidates

def part2(plates, weights):
    for n, w in get_options(plates, weights):
        tmp = weights[n]
        weights[n] = w
        if not get_options(plates, weights):
            print(w)
            break
        weights[n] = tmp

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
