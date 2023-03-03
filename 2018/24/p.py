#!/usr/bin/env pypy3

import copy
import re
import sys
from pprint import pprint

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    teams = []
    for line in lines:
        if line.endswith(':'):
            team = {
                'id': len(teams) + 1,
                'name': line.strip(':'),
                'groups': [],
            }
            teams.append(team)
        elif 'unit' in line:
            group = {
                'id': len(team['groups']) + 1,
                'team_id': team['id'],
                'weak': [],
                'immune': [],
            }
            team['groups'].append(group)
            group['key'] = f'{team["name"]} {group["id"]}'

            idx = line.find('(')
            if idx > -1:
                idx2 = line.find(')')
                x = line[idx+1:idx2].replace(',', '')
                line = line[:idx-1] + line[idx2+1:]
                for y in x.split(';'):
                    tup = y.strip().split()
                    group[tup[0]] = tup[2:]

            mobj = re.match('^([0-9]+) units each with ([0-9]+) hit points with an attack that does ([0-9]+) ([a-z]+) damage at initiative ([0-9]+)$', line)
            assert mobj, line

            tup = mobj.groups()
            group['units'] = int(tup[0])
            group['hp'] = int(tup[1])
            group['ad'] = int(tup[2])
            group['at'] = tup[3]
            group['ini'] = int(tup[4])

    return teams

def ep(group):
    # effective power, units * attack damage
    return group['units'] * group['ad']

def attack_priority(group):
    # effective power, initiative desc
    return (ep(group), group['ini'])

def attack_damage(group, target):
    at = group['at']
    ad = ep(group)
    if at in target['immune']:
        ad = 0
    elif at in target['weak']:
        ad *= 2
    return ad

def defend_priority(group, target):
    # attack damage, target effective power, initiative desc
    ad = attack_damage(group, target)
    return (ad, ep(target), target['ini'])

def target_selection(groups):
    d = {}
    groups.sort(key=lambda x: attack_priority(x), reverse=True)

    for group in groups:
        targets = [_ for _ in groups if _['team_id'] != group['team_id']]
        targets.sort(key=lambda x: defend_priority(group, x), reverse=True)
        for target in targets:
            ad = attack_damage(group, target)
            if ad > 0 and target['key'] not in d.values():
                d[group['key']] = target['key']
                break

    return d

def sim(teams):
    i = 0
    while all(sum(_['units'] for _ in t['groups']) for t in teams):
        if i > 10000:
            return False
        i += 1

        groups = teams[0]['groups'] + teams[1]['groups']
        groups = [_ for _ in groups if _['units'] > 0]
        targets = target_selection(groups)

        groups.sort(key=lambda x: x['ini'], reverse=True)

        for group in groups:
            if group['key'] in targets:
                target = [_ for _ in groups if _['key'] == targets[group['key']]][0]
                ad = attack_damage(group, target)
                killed = min(ad // target['hp'], target['units'])
                debug(group['key'], 'attacks', target['key'], 'killed', killed, ad, target['hp'])
                target['units'] -= killed

    return True

def part1(teams):
    if DEBUG:
        pprint(teams)

    sim(teams)

    units = sum(_['units'] for _ in teams[0]['groups'] + teams[1]['groups'])
    print(units)
    
def part2(teams):
    boost = 0
    while 1:
        boost += 1
        x = copy.deepcopy(teams)
        for g in x[0]['groups']:
            g['ad'] += boost

        # boost 58 never terminates because the attacker doesn't have enough hp
        # to kill the last defender...
        finished = sim(x)
        if not finished:
            continue

        if sum(_['units'] for _ in x[0]['groups']):
            break

    print(boost)
    units = sum(_['units'] for _ in x[0]['groups'])
    print(units)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(copy.deepcopy(data))
    if '2' in sys.argv:
        part2(copy.deepcopy(data))

if __name__ == '__main__':
    main()
