#!/usr/bin/env pypy3

import re
import sys
from collections import defaultdict
from pprint import pprint

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]

    bags = defaultdict(dict)
    for line in lines:
        mobj = re.match('^(.*) bags contain (.*)$', line)
        bag, other = mobj.groups()
        for cnt, color in re.findall('([0-9]+) ([a-z ]+) bag', other):
            cnt = int(cnt)
            bags[bag][color] = cnt

    return bags

def part1(bags):
    if DEBUG:
        pprint(bags)

    find = 'shiny gold'
    contains = set()
    for k, d in bags.items():
        if find in d:
            contains.add(k)

    found = True
    while found:
        found = False
        for k, d in bags.items():
            for k2 in d:
                if k2 in contains and not k in contains:
                    contains.add(k)
                    found = True

    debug(contains)
    print(len(contains))

def part2(bags):
    d = bags['shiny gold']
    cnts = defaultdict(int)
    while d:
        for k, v in d.items():
            cnts[k] += v

        d2 = defaultdict(int)
        for k, v in d.items():
            for k2, v2 in bags[k].items():
                d2[k2] += v * v2
        d = d2

    debug(cnts)
    print(sum(cnts.values()))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
