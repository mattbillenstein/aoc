#!/usr/bin/env pypy3

import copy
import sys
from pprint import pprint

from graph import dfs

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    d = {}
    for line in lines:
        a, b = line.split(': ')
        if a == 'Hit Points':
            a = 'hp'
        a = a.lower()
        d[a] = int(b)

    spells = []
    for line in open('spells.txt'):
        line = line.strip()
        if not line:
            continue

        if line.startswith('-'):
            continue

        name, cost, dmg, armor, hp, turns, mana = [int(_) if _.isdigit() else _ for _ in line.split()]
        spells.append({
            'name': name,
            'cost': cost,
            'damage': dmg,
            'armor': armor,
            'hp': hp,
            'turns': turns,
            'mana': mana,
        })

    return d, spells

class BadState(Exception):
    pass

class State:
    def __init__(self, player, boss, spells, spell=None):
        self.player = copy.deepcopy(player)
        self.boss = copy.deepcopy(boss)
        self.spells = spells

        if spell:
            if DEBUG > 2:
                print('Fight')
                print(spell)
                print(self.player)
                print(self.boss)

            self.do_effects()
            if self.boss['hp'] <= 0:
                return

            # player casts
            if self.player['mana'] < spell['cost']:
                raise BadState()

            # cast
            self.player['mana'] -= spell['cost']
            self.player['mana_used'] += spell['cost']
            if spell['turns']:
                if spell['name'] in self.player['effects']:
                    raise BadState()
                self.player['effects'][spell['name']] = spell = copy.deepcopy(spell)
            else:
                self.boss['hp'] -= spell['damage']
                self.player['hp'] += spell['hp']

            if self.boss['hp'] > 0:
                # boss fights
                self.do_effects()
                if self.boss['hp'] <= 0:
                    return

                self.player['hp'] -= max(1, self.boss['damage'] - self.player['armor'])

                if self.player['hp'] <= 0:
                    raise BadState('Player Died')

            if DEBUG > 2:
                print(self.player)
                print(self.boss)
                print('End Fight')
                print()

    def do_effects(self):
        self.player['armor'] = 0

        remove = []
        for k, e in self.player['effects'].items():
            self.boss['hp'] -= e['damage']

            self.player['armor'] += e['armor']
            self.player['mana'] += e['mana']
            self.player['hp'] += e['hp']

            e['turns'] -= 1
            if e['turns'] <= 0:
                remove.append(k)

        # remove expired effects
        for k in remove:
            del self.player['effects'][k]

    @property
    def done(self):
        # if we're done
        return self.player['hp'] > 0 and self.boss['hp'] <= 0

    @property
    def key(self):
        # the key into the visited dict
        return ''

    @property
    def cost(self):
        # cost, lower is better
        return self.player['mana_used']

    def next(self):
        # next states
        for spell in self.spells:
            try:
                yield self.__class__(self.player, self.boss, self.spells, spell)
            except BadState:
                if DEBUG > 2:
                    print('Bad')
                    print()
                pass

    def __repr__(self):
        return f'State({self.player}, {self.boss}, {self.cost})'

def part(boss, spells):
    player = {
        'hp': 50,
        'mana': 500,
        'armor': 0,
        'mana_used': 0,
        'effects': {},
    }
    if boss['hp'] < 50:
        # test
        player.update({'hp': 10, 'mana': 250})

    if DEBUG:
        print(player)
        print(boss)
        pprint(spells)

    state = State(player, boss, spells)
    print(state)

    best = dfs(state)
    print(best)

def main():
    data = parse_input()
    part(*data)

if __name__ == '__main__':
    main()
