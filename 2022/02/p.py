#!/usr/bin/env python3

import sys

# loss is 0, draw is 3, win is 6

thing_score = {
    'R': 1,
    'P': 2,
    'S': 3,
}

opp_me_score = {
    ('R', 'P'): 6,
    ('P', 'R'): 0,

    ('R', 'S'): 0,
    ('S', 'R'): 6,

    ('P', 'S'): 6,
    ('S', 'P'): 0,

    ('R', 'R'): 3,
    ('P', 'P'): 3,
    ('S', 'S'): 3,
}

opp_code = {
    'A': 'R',
    'B': 'P',
    'C': 'S',
}

me_code = {
    'X': 'R',
    'Y': 'P',
    'Z': 'S',
}

opp_result_play = {
    ('R', 'X'): 'S',
    ('R', 'Y'): 'R',
    ('R', 'Z'): 'P',

    ('P', 'X'): 'R',
    ('P', 'Y'): 'P',
    ('P', 'Z'): 'S',

    ('S', 'X'): 'P',
    ('S', 'Y'): 'S',
    ('S', 'Z'): 'R',
}

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    matches = []
    for line in lines:
        opp, result = line.strip().split()
        matches.append((opp, result))
    return matches

def score_round(opp, me):
    opp = opp_code[opp]
    me = me_code[me]
    return thing_score[me] + opp_me_score[(opp, me)]
    
def score_round_result(opp, result):
    opp = opp_code[opp]
    me = opp_result_play[(opp, result)]
    return thing_score[me] + opp_me_score[(opp, me)]

def part1(matches):
    tot = 0
    for opp, me in matches:
        tot += score_round(opp, me)

    print(tot)

def part2(matches):
    tot = 0
    for opp, result in matches:
        tot += score_round_result(opp, result)

    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
