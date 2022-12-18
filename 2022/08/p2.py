#!/usr/bin/env python3

import sys

def find_visible(i, L):
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

def main(argv):
    with open(argv[1]) as f:
        lines = f.readlines()

    grid = []
    for line in lines:
        line = line.strip('\r\n')
        grid.append(list(int(_) for _ in line))

    result = {}
    for i, L in enumerate(grid):
        result.update(find_visible(i, L))

    # top and bottom, reverse coords...
    for j in range(len(grid[0])):
        L = [_[j] for _ in grid]
        d = find_visible(j, L)
        for coord, prod in d.items():
            coord = (coord[1], coord[0])
            result[coord] *= prod

    print(max(result.values()))


if __name__ == '__main__':
    main(sys.argv)
