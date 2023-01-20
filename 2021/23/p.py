#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    hall = list('.. . . . ..')
    rooms = [[] for _ in range(4)]
    for r, c in [(0, 3), (1, 5), (2, 7), (3, 9)]:
        rooms[r].append(lines[3][c])
        rooms[r].append(lines[2][c])
    return rooms, hall

# power per step
power = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

# room and position to hall position distances
dists = {
    # ((room, position), hall spot): distance
    ((0, 0), 0): 4,
    ((0, 0), 1): 3,
    ((0, 0), 3): 3,
    ((0, 0), 5): 5,
    ((0, 0), 7): 7,
    ((0, 0), 9): 9,
    ((0, 0), 10): 10,

    ((1, 0), 0): 6,
    ((1, 0), 1): 5,
    ((1, 0), 3): 3,
    ((1, 0), 5): 3,
    ((1, 0), 7): 5,
    ((1, 0), 9): 7,
    ((1, 0), 10): 8,

    ((2, 0), 0): 8,
    ((2, 0), 1): 7,
    ((2, 0), 3): 5,
    ((2, 0), 5): 3,
    ((2, 0), 7): 3,
    ((2, 0), 9): 5,
    ((2, 0), 10): 6,

    ((3, 0), 0): 10,
    ((3, 0), 1): 9,
    ((3, 0), 3): 7,
    ((3, 0), 5): 5,
    ((3, 0), 7): 3,
    ((3, 0), 9): 3,
    ((3, 0), 10): 4,
}

# the top room position is just one less step to any hall position
for k, v in list(dists.items()):
    x, h = k
    r, p = x
    dists[((r, p+1), h)] = v-1

    # also reverse mapping
    dists[(h, (r, p))] = v
    dists[(h, (r, p+1))] = v-1

# from each room, hall slots to try in order, break if occupied...
neighbors = {
    0: ([1, 0], [3, 5, 7, 9, 10]),
    1: ([3, 1, 0], [5, 7, 9, 10]),
    2: ([5, 3, 1, 0], [7, 9, 10]),
    3: ([7, 5, 3, 1, 0], [9, 10]),
}

clear = {
    # (hall, room): [hall spots to check]
    (0, 0): [1],
    (1, 0): [],
    (3, 0): [],
    (5, 0): [3],
    (7, 0): [5, 3],
    (9, 0): [7, 5, 3],
    (10, 0): [9, 7, 5, 3],

    (0, 1): [1, 3],
    (1, 1): [3],
    (3, 1): [],
    (5, 1): [],
    (7, 1): [5],
    (9, 1): [7, 5],
    (10, 1): [9, 7, 5],

    (0, 2): [1, 3, 5],
    (1, 2): [3, 5],
    (3, 2): [5],
    (5, 2): [],
    (7, 2): [],
    (9, 2): [7],
    (10, 2): [9, 7],

    (0, 3): [1, 3, 5, 7],
    (1, 3): [3, 5, 7],
    (3, 3): [5, 7],
    (5, 3): [7],
    (7, 3): [],
    (9, 3): [],
    (10, 3): [9],
}

# pod -> destination room
dest = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
}
dest.update({v: k for k, v in dest.items()})

class State:
    def __init__(self, rooms, hall, energy=0):
        self.rooms = [list(_) for _ in rooms]
        self.hall = list(hall)
        self.energy = energy
        self.last = None

    def finished(self):
        for pod, r in [('A', 0), ('B', 1), ('C', 2), ('D', 3)]:
            if self.rooms[r] != [pod, pod]:
                return False
        return True

    def get(self, pos):
        if isinstance(pos, tuple):
            return self.rooms[pos[0]][pos[1]]
        return self.hall[pos]

    def set(self, pos, v):
        if isinstance(pos, tuple):
            self.rooms[pos[0]][pos[1]] = v
        else:
            self.hall[pos] = v

    def move(self, start, end):
        # move (swap) start/end, add cost of this to energy
        pod = self.get(start)
        self.energy += dists[(start, end)] * power[pod]
        tmp = self.get(end)
        self.set(end, self.get(start))
        self.set(start, tmp)

    def copy(self):
        s = State(self.rooms, self.hall, self.energy)
        s.last = self
        return s

    def print(self):
        print('#' * (len(self.hall)+2), self.energy)
        print('#' + ''.join(self.hall) + '#')
        print('###' + '#'.join(_[1] for _ in self.rooms) + '###')
        print('  #' + '#'.join(_[0] for _ in self.rooms) + '#  ')
        print('  #########  ')

def dfs(state):
    stack = [state]
    best = None
    while stack:
        state = stack.pop()

        if DEBUG:
            state.print()
            print()
            time.sleep(3)

        if state.finished():
            if not best or state.energy < best.energy:
                best = state
                best.print()
            continue

        if best and state.energy > best.energy:
            continue

        # can we put a pod into a room? Push state for every pod we could place
        # in a room...
        for h, c in enumerate(state.hall):
            if c in dest:
                r = dest[c]

                # path clear to room
                if not all(_ == '.' for _ in clear[(h, r)]):
                    continue

                room = state.rooms[r]
                if all(_ in ('.', c) for _ in room):
                    s = state.copy()
                    if DEBUG:
                        s.print()
                    p = 0 if room[0] == '.' else 1
                    s.move(h, (r, p))
                    stack.append(s)
                    if DEBUG:
                        s.print()
                        print()

        # otherwise take a pod out into any one of the free spots in the hall
        # if any
        for r, room in enumerate(state.rooms):
            pod = dest[r]
            if any(_ in 'ABCD' and _ != pod for _ in room):
                p = 1 if room[1] != '.' else 0
                for dir in (0, 1):
                    for h in neighbors[r][dir]:
                        if state.hall[h] != '.':
                            break
                        s = state.copy()
                        if DEBUG:
                            s.print()
                            print()
                        s.move((r, p), h)
                        stack.append(s)
                        if DEBUG:
                            s.print()
                            print()

    return best

def part1(rooms, hall):
    state = State(rooms, hall)
    state.print()
    print()
    best = dfs(state)
    print(best.energy)

    s = best
    L = []
    while s:
        L.append(s)
        s = s.last

    L.reverse()
    for s in L:
        s.print()
        print()

def part2(data):
    pass

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
