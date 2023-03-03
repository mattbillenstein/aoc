#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    lines = [int(_) for _ in lines[0]]
    return lines

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

def run(head, times):
    index = dict()
    n = head
    while 1:
        index[n.value] = n
        n = n.next
        if n == head:
            break

    highest = max(index)

    current = head.value

    for i in range(times):
        c = index[current]
        cups = c.next
        last = cups.next.next
        c.next = last.next

        n = cups
        L = []
        for _ in range(3):
            L.append(n.value)
            n = n.next

        dest = current
        while dest == current or dest in L:
            dest -= 1
            if dest == 0:
                dest = highest

        n = index[dest]
        last.next = n.next
        n.next = cups

        current = c.next.value

    if len(index) < 100:
        s = ''
        n = index[1]
        n = n.next
        while n.value != 1:
            s += str(n.value)
            n = n.next

        print(s)
    else:
        print(index[1].next.value * index[1].next.next.value)

def part1(items):
    # turn items into linked-list
    head = n = Node(items[0])
    for i in items[1:]:
        n.next = n = Node(i)

    # make a ring
    n.next = head

    run(head, 100)

def part2(items):
    # turn items into linked-list
    head = n = Node(items[0])
    for i in items[1:]:
        n.next = n = Node(i)

    # add all the items after given list up to 1,000,000
    for i in range(max(items)+1, 1_000_000+1):
        n.next = n = Node(i)

    # make a ring
    n.next = head

    run(head, 10_000_000)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
