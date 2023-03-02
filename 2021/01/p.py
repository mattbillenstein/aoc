#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return [int(_) for _ in lines]

def num_increased(data):
    cnt = 0
    for i in range(1, len(data)):
        if data[i] > data[i-1]:
            cnt += 1
    return cnt

def part(data):
    print(num_increased(data))

    sums = []
    for i in range(2, len(data)):
        sums.append(sum(data[i-2:i+1]))

    print(num_increased(sums))

def main(argv):
    data = parse_input()

    part(data)

if __name__ == '__main__':
    main(sys.argv)
