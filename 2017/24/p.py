#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return sorted([tuple(sorted([int(_) for _ in line.split('/')])) for line in lines])

def search(bridge, connect, links, best):
    # add another matching component to the bridge and recurse - if we can't,
    # compute score and store...
    found = False
    for link in list(links):
        if connect in link:
            found = True
            links.remove(link)
            bridge.add(link)
            c = link[0]
            if link[0] == connect:
                c = link[1]
            search(bridge, c, links, best)
            bridge.remove(link)
            links.add(link)

    if not found:
        strength = sum(a+b for a, b in bridge)
        if strength > best[0][0]:
            best[0][0] = strength
            best[0][1] = tuple(bridge)

        if (len(bridge), strength) > best[1][0]:
            best[1][0] = (len(bridge), strength)
            best[1][1] = tuple(bridge)

def part(links):
    links = set(links)
    best = [
        [0, None],          # best by strength
        [(0, 0), None],     # best by (length, strength)
    ]

    search(set(), 0, links, best)

    print(best[0][0])
    print(best[1][0][1])

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
