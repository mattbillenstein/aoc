#!/usr/bin/env pypy3

import sys
from collections import defaultdict

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]

    template = lines[0]
    rules = dict(_.split(' -> ') for _ in lines[2:])

    return template, rules

def parts_from_template(s):
    L = []
    for j in range(1, len(s)):
        L.append(s[j-1] + s[j])
    return L

def polymerize(template, rules, times):
    t = template
    for i in range(times):
        t2 = ''
        for s in parts_from_template(t):
            t2 += s[0] + rules[s]
        t2 += t[-1]
        t = t2
    return t

def part1(template, rules):
    s = polymerize(template, rules, 10)

    d = defaultdict(int)
    for c in s:
        d[c] += 1

#    print(d)
    print(max(d.values()) - min(d.values()))

def part2(template, rules):
    # at each step, each part present creates two more, just keep a total of
    # all the productions between steps and multiple by the number of
    # occurrences at the start of the step...

    parts = defaultdict(int)
    for p in parts_from_template(template):
        parts[p] += 1

    for i in range(40):
        next_parts = defaultdict(int)
        for k, v in parts.items():
            # at each step, each part creates 2 more
            c = rules[k]
            next_parts[k[0] + c] += v
            next_parts[c + k[1]] += v
        parts = next_parts

    totals = defaultdict(int)
    # the last char is undercounted by one since it's not included in the count
    # below...
    totals[template[-1]] += 1

    # count only first char of parts, the second char is the first char of
    # another part
    for k, v in parts.items():
        totals[k[0]] += v

#    print(totals)
    print(max(totals.values()) - min(totals.values()))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
