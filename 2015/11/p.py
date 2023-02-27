#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines[0]

def nxt(s):
    chars = 'abcdefghjkmnpqrstuvwxyz'
    d = {}
    for i in range(len(chars)-1):
        d[chars[i]] = chars[i+1]
        
    L = list(reversed(s))

    while 1:
        i = 0
        while 1:
            if L[i] == 'z':
                L[i] = 'a'
            else:
                L[i] = d[L[i]]
                break
            i += 1

        yield ''.join(reversed(L))

def check(s):
    for c in ('i', 'o', 'l'):
        if c in s:
            return False

    chars = 'abcdefghijklmnopqrstuvwxyz'
    found = False
    for i in range(len(chars)-2):
        if chars[i:i+3] in s:
            found = True
            break

    if not found:
        return False

    pairs = 0
    for c in chars:
        if c * 2 in s:
            pairs += 1

    return pairs >= 2

def part(pw):
    cnt = 0
    for s in nxt(pw):
        if check(s):
            print(s)
            cnt += 1
        if cnt > 1:
            break

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
