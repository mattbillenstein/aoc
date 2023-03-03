#!/usr/bin/env pypy3

import sys
from collections import defaultdict
from pprint import pprint

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    steps = []
    for line in lines:
        tup = line.split()
        steps.append((tup[1], tup[7]))
    return steps

def part1(steps):
    all_steps = set()

    d = defaultdict(list)
    for tup in steps:
        x, y = tup
        d[y].append(x)
        all_steps.add(x)
        all_steps.add(y)

    if DEBUG:
        pprint(d)

    all_steps = sorted(all_steps)
    start = [_ for _ in all_steps if _ not in d]
    completed = []

    while d:
        found = start[0] if start else None

        for step in sorted(d):
            deps = d[step]
            if all(_ in completed for _ in deps):
                if not found or step < found:
                    found = step
                break

        completed.append(found)
        if found in start:
            start.remove(found)
        if found in d:
            d.pop(found)

    print(''.join(completed))

def duration(step):
    return ord(step) - ord('A') + 1

def part2(steps):
    all_steps = set()

    d = defaultdict(list)
    for tup in steps:
        x, y = tup
        d[y].append(x)
        all_steps.add(x)
        all_steps.add(y)

    if DEBUG:
        pprint(d)

    all_steps = sorted(all_steps)
    start = [_ for _ in all_steps if _ not in d]
    completed = []

    def next_step():
        found = start[0] if start else None

        for step in sorted(d):
            deps = d[step]
            if all(_ in completed for _ in deps):
                if not found or step < found:
                    found = step
                break

        if found in start:
            start.remove(found)
        if found in d:
            d.pop(found)

        return found

    slots = [None] * 5
    base_duration = 60
    if len(steps) < 20:
        slots = [None] * 2
        base_duration = 0

    t = 0
    while 1:
        # complete
        for i in range(len(slots)):
            slot = slots[i]
            if slot:
                slot[1] -= 1
                if slot[1] == 0:
                    completed.append(slot[0])
                    slots[i] = None
                    
        # start
        for i in range(len(slots)):
            if not slots[i]:
                step = next_step()
                if step:
                    slots[i] = [step, base_duration + duration(step)]

        debug(t, slots, completed)

        # done?
        if len(completed) == len(all_steps):
            break

        t += 1

    print(t)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
