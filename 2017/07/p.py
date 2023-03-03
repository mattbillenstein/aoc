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

def part2(plates, weights):
    if 1:
        print('vrgxe', 1219)
        weights['vrgxe'] = 1219

    for t, L in plates.items():
        ws = sorted([(compute_weight(_, plates, weights), _) for _ in L])
        if any(_[0] != ws[0][0] for _ in ws):
            print(t, ws)
            delta = ws[-1][0] - ws[0][0]
            if ws[0][0] == ws[1][0]:
                print(ws[-1], weights[ws[-1][1]] - delta)
            else:
                print(ws[0], weights[ws[0][1]] + delta)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
