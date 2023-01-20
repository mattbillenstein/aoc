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

# from each room, hall slots to try in order, break if blocked
room_to_hall = {
    0: ([1, 0], [3, 5, 7, 9, 10]),
    1: ([3, 1, 0], [5, 7, 9, 10]),
    2: ([5, 3, 1, 0], [7, 9, 10]),
    3: ([7, 5, 3, 1, 0], [9, 10]),
}

hall_to_room = {
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
pod_rooms = [('A', 0), ('B', 1), ('C', 2), ('D', 3)]
dest = dict(pod_rooms)
dest.update({r: p for p, r in pod_rooms})

class State:
    def __init__(self, rooms, hall, energy=0):
        self.rooms = [list(_) for _ in rooms]
        self.hall = list(hall)
        self.energy = energy
        self.last = None

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
        assert tmp == '.'
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

    def finished(self):
        for pod, r in pod_rooms:
            if self.rooms[r] != [pod, pod]:
                return False
        return True

    def could_solve(self):
        for pod, r in pod_rooms:
            room = self.rooms[r]
            if not all(_ in ('.', pod) for _ in room):
                return False
        return True

    def best_score(self):
        # best we could score if we could place everything
        score = self.energy
        for h, c in enumerate(self.hall):
            if c not in ('.', ' '):
                end = (dest[c], 1)
                score += dists[(h, end)] * power[c]
        return score

_last = time.time()

def dfs(state, best):
    global _last
    if DEBUG and time.time() - _last > 5:
        _last = time.time()
        print(best[0] and best[0].energy)
        state.print()
        print()
#        time.sleep(3)

    # costly
    if 'D' in state.hall[:2]:
        return

    # impossible to solve
    for d, a in [(3, 5), (5, 7), (3, 7)]:
        if state.hall[d] == 'D' and state.hall[a] == 'A':
            return
    for d, b in [(5, 7)]:
        if state.hall[d] == 'D' and state.hall[b] == 'B':
            return
    for c, a in [(3, 5)]:
        if state.hall[c] == 'C' and state.hall[a] == 'A':
            return

    if best[0]:
        # if used energy > best
        if state.energy > best[0].energy:
            return

        # if rooms are clear of other pods and best we could do > best found
        if state.could_solve() and state.best_score() > best[0].energy:
            return

    if state.finished():
        if not best[0] or state.energy < best[0].energy:
            best[0] = state
#            best[0].print()
#            print()
        return

    # can we put a pod into a room? Push state for every pod we could place
    # in a room...
    for h, c in enumerate(state.hall):
        if c in dest:
            r = dest[c]

            # path clear to room
            if any(state.hall[_] != '.' for _ in hall_to_room[(h, r)]):
                continue

            room = state.rooms[r]
            if all(_ in ('.', c) for _ in room):
                p = 0 if room[0] == '.' else 1
                s = state.copy()
                s.move(h, (r, p))
                dfs(s, best)

    # take a pod out into any one of the free spots in the hall if possible
    for r, room in enumerate(state.rooms):
        pod = dest[r]
        if any(_ in 'ABCD' and _ != pod for _ in room):
            p = 1 if room[1] != '.' else 0
            for dir in (0, 1):
                for h in room_to_hall[r][dir]:
                    if state.hall[h] != '.':
                        break

                    s = state.copy()
                    s.move((r, p), h)
                    dfs(s, best)


def part1(rooms, hall):
    state = State(rooms, hall)

#    best = [state.copy()]
#    best[0].energy = 20000 

    best = [None]
    dfs(state, best)
    best = best[0]

    if DEBUG:
        s = best
        L = []
        while s:
            L.append(s)
            s = s.last

        L.reverse()
        for s in L:
            s.print()
            print()

    print('BEST', best.energy)

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
