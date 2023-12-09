#!/usr/bin/env pypy3

import sys

DEBUG = sys.argv.count('-v')

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return [[int(_) for _ in line.split()] for line in lines]

def parts(data):
    tot = 0
    for i in range(len(data)):
        # list of lists
        data[i] = L = [data[i]]

        # build difference lists down
        while 1:
            a = L[-1]
            if all(_ == 0 for _ in a):
                break
            b = [a[i+1] - a[i] for i in range(0, len(a)-1)]
            L.append(b)

        # fill up right side
        a = L[-1]
        a.append(0)
        for b in L[-2::-1]:
            b.append(b[-1] + a[-1])
            a = b

        tot += L[0][-1]

        if DEBUG:
            print()
            print(L[0][-1])
            for item in L:
                print(item)

    print(tot)

    tot = 0
    for L in data:
        # fill up left side
        a = L[-1]
        a.insert(0, 0)
        for b in L[-2::-1]:
            b.insert(0, b[0] - a[0])
            a = b

        tot += L[0][0]

        if DEBUG:
            print()
            print(L[0][0])
            for item in L:
                print(item)

    print(tot)

def main():
    data = parse_input()
    parts(data)

if __name__ == '__main__':
    main()
