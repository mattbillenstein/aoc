#!/usr/bin/env pypy3

import itertools
import math
import sys
from collections import defaultdict

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    boxes = [tuple([int(_) for _ in line.split(',')]) for line in lines]
    return (boxes,)

def ldist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)

def part(boxes):
    # compute euclidian distance between each pair of points
    pairs = []
    for b1, b2 in itertools.combinations(boxes, 2):
        pairs.append((ldist(b1, b2), b1, b2))
    pairs.sort()

    # test input, just consider 10 pairs in part 1, 1000 part 2
    N = 10 if len(boxes) < 100 else 1000

    # box -> circuit # it's in
    circuits = {}
    n = 0
    for _, b1, b2 in pairs:
        if b1 not in circuits and b2 not in circuits:
            # new circuit
            circuits[b1] = circuits[b2] = len(circuits)
        elif b1 in circuits and b2 not in circuits:
            # b2 joins circuit on b1
            circuits[b2] = circuits[b1]
        elif b2 in circuits and b1 not in circuits:
            # b1 joins circuit on b2
            circuits[b1] = circuits[b2]
        else:
            # join two different circuits using circuit of b1
            c1 = circuits[b1]
            c2 = circuits[b2]
            for k in list(circuits):
                if circuits[k] == c2:
                    circuits[k] = c1

        n += 1
        if n == N and '1' in sys.argv:
            # part 1, product of number of boxes in 3 largest circuits
            counts = defaultdict(int)
            for k, v in circuits.items():
                counts[v] += 1

            L = list(counts.values())
            L.sort(reverse=True)

            tot = 1
            for x in L[:3]:
                tot *= x
            print(tot)

            if '2' not in sys.argv:
                return

        # part 2, every box in a single circuit, take product of X of b1, b2
        if len(circuits) == len(boxes) and len(set(circuits.values())) == 1:
            print(b1[0] * b2[0])
            return

def main():
    data = parse_input()
    part(*data)

if __name__ == '__main__':
    main()
