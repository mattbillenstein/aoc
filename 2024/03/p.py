#!/usr/bin/env pypy3

import re
import sys

def parse_input():
    return sys.stdin.read().strip()

def mul(data):
    tot = 0
    for x in re.findall('mul\(([0-9]{1,3}),([0-9]{1,3})\)', data):
        tot += int(x[0]) * int(x[1])
    return tot

def part1(data):
    print(mul(data))

def part2(data):
    # remove don't -> do() stretches and compute
    DONT = "don't()"
    DO = "do()"
    while 1:
        dont = data.find(DONT)
        if dont != -1:
            do = data.find(DO, dont)
            if do != -1:
                # remove dont to next do
                data = data[:dont] + data[do+len(DO):]
            else:
                # keep data up to dont
                data = data[:dont]
        else:
            # if don't not found, we're done
            break
    
    print(mul(data))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
