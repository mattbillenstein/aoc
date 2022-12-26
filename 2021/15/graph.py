#!/usr/bin/env python3

# I really need a set of canned graph algorithms I can rely on - reinventing
# the wheel every problem is killing a lot of nights...

# https://www.reddit.com/r/adventofcode/comments/zu7kq8/advice_maybe_abstract_your_searches/
# https://www.reddit.com/r/adventofcode/comments/zubqho/2022_day_24_why_bfs_not_dfs/

# bfs - shortest path
# dfs - find a path, need a lot of pruning probably...
# djikstra
# astar?

import sys

from datastructures import PriorityQueue

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
