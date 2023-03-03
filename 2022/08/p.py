#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]

    grid = []
    for line in lines:
        line = line.strip('\r\n')
        grid.append(list(int(_) for _ in line))

    return grid

def find_visible(i, L):
    visible = set()
    mx = max(L)

    # look from left and right and add to visible if the tree is taller
    # than an previous...
    for step in (1, -1):
        mn = -1
        j = 0 if step == 1 else len(L)-1
        while 1:
            if L[j] > mn:
                visible.add((i, j))
                mn = L[j]
            if L[j] == mx:
                break
            j += step

    return visible

def part1(grid):
    visible = set()
    for i, L in enumerate(grid):
        visible.update(find_visible(i, L))

    # top and bottom, reverse coords...
    for j in range(len(grid[0])):
        L = [_[j] for _ in grid]
        s = find_visible(j, L)
        visible.update((_[1], _[0]) for _ in s)

    print(len(visible))

def find_visible_product(i, L):
    result = {}

    # look from left and right compute the product of the number of trees
    # visible...
    for j, elem in enumerate(L):
        height = elem
        prod = 1
        for step in (1, -1):
            cnt = 0
            k = j
            k += step
            while k >= 0 and k < len(L):
                cnt += 1
                if L[k] >= height:
                    break
                k += step

            prod *= cnt

        result[(i, j)] = prod

    return result

def part2(grid):
    result = {}
    for i, L in enumerate(grid):
        result.update(find_visible_product(i, L))

    # top and bottom, reverse coords...
    for j in range(len(grid[0])):
        L = [_[j] for _ in grid]
        d = find_visible_product(j, L)
        for coord, prod in d.items():
            coord = (coord[1], coord[0])
            result[coord] *= prod

    print(max(result.values()))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
