#!/usr/bin/env pypy3

import hashlib
import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines[0]

def get_doors(data, path):
    b = (data + ''.join(path)).encode('utf8')
    s = hashlib.md5(b).hexdigest()[:4]
    d = {}
    for dir, c in zip('UDLR', s):
        d[dir] = 'closed'
        if c in 'bcdef':
            d[dir] = 'open'
    return d

def move(pt, path, neighbors, best, longest=False):
    if not longest and len(path) > len(best[0]):
        return

    if pt == (3, 3):
        if longest:
            if len(path) > len(best[0]):
                best[0] = ''.join(path)
                debug('Best:', best[0])
        elif len(path) < len(best[0]):
            best[0] = ''.join(path)
            debug('Best:', best[0])

        return

    for dir, npt in neighbors(pt, path):
        move(npt, path + [dir], neighbors, best, longest)

def part1(data, longest=False):
    def neighbors(pt, path):
        x, y = pt
        maxx = maxy = 3
        doors = get_doors(data, path)
        for d, state in doors.items():
            if state == 'open':
                if d == 'U' and y > 0:
                    yield d, (x, y-1)
                elif d == 'D' and y < maxy:
                    yield d, (x, y+1)
                elif d == 'L' and x > 0:
                    yield d, (x-1, y)
                elif d == 'R' and x < maxx:
                    yield d, (x+1, y)

    best = [[]] if longest else [[None] * 100] 
    move((0, 0), [], neighbors, best, longest)

    path = best[0]

    if longest:
        print(len(path))
    else:
        debug(len(path))
        print(path)

    return path

def part2(data):
    part1(data, True)

def main():
    data = parse_input()
    if 'test' in sys.argv:
        data = 'ulqzkmiv'
        s = part1(data)
        assert s == 'DRURDRUDDLLDLUURRDULRLDUUDDDRR'
        n = part1(data, True)
        assert n == 830

    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
