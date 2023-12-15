#!/usr/bin/env pypy3

import sys
from collections import OrderedDict

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines[0].split(',')

def h(s):
    v = 0
    for c in s:
        v += ord(c)
        v *= 17
        v %= 256
    return v

def part1(items):
    tot = 0
    for item in items:
        tot += h(item)
    print(tot)

def part2(items):
    boxes = [OrderedDict() for _ in range(256)]
    for item in items:
        if item[-1] == '-':
            label = item[:-1]
            box = boxes[h(label)]
            if label in box:
                del box[label]
        else:
            label, power = item.split('=')
            power = int(power)
            boxes[h(label)][label] = power

    tot = 0
    for i, box in enumerate(boxes):
        for j, power in enumerate(box.values()):
            tot += (i+1) * (j+1) * power
    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
