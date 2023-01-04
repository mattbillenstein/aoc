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

def match_message(message, rule, rules):
    if isinstance(rule, str):
        # consume a char
        if rule == message[0]:
            return rule, message[1:]
        return '', message
    elif isinstance(rule, int):
        return match_message(message, rules[rule], rules)
    elif isinstance(rule, list):
        # match each part
        left = message
        consumed = ''
        for x in rule:
            c, left = match_message(left, x, rules)
            consumed += c
        return consumed, left
    elif isinstance(rule, tuple):
        # match either side and return best match
        c1, left1 = match_message(message, rule[0], rules)
        c2, left2 = match_message(message, rule[1], rules)
        if len(c1) > len(c2):
            return c1, left1
        return c2, left2
    else:
        assert 0, rule

def part1(rules, messages):
    count = 0
    for m in messages:
        consumed, left = match_message(m, rules[0], rules)
        if not left:
            count += 1

    print(count)

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
