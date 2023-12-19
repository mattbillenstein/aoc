#!/usr/bin/env pypy3

import sys
from pprint import pprint

DEBUG = sys.argv.count('-v')

def parse_rule(rule):
    x, rest = rule.split(':', 1)
    attr, op, v = x[0], x[1], x[2:]
    v = int(v)

    acc, rej = rest.split(',', 1)
    assert not ':' in acc
    if ':' in rej:
        rej = parse_rule(rej)

    return {'attr': attr, 'op': op, 'value': v, 'accept': acc, 'reject': rej}

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    flows = {}
    parts = []
    for line in lines:
        if not line:
            continue
        if line.startswith('{'):
            part = {}
            parts.append(part)
            for attr in line[1:-1].split(','):
                n, v = attr.split('=')
                part[n] = int(v)
        else:
            name, rule = line[:-1].split('{')
            flows[name] = parse_rule(rule)

    return flows, parts

def evaluate(part, rule, rules):
    v = part[rule['attr']]

    key = 'reject'
    if rule['op'] == '<' and v < rule['value']:
        key = 'accept'
    elif rule['op'] == '>' and v > rule['value']:
        key = 'accept'

    if isinstance(rule[key], dict):
        return evaluate(part, rule[key], rules)

    if rule[key] in 'AR':
        return rule[key]
    else:
        return evaluate(part, rules[rule[key]], rules)

    assert 0

def part1(rules, parts):
    if DEBUG:
        pprint(rules)
        print()
        for p in parts:
            print(p)

    tot = 0
    for part in parts:
        x = evaluate(part, rules['in'], rules)
        if x == 'A':
            tot += sum(part.values())
    print(tot)

def part2(rules, parts):
    def evaluate2(part, rule, rules, tot):
        attr = rule['attr']
        value = rule['value']

        if rule['op'] == '<':
            left = set(range(1, value))
            right = set(range(value, 4001))
        elif rule['op'] == '>':
            left = set(range(value+1, 4001))
            right = set(range(1, value+1))
        else:
            assert 0

        for key, fact in [('accept', left), ('reject', right)]:
            p = part.copy()
            p[attr] = part[attr] & fact
            if isinstance(rule[key], dict):
                evaluate2(p, rule[key], rules, tot)
            else:
                if rule[key] in 'AR':
                    if rule[key] == 'A':
                        x = 1
                        for s in p.values():
                            x *= len(s)
                        tot[0] += x
                    else:
                        assert rule[key] == 'R'
                else:
                    evaluate2(p, rules[rule[key]], rules, tot)

    tot = [0]
    part = {_: set(range(1, 4001)) for _ in 'xmas'}
    evaluate2(part, rules['in'], rules, tot)
    print(tot[0])

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
