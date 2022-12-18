#!/usr/bin/env python3

import sys

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

def main(argv):
    with open(argv[1]) as f:
        lines = f.readlines()

    grid = []
    for line in lines:
        line = line.strip('\r\n')
        grid.append(list(int(_) for _ in line))

    visible = set()
    for i, L in enumerate(grid):
        visible.update(find_visible(i, L))

    # top and bottom, reverse coords...
    for j in range(len(grid[0])):
        L = [_[j] for _ in grid]
        s = find_visible(j, L)
        visible.update((_[1], _[0]) for _ in s)

    print(len(visible))


if __name__ == '__main__':
    main(sys.argv)
