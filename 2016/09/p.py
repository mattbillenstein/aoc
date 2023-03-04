#!/usr/bin/env pypy3

import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines[0]

def part1(line):
    debug(line)
    pos = 0
    while 1:
        i = line.find('(', pos)
        if i == -1:
            break
        j = line.index(')', i)
        a, b = line[i+1:j].split('x')
        a = int(a)
        b = int(b)
        s = line[j+1:j+1+a]
        line = line[:i] + (s * b) + line[j+1+a:]
        pos = i + len(s) * b

    debug(line)
    print(len(line))

def part2(line):
    L = [(line, 1)]

    cnt = 0
    debug(line)
    while L:
        line, repeat = L.pop()
        i = line.find('(')
        if i == -1:
            cnt += len(line) * repeat
            continue

        cnt += i * repeat

        j = line.index(')', i)
        a, b = line[i+1:j].split('x')
        a = int(a)
        L.append((line[j+1+a:], repeat))

        b = int(b)
        s = line[j+1:j+1+a]
        if s:
            L.append((s, b * repeat))

    print(cnt)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
