#!/usr/bin/env pypy3

import sys
import time
from collections import defaultdict
from pprint import pprint

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    lines = [int(_) for _ in lines]
    return lines

class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

def mix(data, key=1, rounds=1):
    nodes = [Node(_ * key) for _ in data]
    for i in range(1, len(nodes)):
        nodes[i-1].next = nodes[i]
        nodes[i].prev = nodes[i-1]
    nodes[0].prev = nodes[-1]
    nodes[-1].next = nodes[0]

    for _ in range(rounds):
        for node in nodes:
            x = node.value
            x = x % (len(nodes)-1)

            for _ in range(0, x):
                if x < 0:
                    prev = node.prev
                    node.next.prev = prev
                    node.prev = prev.prev
                    prev.prev.next = node
                    prev.next = node.next
                    node.next = prev
                    prev.prev = node
                else:
                    next = node.next
                    node.prev.next = next
                    node.next.prev = node.prev
                    node.next = node.next.next
                    node.prev = next
                    next.next.prev = node
                    next.next = node

    zero = None
    for n in nodes:
        if n.value == 0:
            zero = n
            break

    sum = 0
    n = zero
    for i in range(3):
        for _ in range(1000):
            n = n.next
        print(n.value)
        sum += n.value
    print('SUM', sum)

def part1(data):
    mix(data)

def part2(data):
    mix(data, key=811589153, rounds=10)

def main(argv):
    data = parse_input()
    part1(data)
    print()
    part2(data)

if __name__ == '__main__':
    main(sys.argv)
