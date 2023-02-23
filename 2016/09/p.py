#!/usr/bin/env pypy3

import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines

def part1(data):
    for line in data:
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

def part2(data):
    for line in data:
        cnt = 0
        debug(line)
        while 1:
            i = line.find('(')
            if i == -1:
                cnt += len(line)
                break
            cnt += i

            j = line.index(')', i)
            a, b = line[i+1:j].split('x')
            a = int(a)
            b = int(b)
            s = line[j+1:j+1+a]
            line = (s * b) + line[j+1+a:]

        print(cnt)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
