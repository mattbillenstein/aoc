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
    lines.sort()

    events = []
    for line in lines:
        for c in '[]#:':
            line = line.replace(c, ' ')
        dt, h, m, *evt = line.split()
        h = int(h)
        m = int(m)

        if evt[0] == 'Guard':
            guard_id = int(evt[1])
        elif evt[0] == 'wakes':
            wakes = m
            events.append({'dt': dt, 'h': h, 'guard_id': guard_id, 'sleeps': sleeps, 'wakes': wakes})
        elif evt[0] == 'falls':
            sleeps = m

    return events

def part(events):
    guards = defaultdict(int)
    mins = defaultdict(lambda: defaultdict(int))

    for evt in events:
        guards[evt['guard_id']] += evt['wakes'] - evt['sleeps']
        for m in range(evt['sleeps'], evt['wakes']):
            mins[evt['guard_id']][m] += 1

    if DEBUG:
        pprint(guards)
        pprint(mins)

    guards = sorted((v, k) for k, v in guards.items())

    guard_id = guards[-1][1]

    min = sorted((v, k) for k, v in mins[guard_id].items())[-1][1]

    print(guard_id * min)

    gid = None
    mx = 0
    for guard_id, d in mins.items():
        if max(d.values()) > mx:
            mx = max(d.values())
            gid = guard_id

    for m, cnt in mins[gid].items():
        if cnt == mx:
            debug(gid, m, cnt)
            print(gid * m)

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
