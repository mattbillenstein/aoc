#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return [int(_.split()[-1]) for _ in lines]

def part1(data):
    A = data[0]
    B = data[1]
    Af = 16807
    Bf = 48271
    mod = 2147483647
    cnt = 0
    for i in range(40_000_000):
        A = (A * Af) % mod
        B = (B * Bf) % mod
        if A & 0xffff == B & 0xffff:
            cnt += 1

    print(cnt)

def part2(data):
    A = data[0]
    B = data[1]
    Af = 16807
    Bf = 48271
    mod = 2147483647

    def gA():
        A = data[0]
        while 1:
            A = (A * Af) % mod
            if A % 4 == 0:
                yield A
    gA = gA()
        
    def gB():
        B = data[1]
        while 1:
            B = (B * Bf) % mod
            if B % 8 == 0:
                yield B
    gB = gB()

    cnt = 0
    for i in range(5_000_000):
        A = next(gA)
        B = next(gB)
        if A & 0xffff == B & 0xffff:
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
