#!/usr/bin/env pypy3

import random
import sys
import time
from collections import defaultdict
from pprint import pprint

num_to_segments = {
    0: 'abcefg',
    1: 'cf',
    2: 'acdeg',
    3: 'acdfg',
    4: 'bcdf',
    5: 'abdfg',
    6: 'abdefg',
    7: 'acf',
    8: 'abcdefg',
    9: 'abcdfg',
}

segments_to_num = {v: k for k, v in num_to_segments.items()}

length_to_nums = defaultdict(list)
for k, v in num_to_segments.items():
    length_to_nums[len(v)].append(k)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    lines = [_.split(' | ') for _ in lines]
    return [(_[0].split(), _[1].split()) for _ in lines]

#  a
# b c
#  d
# e f
#  g

def part1(data):
    cnt = 0
    for inputs, outputs in data:
        for item in outputs:
            if len(length_to_nums[len(item)]) == 1:
                cnt += 1
    print(cnt)

def decode_items(items, mapping):
    L = []
    for item in items:
        new = ''.join(sorted(mapping[_] for _ in item))
        digit = segments_to_num.get(new)
        L.append(digit)
    return L

def test_mapping(mapping, items):
    cnt = 0
    for item in items:
        new = ''.join(sorted(mapping[_] for _ in item))
        digit = segments_to_num.get(new)
        if digit is not None:
            cnt += 1
    return cnt


def part2(data):
    tot = 0
    for inputs, outputs in data:
        fixed = {}
        found = {}
        for item in inputs:
            if len(item) == 2:  # 1
                found[1] = item
            elif len(item) == 3: # 7
                found[7] = item
            elif len(item) == 4: # 4
                found[4] = item
            elif len(item) == 8: # 8
                found[8] = item
            
        if 1 in found and 7 in found:
            a = set(found[7]) - set(found[1])
            a = a.pop()
            fixed[a] = 'a'

        items = inputs + outputs
        best = 0
        best_mapping = None

        while 1:
            keys = [_ for _ in 'abcdefg' if _ not in fixed]
            values = [_ for _ in 'abcdefg' if _ not in fixed.values()]
            random.shuffle(values)
            mapping = dict(zip(keys, values), **fixed)
            score = test_mapping(mapping, items)
            if score > best:
                best = score
                best_mapping = dict(mapping)
                decoded = decode_items(items, mapping)
                if None not in decoded:
                    break

#        print(' '.join(inputs), '|', ' '.join(outputs))
#        print(decode_items(inputs, best_mapping))
#
        outs = decode_items(outputs, best_mapping)
#        print(outs)

        val = outs[0] * 1000 + outs[1] * 100 + outs[2] * 10 + outs[3]
#        print(val)
        tot += val

#        print()

    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
