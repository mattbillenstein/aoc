#!/usr/bin/env pypy3

import itertools
import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    cmds = []
    for line in lines:
        cmd, *rest = line.split()
        for i in range(len(rest)):
            try:
                rest[i] = int(rest[i])
            except ValueError:
                pass

        if cmd == 'reverse':
            cmds.append((cmd, (rest[1], rest[3])))
        elif cmd in ('move', 'swap'):
            cmds.append((cmd, (rest[1], rest[4])))
        elif cmd == 'rotate':
            if rest[0] == 'based':
                cmds.append((cmd, (rest[2], rest[5])))
            else:
                cmds.append((cmd, (rest[0], rest[1])))
        else:
            assert 0
    return cmds

def scramble(s, cmds):
    for cmd, opts in cmds:
        if cmd == 'rotate':
            if opts[0] == 'position':
                idx = s.index(opts[1])
                if idx >= 4:
                    idx += 1
                idx += 1
                for i in range(idx):
                    s = s[-1] + s[:-1]
            else:
                idx = opts[1]
                if opts[0] == 'left':
                    for i in range(idx):
                        s = s[1:] + s[0]
                else:
                    for i in range(idx):
                        s = s[-1] + s[:-1]
        elif cmd == 'move':
            a, b = opts
            s = list(s)
            c = s.pop(a)
            s.insert(b, c)
            s = ''.join(s)
        elif cmd == 'swap':
            a, b = opts
            s = list(s)
            if isinstance(a, str):
                a = s.index(a)
                b = s.index(b)
            s[b], s[a] = s[a], s[b]
            s = ''.join(s)
        elif cmd == 'reverse':
            a, b = opts
            s = list(s)
            s[a:b+1] = reversed(s[a:b+1])
            s = ''.join(s)
        else:
            assert 0, (cmd, opts)

        debug(cmd, opts, s)

    return s

def part1(cmds):
    print(scramble('abcdefgh', cmds))

def part2(cmds):
    # try permutations until we find the scrambled output
    expected = 'fbgdceah'
    for s in itertools.permutations(expected, len(expected)):
        s = ''.join(s)
        out = scramble(s, cmds)
        if out == expected:
            print(s)
            break

def main():
    data = parse_input()
    if 'test' in sys.argv:
        print(scramble('abcde', data))
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
