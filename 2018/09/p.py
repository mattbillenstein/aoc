#!/usr/bin/env pypy3

import itertools
import math
import sys
import time
from collections import defaultdict
from pprint import pprint

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    L = lines[0].split()
    return (int(L[0]), int(L[6]))

class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

def play(players, last):
    scores = [0] * players
    player = -1
    current = None

    for i in range(last+1):
        player += 1
        if player == players:
            player = 0 

        if i and i % 23 == 0:
            scores[player] += i
            for i in range(6):
                current = current.prev

            # remove prev
            scores[player] += current.prev.value
            current.prev.prev.next = current
            current.prev = current.prev.prev
            continue

        n = Node(i)
        if not current:
            current = n
            n.next = n
            n.prev = n
        else:
            x = current.next
            n.next = x.next
            n.prev = x
            x.next.prev = n
            x.next = n

            current = n

    return max(scores)

def part1(data):
    players, last = data
    score = play(players, last)
    print(score)

def part2(data):
    players, last = data
    score = play(players, last*100)
    print(score)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
