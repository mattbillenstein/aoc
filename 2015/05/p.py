#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines

def part1(data):
    cnt = 0
    for word in data:
        vowels = bad = double = 0
        for i in range(len(word)-1):
            if word[i] in 'aeiou':
                vowels += 1
            if word[i] == word[i+1]:
                double += 1
            if word[i:i+2] in ('ab', 'cd', 'pq', 'xy'):
                bad += 1

        if word[-1] in 'aeiou':
            vowels += 1

        if bad == 0 and vowels >= 3 and double > 0:
            cnt += 1

    print(cnt)

def part2(data):
    cnt = 0
    for word in data:
        repeats = pairs = 0
        for i in range(len(word)-2):
            if word[i] == word[i+2]:
                repeats += 1
                
        for i in range(len(word)-1):
            for j in range(i+2, len(word)-1):
                if word[i:i+2] == word[j:j+2] and abs(i-j) >= 2:
                    pairs += 1
                

        if repeats and pairs:
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
