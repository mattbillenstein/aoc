#!/usr/bin/env pypy3

import copy
import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    deer = []
    for line in lines:
        L = line.split()
        deer.append({
            'name': L[0],
            'speed': int(L[3]),
            'fly_time': int(L[6]),
            'rest_time': int(L[13]),
        })
    return deer

def part1(deer):
    tot_time = 2503

    for d in deer:
        dist = 0
        t = 0
        state = 'fly'
        while t <= tot_time:
            if state == 'fly':
                dist += d['speed'] * d['fly_time']
                state = 'rest'
                t += d['fly_time']
            else:
                state = 'fly'
                t += d['rest_time']

        if state == 'rest':
            # deduct time over total time
            dist -= d['speed'] * (t - tot_time)
            
        d['distance'] = dist

    if DEBUG:
        for d in deer:
            print(d)

    print(max(_['distance'] for _ in deer))

class Deer:
    def __init__(self, d):
        self.d = d
        self.dist = 0
        self.state = 'fly'
        self.t = d['fly_time']
        self.score = 0

    def step(self):
        self.t -= 1
        if self.state == 'fly':
            self.dist += self.d['speed']
            if self.t == 0:
                self.state = 'rest'
                self.t = self.d['rest_time']
        else:
            if self.t == 0:
                self.state = 'fly'
                self.t = self.d['fly_time']

    def __repr__(self):
        return f'Deer({self.d["name"]}, {self.dist}, {self.score})'
def part2(deer):
    deer = [Deer(_) for _ in deer]
    for t in range(2503):
        for d in deer:
            d.step()

        best = max(_.dist for _ in deer)
        for d in deer:
            if d.dist == best:
                d.score += 1

        if DEBUG:
            print(t)
            for d in deer:
                print(d)

    print(max(_.score for _ in deer))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(copy.deepcopy(data))
    if '2' in sys.argv:
        part2(copy.deepcopy(data))

if __name__ == '__main__':
    main()
