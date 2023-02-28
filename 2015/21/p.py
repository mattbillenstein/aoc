#!/usr/bin/env pypy3

import copy
import sys
from pprint import pprint

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    d = {}
    for line in lines:
        a, b = line.split(': ')
        d[a] = int(b)

    items = {}
    for line in open('items.txt'):
        line = line.strip()
        if not line:
            continue

        if ':' in line:
            type = line.split(':')[0]
            items[type] = []
        else:
            line = line.replace(' +', '_+')
            name, cost, dmg, armor = [int(_) if _.isdigit() else _ for _ in line.split()]
            items[type].append({'name': name, 'cost': cost, 'damage': dmg, 'armor': armor})

    return d, items

def fight(player, boss):
    player = copy.deepcopy(player)
    boss = copy.deepcopy(boss)
    while 1:
        debug('Player:', player)
        debug('Boss:  ', boss)

        boss['Hit Points'] -= max(1, player['Damage'] - boss['Armor'])
        if boss['Hit Points'] <= 0:
            return 'player'

        player['Hit Points'] -= max(1, boss['Damage'] - player['Armor'])
        if player['Hit Points'] <= 0:
            return 'boss'

def part(boss, items):
    player = {
        'Hit Points': 100,
        'Damage': 0,
        'Armor': 0,
    }

    if DEBUG:
        print(boss)
        pprint(items)

    # minimize spent
    best = sys.maxsize
    worst = 0
    for weapon in items['Weapons']:
        for armor in items['Armor'] + [None]:
            for ring1 in items['Rings'] + [None]:
                for ring2 in items['Rings'] + [None]:
                    if ring1 and ring2 and ring1 is ring2:
                        continue

                    stuff = [weapon, armor, ring1, ring2]
                    player['Armor'] = sum(_['armor'] for _ in stuff if _)
                    player['Damage'] = sum(_['damage'] for _ in stuff if _)
                    spent = sum(_['cost'] for _ in stuff if _)

                    winner = fight(player, boss)
                    debug(spent, winner, weapon, armor, ring1, ring2)

                    if winner == 'player':
                        if spent < best:
                            best = spent
                    else:
                        if spent > worst:
                            worst = spent

    print(best)
    print(worst)

def main():
    data = parse_input()
    part(*data)

if __name__ == '__main__':
    main()
