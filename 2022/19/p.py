#!/usr/bin/env pypy3

import re
import sys
import time
from collections import defaultdict
from pprint import pprint

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]

    blueprints = []
    for line in lines:
        mobj = re.match('^Blueprint (\d+): Each (ore) robot costs (\d+) (ore). Each (clay) robot costs (\d+) (ore). Each (obsidian) robot costs (\d+) (ore) and (\d+) (clay). Each (geode) robot costs (\d+) (ore) and (\d+) (obsidian).$', line)
        g = mobj.groups()
        blueprint = {
            'id': int(g[0]),
            g[ 1]: {g[ 3]: int(g[ 2])},
            g[ 4]: {g[ 6]: int(g[ 5])},
            g[ 7]: {g[ 9]: int(g[ 8]), g[11]: int(g[10])},
            g[12]: {g[14]: int(g[13]), g[16]: int(g[15])},
        }
        blueprints.append(blueprint)
    return blueprints

last = time.time()
def simulate(minutes_left, robots, resources, blueprint):
    global last

    if minutes_left <= 1:
        if time.time() - last > 10:
            print(' ' * (24-minutes_left), 'sim', minutes_left, 
                ','.join(':'.join((k, str(v))) for k, v in robots.items()),
                ','.join(':'.join((k, str(v))) for k, v in resources.items()),
            )
            last = time.time()
        return resources['geode']

    # build new robots
    can_build = {}
    for k, d in blueprint.items():
        if k == 'id':
            continue
        
        num = min(resources[resource] // amt for resource, amt in d.items())
        can_build[k] = num

#    pprint(blueprint)
#    print(can_build)

    # collect resources
    for resource, amt in robots.items():
        resources[resource] += amt

    # need to maintain within the loop, this can be deleted...
    robots = robots
    resources = resources

    best = resources['geode']
    for ore in range(0, can_build['ore']+1):

        robots['ore'] += ore
        resources['ore'] -= blueprint['ore']['ore'] * ore

        for clay in range(0, can_build['clay']+1):
            if resources['ore'] < blueprint['clay']['ore'] * clay:
                continue

            robots['clay'] += clay
            resources['ore'] -= blueprint['clay']['ore'] * clay

            for obsidian in range(0, can_build['obsidian']+1):
                if resources['ore'] < blueprint['obsidian']['ore'] * obsidian:
                    continue
                if resources['clay'] < blueprint['obsidian']['clay'] * obsidian:
                    continue

                robots['obsidian'] += obsidian
                resources['ore'] -= blueprint['obsidian']['ore'] * obsidian
                resources['clay'] -= blueprint['obsidian']['clay'] * obsidian

                for geode in range(0, can_build['geode']+1):
                    if resources['ore'] < blueprint['geode']['ore'] * geode:
                        continue
                    if resources['obsidian'] < blueprint['geode']['obsidian'] * geode:
                        continue

                    robots['geode'] += geode
                    resources['ore'] -= blueprint['geode']['ore'] * geode
                    resources['obsidian'] -= blueprint['geode']['obsidian'] * geode

#                    print('ore', ore)
#                    print('clay', clay)
#                    print('obsidian', obsidian)
#                    print('geode', geode)
#                    print('sim', minutes_left-1, robots, resources)
#                    print()
                    # take a copy here, we mutate inside this function of course...
                    sim_geode = simulate(minutes_left-1, dict(robots), dict(resources), blueprint)
                    if sim_geode > best:
                        best = sim_geode

                    robots['geode'] -= geode
                    resources['ore'] += blueprint['geode']['ore'] * geode
                    resources['obsidian'] += blueprint['geode']['obsidian'] * geode
                robots['obsidian'] -= obsidian
                resources['ore'] += blueprint['obsidian']['ore'] * obsidian
                resources['clay'] += blueprint['obsidian']['clay'] * obsidian
            robots['clay'] -= clay
            resources['ore'] += blueprint['clay']['ore'] * clay
        robots['ore'] -= ore
        resources['ore'] += blueprint['ore']['ore'] * ore

    return best


def part1(blueprints):
#    pprint(blueprints)

    minutes = 24
    robots = {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}
    resources = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}

#    resources = {'ore': 4, 'clay': 0, 'obsidian': 0, 'geode': 0}
    x = simulate(minutes, robots, resources, blueprints[0])
    print(x)
    duh


    geodes = {}
    for b in blueprints:
        geodes[b['id']] = simulate(minutes, robots, resources, b)

    print(geodes)

def main(argv):
    data = parse_input()
    pprint(data)

    part1(data)

if __name__ == '__main__':
    main(sys.argv)
