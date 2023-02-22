#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines

def abba(s):
    matches = False
    in_brackets = False
    for i in range(len(s)-3):
        if s[i] == '[':
            in_brackets = True
            continue
        if s[i] == ']':
            in_brackets = False
            continue

        if s[i] != s[i+1] and s[i:i+2] == s[i+3:i+1:-1]:
            if in_brackets:
                return False
            matches = True
    return matches

def part1(data):
    cnt = 0
    for line in data:
        if abba(line):
            cnt += 1
    print(cnt)

def aba(s):
    inside = set()
    outside = set()
    in_brackets = False
    for i in range(len(s)-2):
        if s[i] == '[':
            in_brackets = True
        if s[i] == ']':
            in_brackets = False

        if s[i] != s[i+1] and s[i] == s[i+2] and not '[' in s[i:i+3] and not ']' in s[i:i+3]:
            if in_brackets:
                inside.add(s[i:i+3])
            else:
                outside.add(s[i:i+3])

    for s in inside:
        t = s[1] + s[0] + s[1]
        if t in outside:
            return True

    return False
    
def part2(data):
    cnt = 0
    for line in data:
        if aba(line):
            cnt += 1
    print(cnt)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
