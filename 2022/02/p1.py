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

def score_round(opp, me):
    opp = opp_code[opp]
    me = me_code[me]
    return thing_score[me] + opp_me_score[(opp, me)]
    
def score_round_result(opp, result):
    opp = opp_code[opp]
    me = opp_result_play[(opp, result)]
    return thing_score[me] + opp_me_score[(opp, me)]

def p1(argv):
    tot = 0
    with open(argv[1]) as f:
        for line in f:
            opp, me = line.strip().split()
            tot += score_round(opp, me)

    print(tot)

def p2(argv):
    tot = 0
    with open(argv[1]) as f:
        for line in f:
            opp, result = line.strip().split()
            tot += score_round_result(opp, result)

    print(tot)

def main(argv):
    p1(argv)
    p2(argv)
if __name__ == '__main__':
    main(sys.argv)
