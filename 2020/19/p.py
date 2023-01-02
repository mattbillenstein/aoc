#!/usr/bin/env pypy3

import math
import sys
import time
from collections import defaultdict
from pprint import pprint

DEBUG = '--debug' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]

    rules = {}
    messages = []
    for line in lines:
        if not line:
            break
        if ':' in line:
            num, rest = line.replace('"', '').split(': ')
            num = int(num)
            if ' | ' in rest:
                a, b = rest.split(' | ')
                rules[num] = tuple([
                    [int(_) for _ in a.split()],
                    [int(_) for _ in b.split()],
                ])
            else:
                rest = rest.split()
                if rest[0].isdigit():
                    rules[num] = [int(_) for _ in rest]
                else:
                    assert len(rest) == 1
                    rules[num] = rest[0]

    idx = lines.index('')
    messages = lines[idx+1:]
        
    return rules, messages

def expand_tuple(item):
    is_tuple = isinstance(item, tuple)
    is_list = isinstance(item, list)

    if isinstance(item, str):
        return item

    if is_tuple and all(isinstance(_, str) for _ in item):
        return item

    if is_tuple and all(isinstance(_, tuple) for _ in item):
        assert len(item) == 2, item
        return tuple(sorted(set(item[0] + item[1])))

    if is_list and len(item) == 1:
        return item[0]

    # reduce lists > length 2
    while len(item) > 2:
        assert is_list
        item = expand_tuple(item[:2]) + item[2:]

    if is_list:
        item[0] = expand_tuple(item[0])
        item[1] = expand_tuple(item[1])

    # now, actually expand against tuple
    res = None
    a, b = item
    if isinstance(a, tuple):
        if isinstance(b, tuple):
            L2 = []
            for s1 in a:
                for s2 in b:
                    L2.append(s1 + s2)
            res = tuple(L2)
        else:
            assert isinstance(b, str), b
            L2 = []
            for s1 in a:
                L2.append(s1 + b)
            res = tuple(L2)
    else:
        assert isinstance(a, str), a
        if isinstance(b, tuple):
            L2 = []
            for s1 in b:
                L2.append(a + s1)
            res = tuple(L2)
        else:
            assert isinstance(b, str), b
            # list of string, combine
            if isinstance(item, list):
                res = ''.join(item)
            else:
                # tuple of string, options
                res = item

    assert res is not None
    return res

def expand_rule(rule, rules):
    if isinstance(rule, str):
        return rule

    if isinstance(rule, int):
        return expand_rule(rules[rule], rules)

    if isinstance(rule, tuple):
        # expand |
        return expand_tuple(tuple([expand_rule(_, rules) for _ in rule]))

    rule = [expand_rule(rules[_], rules) for _ in rule]

    while 1:
        x = expand_tuple(rule)
        if x == rule:
            rule = x
            break
        rule = x

    return rule

def part1(rules, messages):
    valid = expand_rule(rules[0], rules)
    valid = set(valid)
    debug('valid', len(valid))

    cnt = 0
    for m in messages:
        if m in valid:
            cnt += 1
        else:
            print(m)
    print(cnt)

def part2(data):
    pass

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
