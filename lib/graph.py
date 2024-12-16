#!/usr/bin/env pypy3

# I really need a set of canned graph algorithms I can rely on - reinventing
# the wheel every problem is killing a lot of nights...

# https://www.reddit.com/r/adventofcode/comments/zu7kq8/advice_maybe_abstract_your_searches/
# https://www.reddit.com/r/adventofcode/comments/zubqho/2022_day_24_why_bfs_not_dfs/

# bfs - shortest path
# dfs - find a path, need a lot of pruning probably...
# dijkstra
# astar?

import itertools
import sys
import time
from collections import defaultdict, deque
from heapq import heappop, heappush

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

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

    def __len__(self):
        return len(self.entry_finder)

class BucketHeap:
    def __init__(self):
        self.heap = defaultdict(deque)
        self.min_bucket = sys.maxsize
        self.count = 0

    def add_task(self, element, cost):
        self.heap[cost].append(element)
        if cost < self.min_bucket:
            self.min_bucket = cost
        self.count += 1

    def pop_task(self):
        min_element = self.heap[self.min_bucket].popleft()
        if not self.heap[self.min_bucket]:
            del self.heap[self.min_bucket]
            self.min_bucket = sys.maxsize
            if self.heap:
                self.min_bucket = min(self.heap)
        self.count -= 1
        return min_element

    def __bool__(self):
        return bool(self.count)

    def __len__(self):
        return self.count

def bfs(frontier, neighbors, end=None):
    # neighbors is a function that takes a vertex and yields neighboring
    # vertices...
    #
    # if you need the path, collect {npt: pt} in neighbors function...
    found = []

    if not isinstance(frontier, (list, set)):
        frontier = [frontier]

    distance = 0
    visited = set()
    while 1:
        next_frontier = set()
        for x in frontier:
            if isinstance(end, set) and x in end:
                found.append((x, distance))
            elif x == end:
                return distance

            visited.add(x)
            for y in neighbors(x):
                if y not in visited:
                    next_frontier.add(y)

        frontier = next_frontier

        if not frontier:
            if isinstance(end, set):
                return found
            if end:
                return None
            return distance

        distance += 1

_last = 0.0
def dfs(state, queue_class=BucketHeap):
    # dfs, to use this you need to implement a state class, see 2016/24 for an
    # example
    global _last

    visited = {}
    best = None

    q = queue_class()
    q.add_task(state, state.cost)

    while q:
        assert len(q) < 10_000_000, 'Too much fanout?'
        state = q.pop_task()

        if best and state.cost > best.cost:
            continue

        if DEBUG > 1:
            if time.time() - _last > 10:
                _last = time.time()
                print(state, best, len(q), len(visited))
                if visited:
                    mn = min(visited.values())
                    for k, v in visited.items():
                        if v == mn:
                            print('  ', k, v)

        if state.done:
            if not best or state.cost < best.cost:
                best = state
                debug('Found best:', best)
            continue

        k = state.key
        if k:
            if k in visited and visited[k] <= state.cost:
                continue
            visited[k] = state.cost

        for s in state.next():
            k = s.key
            if k in visited and visited[k] <= s.cost:
                continue
            q.add_task(s, s.cost)

    return best

def dfs_longest(start, end, graph):
    best = [None, 0]
    visited = set()

    def _dfs(pos, dist):
        visited.add(pos)
        if pos == end and dist > best[1]:
            best[0] = list(visited)
            best[1] = dist
        else:
            for v, d in graph[pos]:
                if v not in visited:
                    _dfs(v, dist + d)
        visited.remove(pos)
    _dfs(start, 0)

    return best

def dfs_shortest(start, end, graph):
    best = [None, sys.maxsize]
    visited = set()

    def _dfs(pos, dist):
        visited.add(pos)
        if pos == end and dist < best[1]:
            best[0] = list(visited)
            best[1] = dist
        else:
            for v, d in graph[pos]:
                if v not in visited:
                    _dfs(v, dist + d)
        visited.remove(pos)
    _dfs(start, 0)

    return best

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
        dist[v] = d = 0 if v == start else sys.maxsize
        prev[v] = None
        pq.add_task(v, d)

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
