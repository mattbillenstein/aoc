#!/usr/bin/env pypy3

import sys

DEBUG = sys.argv.count('-v')

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
    for consumed, left in _match_message(message, rule, rules):
        if left == '':
            return True
    return False

def _match_message(message, rule, rules):
    if isinstance(rule, str):
        # consume a char
        if message and rule == message[0]:
            yield rule, message[1:]
        else:
            yield '', message
    elif isinstance(rule, int):
        for tup in _match_message(message, rules[rule], rules):
            yield tup
    elif isinstance(rule, list):
        # match each part, peel off the first item, match, then recurse on the
        # rest...
        rule = list(rule)  # don't mutate the global rules
        x = rule.pop(0)
        for tup in _match_message(message, x, rules):
            if tup is None:
                break

            consumed, left = tup

            # we didn't match on the first rule, skip the rest
            if not consumed:
                continue

            # rule longer than left msg, can't match...
            if len(rule) > len(left):
                continue

            if rule:
                for c, lft in _match_message(left, rule, rules):
                    yield consumed + c, lft
            else:
                yield consumed, left

    elif isinstance(rule, tuple):
        # match any of the sub-expressions
        for x in rule:
            for tup in _match_message(message, x, rules):
                yield tup

def run(rules, messages):
    count = 0
    i = 0
    for msg in messages:
        i += 1
        if match_message(msg, rules[0], rules):
            count += 1
            debug(i, msg)

    print(count)

def part1(rules, messages):
    run(rules, messages)

def part2(rules, messages):
    # HACK - update so the rules don't contain loops by expanding them to some
    # arbitrary length...
    # 8: 42 | 42 8
    # 11: 42 31 | 42 11 31

    # one or more of 42
    #rules[8] = (42, [42, 8])

    L = []
    for i in range(1, 50):
        L.append([42] * i)
    rules[8] = tuple(L)

    # 42 zero or more 11
    #rules[11] = ([42, 31], [42, 11, 31])

    L = []
    for i in range(1, 25):
        L.append([42] * i + [31] * i)
    rules[11] = tuple(L)

    run(rules, messages)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
