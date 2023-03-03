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
    data = [int(_) for _ in lines[0].split()]
    return data

class Node:
    def __init__(self, nodes, metadata):
        self.nodes = nodes
        self.metadata = metadata

    @property
    def value(self):
        if not self.nodes:
            return sum(self.metadata)

        tot = 0
        for idx in self.metadata:
            idx -= 1
            if 0 <= idx < len(self.nodes):
                tot += self.nodes[idx].value

        return tot

    def __repr__(self):
        return f'Node({len(self.nodes)}, {self.metadata})'


def parse_nodes(data, offset, count):
    nodes = []
    for i in range(count):
        num_nodes = data[offset]
        offset += 1
        num_metadata = data[offset]
        offset += 1
        child_nodes, offset = parse_nodes(data, offset, num_nodes)
        metadata = data[offset:offset + num_metadata]
        offset += num_metadata
        nodes.append(Node(child_nodes, metadata))

    return nodes, offset

def yield_nodes(node):
    yield node
    for n in node.nodes:
        for n2 in yield_nodes(n):
            yield n2

def part(data):
    nodes, _ = parse_nodes(data, 0, 1)

    tot = 0
    for n in yield_nodes(nodes[0]):
        tot += sum(n.metadata)

    print(tot)

    # part2
    print(nodes[0].value)


def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
