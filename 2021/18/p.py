#!/usr/bin/env python3

import json
import sys

DEBUG = sys.argv.count('-v')

def parse_input():
    lines = [json.loads(_.strip('\r\n')) for _ in sys.stdin]
    return lines

def to_tree(o):
    if isinstance(o, int):
        return Int(o)
    n = Node(to_tree(o[0]), to_tree(o[1]))
    n.left.parent = n
    n.right.parent = n
    return n

class Int:
    def __init__(self, value):
        self.value = value
        self.parent = None

    @property
    def magnitude(self):
        return self.value

    def __repr__(self):
        return f'{self.value}'

class Node:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.parent = None

    def is_term(self):
        return isinstance(self.left, Int) and isinstance(self.right, Int)

    @property
    def magnitude(self):
        return self.left.magnitude * 3 + self.right.magnitude * 2

    def __repr__(self):
        return f'[{self.left}, {self.right}]'

def find_explode(num, depth=0):
    if isinstance(num, Int):
        return None

    if num.is_term():
        return num if depth >= 4 else None

    if n := find_explode(num.left, depth+1):
        return n
    return find_explode(num.right, depth+1)

def explode(num):
    '''
    If any pair is nested inside four pairs, the leftmost such pair explodes.
    '''
    x = find_explode(num)
    if not x:
        return False

    if DEBUG:
        print('explode', num, x)

    if 1:
        # find left - go up until we're on the right, then if we didn't hit the
        # root, down left one, then down right to Int...
        n = x
        while n.parent and n.parent.left == n:
            n = n.parent

        if n.parent:
            n = n.parent.left
            while not isinstance(n, Int):
                n = n.right
            n.value += x.left.value

        # find right - same except opposite pointers down
        n = x
        while n.parent and n.parent.right == n:
            n = n.parent

        if n.parent:
            n = n.parent.right
            while not isinstance(n, Int):
                n = n.left
            n.value += x.right.value
    else:
        def flatten(num):
            if isinstance(num, Int):
                return [num]
            return flatten(num.left) + flatten(num.right)

        # other option is to recursively flatten, then just look left and
        # right...
        L = flatten(num)

        # find left number
        idx = L.index(x.left)
        if idx > 0:
            L[idx-1].value += x.left.value

        # find right number
        idx = L.index(x.right)
        if idx < len(L)-1:
            L[idx+1].value += x.right.value

    # replace x with 0
    n = Int(0)
    n.parent = x.parent
    if x.parent.left == x:
        x.parent.left = n
    else:
        x.parent.right = n

    return True

def find_split(num):
    if isinstance(num, Int):
        return num if num.value >= 10 else None

    if n := find_split(num.left):
        return n
    return find_split(num.right)

def split(num):
    x = find_split(num)
    if not x:
        return False

    if DEBUG:
        print('split', num, x)

    # create Node(Int, Int) with proper values
    left = Int(x.value // 2)
    right = Int(x.value // 2 + x.value % 2)

    n = Node(left, right)
    left.parent = n
    right.parent = n

    # replace x with n
    n.parent = x.parent
    if x.parent.left == x:
        x.parent.left = n
    else:
        x.parent.right = n

    return True

def reduce(num):
    '''
    To reduce a snailfish number, you must repeatedly do the first action in
    this list that applies to the snailfish number:

    If any pair is nested inside four pairs, the leftmost such pair explodes.
    If any regular number is 10 or greater, the leftmost such regular number splits.
    '''

    # note, short-circuit "or" here, we explode or split on each pass and keep
    # looping until neither fire...
    while explode(num) or split(num):
        pass

def add(a, b):
    c = Node(a, b)
    a.parent = c
    b.parent = c
    reduce(c)
    return c

def snail_sum(nums):
    a = nums[0]
    for b in nums[1:]:
        a = add(a, b)
    return a

def part1(data):
    # magnitude of sum of all numbers

    data = [to_tree(_) for _ in data]

    num = snail_sum(data)
    if DEBUG:
        print(num)

    print(num.magnitude)

def part2(data):
    # max magnitude of any two numbers - addition is not commutative...

    mx = [None, None, None, 0]
    for a in data:
        for b in data:
            if a != b:
                c = add(to_tree(a), to_tree(b))
                mag = c.magnitude
                if mag > mx[-1]:
                    mx = [a, b, c, mag]

    if DEBUG:
        for item in mx[:3]:
            print(item)

    print(mx[3])

def main():
    data = parse_input()

    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
