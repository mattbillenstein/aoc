#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines

def part1(data):
    scores = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }
    push = {'(': ')', '[': ']', '<': '>', '{': '}'}

    corrupted = []

    score = 0
    for line in data:
        stack = []
        for i, c in enumerate(line):
            if c in push:
                stack.append(push[c])
            else:
                x = stack.pop()
                if c != x:
                    score += scores[c]
#                    print(line)
#                    print(f'Corrupted got {x} expected {c} position {i+1}')
#                    print()
                    corrupted.append(line)
                    break

    print(score)

    return corrupted

def part2(data):
    char_scores = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }
    push = {'(': ')', '[': ']', '<': '>', '{': '}'}

    scores = []
    for line in data:
        score = 0
        stack = []
        for i, c in enumerate(line):
            if c in push:
                stack.append(push[c])
            else:
                x = stack.pop()
                assert c == x, (c, x)

        completion = ''.join(reversed(stack))
        for c in completion:
            score *= 5
            score += char_scores[c]

        scores.append(score)

    scores.sort()
    print(scores[len(scores)//2])

def main():
    data = parse_input()

    corrupted = part1(data)

    data = [_ for _ in data if _ not in corrupted]

    part2(data)

if __name__ == '__main__':
    main()
