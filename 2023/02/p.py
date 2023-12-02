#!/usr/bin/env pypy3

import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    games = {}
    for line in lines:
        game_id, draws = line.split(':', 1)
        game_id = int(game_id.split()[1])
        games[game_id] = []
        draws = draws.strip().split(';')
        for d in draws:
            cubes = d.strip().split(';')
            for x in cubes:
                draw = {}
                games[game_id].append(draw)
                for y in x.strip().split(','):
                    cnt, color = y.strip().split()
                    draw[color] = int(cnt)

    return games

def part1(games):
    available = {'red': 12, 'green': 13, 'blue': 14}

    tot = 0
    for id, game in games.items():
        poss = True
        for draw in game:
            if any(draw[_] > available[_] for _ in draw):
                poss = False
                break

        if poss:
            tot += id

    print(tot)
            
def part2(games):
    tot = 0
    for id, game in games.items():
        mins = {'red': 0, 'green': 0, 'blue': 0}
        for draw in game:
            for color, cnt in draw.items():
                if mins[color] < cnt:
                    mins[color] = cnt

        tot += mins['red'] * mins['green'] * mins['blue']

    print(tot)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
