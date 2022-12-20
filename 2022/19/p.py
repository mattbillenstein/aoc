#!/usr/bin/env pypy3

import json
import re
import sys
import time
from collections import defaultdict
from multiprocessing import Pool
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

def can_make_robot(type, resources, blueprint):
    return all(resources[k] >= v for k, v in blueprint[type].items())

def make_robot(type, robots, resources, blueprint):
    robots[type] += 1
    for k, v in blueprint[type].items():
        resources[k] -= v

def simulate(minutes, robots, resources, blueprint):
    # dfs
    robots = dict(robots)
    resources = dict(resources)

    print(json.dumps(blueprint, indent=4))

    best = 0

    # since we can only produce one robot per turn, we can limit the number of
    # robots of each type based on the maximum required in a single turn...
    limit = {
        'ore': max(blueprint[_].get('ore', 0) for _ in robots),
        'clay': max(blueprint[_].get('clay', 0) for _ in robots),
        'obsidian': max(blueprint[_].get('obsidian', 0) for _ in robots),
        'geode': 999,
    }

    print('Limit:', limit)

    stack = []
    stack.append((1, dict(robots), dict(resources), []))

    debug = 0

    while stack:
        minute, robots, resources, made = stack.pop()

#        # sloppy
#        if minute >= 18 and robots['obsidian'] == 0:
#            continue

        # abort if we can't make more geode than current best
        T = minutes - minute
        possible = resources['geode'] + robots['geode'] * T + T*(T+1)//2
        if possible < best:
            if debug:
                print(minute, possible, best)
                print(robots)
                print(resources)
                print()
            continue

        if debug:
            print()
            print(
                minute,
                ','.join(':'.join((k, str(v))) for k, v in robots.items()),
                ','.join(':'.join((k, str(v))) for k, v in resources.items()),
            )

        if minute < minutes:
            # can only make one robot per round - we have one machine...
            for type in ('geode', 'obsidian', 'clay', 'ore'):
                number = robots[type]
                if number < limit[type]:
                    if can_make_robot(type, resources, blueprint):
                        # push making this robot
                        new_robots = dict(robots)

                        new_resources = dict(resources)
                        for resource, amt in robots.items():
                            new_resources[resource] += amt

                        make_robot(type, new_robots, new_resources, blueprint)

                        new_made = list(made)
                        new_made.append((minute, type))

                        stack.append((minute+1, new_robots, new_resources, new_made))

                        if debug:
                            print(f'Make {type} at {minute} {blueprint[type]}')
                        if debug:
                            print(f'Push {stack[-1]}')

            assert all(resources[_] >= 0 for _ in resources)


        # now actually collect resources
        for resource, amt in robots.items():
            resources[resource] += amt

        # check best
        if minute >= minutes:
            if resources['geode'] > best:
                best = resources['geode']
                print(
                    f'Best:{best}',
                    f'Minute:{minute}',
                    f'Blueprint:{blueprint["id"]}',
                )
                print('Robots:', ' '.join(':'.join((k, str(v))) for k, v in robots.items()))
                print('Resources:', ' '.join(':'.join((k, str(v))) for k, v in resources.items()))
                print('Made:', ' '.join(':'.join((str(a), b)) for a, b in made))
                print()
            continue

        # we didn't make anything, just collected
        stack.append((minute+1, dict(robots), dict(resources), made))
        if debug:
            print(f'Push {stack[-1]}')

    return (blueprint['id'], best)

def part1(blueprints):
    minutes = 24

    robots = {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}
    resources = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}

    # debug
#    blueprints = blueprints[:1]

    start = time.time()
    sum_quality = 0

    if '-m' in sys.argv:
        results = []
        with Pool(processes=8) as pool:
            for b in blueprints:
                res = pool.apply_async(simulate, (minutes, robots, resources, b))
                results.append(res)

            L = []
            for res in results:
                L.append(res.get())

            for bid, geodes in L:
                quality = bid * geodes
                print('RESULT', bid, geodes, quality, time.time() - start)
                sum_quality += quality
    else:
        for b in blueprints:
            bid, geodes = simulate(minutes, robots, resources, b)
            quality = bid * geodes
            print('RESULT', bid, geodes, quality, time.time() - start)
            sum_quality += quality

    print(sum_quality)

def main(argv):
    data = parse_input()

    part1(data)

if __name__ == '__main__':
    main(sys.argv)
