#!/usr/bin/env python3

# I really need a set of canned graph algorithms I can rely on - reinventing
# the wheel every problem is killing a lot of nights...

# https://www.reddit.com/r/adventofcode/comments/zu7kq8/advice_maybe_abstract_your_searches/
# https://www.reddit.com/r/adventofcode/comments/zubqho/2022_day_24_why_bfs_not_dfs/

# bfs - shortest path
# dfs - find a path, need a lot of pruning probably...
# djikstra
# astar?

import itertools
import sys
from heapq import heappop, heappush

def bfs(frontier, neighbors, end=None):
    # neighbors is a function that takes a vertex and yields neighboring
    # vertices...

    if not isinstance(frontier, (list, set)):
        frontier = [frontier]

    distance = 0
    visited = set()
    while 1:
        next_frontier = set()
        for x in frontier:
            if x == end:
                return distance

            visited.add(x)
            for y in neighbors(x):
                if y not in visited:
                    next_frontier.add(y)

        frontier = next_frontier

        if not frontier:
            return distance

        distance += 1

def part1(mem):
    prog = intcode(mem)
    next(prog)

    g = SparseGrid([], {'.': 0, '#': 1, 'O': 2, 'X': 3})
    pos = (0, 0)
    g.set(pos, 3)
    visited = set([pos])

    # N=1, S=2, W=3, E=4

    rdir = {'N': 1, 'S': 2, 'W': 3, 'E': 4}
    dir = 'N'
    end = None

    # found this visited size by just letting this run awhile... and printing
    # the grid...
    while len(visited) < 799:
        dir = random.choice([_ for _ in 'NSEW' if _ != dir])
        result = None
        while result is None:
            result = prog.send(rdir[dir])

        npos = g.step(pos, dir)
        if result in (1, 2):
            pos = npos
            visited.add(pos)
        else:
            # set wall and make a random turn
            g.set(npos, 1)

        if result == 2:
            end = pos
            g.set(pos, 2)

    if DEBUG:
        print()
        g.print()

    def neighbors(pt):
        for dir in 'NSEW':
            npt = g.step(pt, dir)
            if npt in visited:
                yield npt

    distance = bfs([end], (0, 0), neighbors)
    print(distance)

    # to compute time to fill, just BFS with no start point...
    distance = bfs([end], None, neighbors)
    print(distance)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()




def dijkstra(graph, start, end=None):
    '''
    From Wikipedia
     1  function Dijkstra(Graph, source):
     2
     3      for each vertex v in Graph.Vertices:
     4          dist[v] ← INFINITY
     5          prev[v] ← UNDEFINED
     6          add v to Q
     7      dist[source] ← 0
     8
     9      while Q is not empty:
    10          u ← vertex in Q with min dist[u]
    11          remove u from Q
    12
    13          for each neighbor v of u still in Q:
    14              alt ← dist[u] + Graph.Edges(u, v)
    15              if alt < dist[v]:
    16                  dist[v] ← alt
    17                  prev[v] ← u
    18
    19      return dist[], prev[]
    '''

    pq = PriorityQueue()
    dist = {}
    prev = {}
    for v in graph:
        dist[v] = sys.maxsize
        prev[v] = None
        pq.add_task(v)

    dist[start] = 0

    while pq:
        u = pq.pop_task()
        if u == end:
            break
        for v, w in graph[u]:
            if v in pq:
                alt = dist[u] + w
                if alt < dist[v]:
                    pq.add_task(v, alt)
                    dist[v] = alt
                    prev[v] = u

    if end:
        path = []
        pt = end
        while 1:
            path.append((pt, dist[pt]))
            if pt == start:
                break
            pt = prev[pt]
        path.reverse()
        return path

    return dist, prev


class PriorityQueue:
    '''https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes'''

    def __init__(self):
        self.pq = []                         # list of entries arranged in a heap
        self.entry_finder = {}               # mapping of tasks to entries
        self.REMOVED = '<removed-task>'      # placeholder for a removed task
        self.counter = itertools.count()     # unique sequence count

    def add_task(self, task, priority=sys.maxsize):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def remove_task(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task = heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task
        return None

    def __contains__(self, task):
        return task in self.entry_finder

    def __bool__(self):
        return bool(self.entry_finder)

