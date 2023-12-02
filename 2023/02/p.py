#!/usr/bin/env pypy3

import math
import sys

def parse_input():
    # Game 1: 7 blue, 6 green, 3 red; 3 red, 5 green, 1 blue; 1 red, 5 green, 8 blue; 3 red, 1 green, 5 blue
    lines = [_.strip('\r\n') for _ in sys.stdin]
    games = {}
    for line in lines:
        id, draws = line.split(': ')
        id = int(id.split()[1])
        games[id] = []
        for d in draws.split('; '):
            draw = {}
            games[id].append(draw)
            for x in d.split(', '):
                cnt, color = x.strip().split()
                draw[color] = int(cnt)

    return games

def part1(games):
    avail = {'red': 12, 'green': 13, 'blue': 14}
    tot = 0
    for id, game in games.items():
        if all(all(draw[_] <= avail[_] for _ in draw) for draw in game):
            tot += id
    print(tot)
            
def part2(games):
    colors = ('red', 'green', 'blue')
    tot = 0
    for game in games.values():
        tot += math.prod(max(_.get(color, 0) for _ in game) for color in colors)
    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
