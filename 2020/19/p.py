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
            continue
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
        else:
            messages.append(line)

    return rules, messages

def expand_tuple(item):
    is_tuple = isinstance(item, tuple)
    is_list = isinstance(item, list)
    is_str = isinstance(item, str)

    if is_str:
        return item

    if is_list and len(item) == 1:
        return item[0]

    if is_tuple and all(isinstance(_, str) for _ in item):
        return item

    if is_tuple and all(isinstance(_, tuple) for _ in item):
        assert len(item) == 2, item
        assert all(isinstance(_, str) for _ in item[0])
        assert all(isinstance(_, str) for _ in item[1])
        return tuple(sorted(set(item[0] + item[1])))

    # reduce lists > length 2
    while len(item) > 2:
        assert is_list
        item = [expand_tuple(item[:2])] + item[2:]

    # now, actually expand against tuple
    res = None
    a, b = item
    if isinstance(a, tuple):
        if isinstance(b, tuple):
            res = tuple(s1 + s2 for s1 in a for s2 in b)
        else:
            assert isinstance(b, str), b
            res = tuple(s + b for s in a)
    else:
        assert isinstance(a, str), a
        if isinstance(b, tuple):
            res = tuple(a + s for s in b)
        else:
            assert isinstance(b, str), b
            if is_list:
                # list of string, combine
                res = a + b
            else:
                # 2-tuple str handled above
                assert 0, (a, b)

    assert res is not None
    return res

def expand_rule(rule, rules):
    if isinstance(rule, str):
        return rule

    if isinstance(rule, int):
        return expand_rule(rules[rule], rules)

    if isinstance(rule, tuple):
        # expand |
        assert len(rule) == 2
        rule = (expand_rule(rule[0], rules), expand_rule(rule[1], rules))
        return expand_tuple(rule)

    assert isinstance(rule, list)
    rule = [expand_rule(rules[_], rules) for _ in rule]

    while 1:
        x = expand_tuple(rule)
        if x == rule:
            break
        rule = x

    return rule

def part1(rules, messages):
    pprint(rules)
    print()

    eight = expand_rule(rules[8], rules)
    eleven = expand_rule(rules[11], rules)

    print(len(eight), len(eleven))

    valid = expand_rule(rules[0], rules)
    print(len(valid))
#    print(valid)
    d = defaultdict(int)
    for x in valid:
        d[len(x)] += 1

    pprint(d)

    with open('valid.txt', 'w') as f:
        for s in valid:
            f.write(s + '\n')

    valid = set(valid)
    debug('valid', len(valid))

    cnt = 0
    d = defaultdict(int)
    for m in messages:
        d[len(m)] += 1
        if m in valid:
            cnt += 1
        else:
#            print(m)
            pass
    print(cnt)

    pprint(d)

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
