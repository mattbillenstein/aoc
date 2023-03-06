#!/usr/bin/env pypy3

import sys
import time

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    hall = list('.. . . . ..')
    rooms = [[] for _ in range(4)]
    for r, c in [(0, 3), (1, 5), (2, 7), (3, 9)]:
        rooms[r].append(lines[2][c])
        rooms[r].append(lines[3][c])
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
    ((0, 0), 0): 3,
    ((0, 0), 1): 2,
    ((0, 0), 3): 2,
    ((0, 0), 5): 4,
    ((0, 0), 7): 6,
    ((0, 0), 9): 8,
    ((0, 0), 10): 9,

    ((1, 0), 0): 5,
    ((1, 0), 1): 4,
    ((1, 0), 3): 2,
    ((1, 0), 5): 2,
    ((1, 0), 7): 4,
    ((1, 0), 9): 6,
    ((1, 0), 10): 7,

    ((2, 0), 0): 7,
    ((2, 0), 1): 6,
    ((2, 0), 3): 4,
    ((2, 0), 5): 2,
    ((2, 0), 7): 2,
    ((2, 0), 9): 4,
    ((2, 0), 10): 5,

    ((3, 0), 0): 9,
    ((3, 0), 1): 8,
    ((3, 0), 3): 6,
    ((3, 0), 5): 4,
    ((3, 0), 7): 2,
    ((3, 0), 9): 2,
    ((3, 0), 10): 3,
}

# reverse mapping and add additional positions to the rooms
for k, v in list(dists.items()):
    x, h = k
    r, p = x
    dists[((r, p+1), h)] = v+1
    dists[((r, p+2), h)] = v+2
    dists[((r, p+3), h)] = v+3

    # also reverse mapping
    dists[(h, (r, p))] = v
    dists[(h, (r, p+1))] = v+1
    dists[(h, (r, p+2))] = v+2
    dists[(h, (r, p+3))] = v+3

room_to_hall = {
    # room: hall left and right in order, break if occupied...
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
        for i in range(len(self.rooms[0])):
            print('###' + '#'.join(_[i] for _ in self.rooms) + '###')
        print('#############')

    def finished(self):
        for pod, r in pod_rooms:
            if any(_ != pod for _ in self.rooms[r]):
                return False
        return True

    def could_solve(self):
        for pod, r in pod_rooms:
            if any(_ not in ('.', pod) for _ in self.rooms[r]):
                return False
        return True

    def best_score(self):
        # best we could score if we could place everything
        score = self.energy
        for h, c in enumerate(self.hall):
            if c not in ('.', ' '):
                end = (dest[c], 0)
                score += dists[(h, end)] * power[c]
        return score

    def hash(self):
        return hash((tuple(tuple(_) for _ in self.rooms), tuple(self.hall)))

_last = time.time()
visited = {}

def dfs(state, best):
    global _last
    if DEBUG and time.time() - _last > 5:
        _last = time.time()
        print(best[0] and best[0].energy)
        state.print()
        print()

    if state.finished():
        if not best[0] or state.energy < best[0].energy:
            best[0] = state
        return

    h = state.hash()
    if h in visited and visited[h] < state.energy:
        return
    visited[h] = state.energy

    # costly
    if 'D' in state.hall[:4]:
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

    # can we put a pod into a room? Push state for every pod we could place
    # in a room...
    for h, pod in enumerate(state.hall):
        if pod in dest:
            r = dest[pod]

            # path clear to room
            if any(state.hall[_] != '.' for _ in hall_to_room[(h, r)]):
                continue

            room = state.rooms[r]
            if all(_ in ('.', pod) for _ in room):
                p = len(room) - 1
                while room[p] == pod:
                    p -= 1

                s = state.copy()
                s.move(h, (r, p))
                dfs(s, best)

    # take a pod out into any one of the free spots in the hall if possible
    for r, room in enumerate(state.rooms):
        pod = dest[r]
        if any(_ in 'ABCD' and _ != pod for _ in room):
            p = 0
            while room[p] == '.':
                p += 1

            for dir in (0, 1):
                for h in room_to_hall[r][dir]:
                    if state.hall[h] != '.':
                        break

                    s = state.copy()
                    s.move((r, p), h)
                    dfs(s, best)


def part1(rooms, hall):
    state = State(rooms, hall)
    if DEBUG:
        state.print()

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

    print(best.energy)

def part2(rooms, hall):
    # splice new data into rooms between first and second row

    #D#C#B#A#
    #D#B#A#C#

    visited.clear()

    for r, s in enumerate(['DD', 'CB', 'BA', 'AC']):
        for c in s:
            rooms[r].insert(-1, c)

    part1(rooms, hall)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
