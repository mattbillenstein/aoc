#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines

def part(data):
    code = 0
    literal = 0
    rpr = 0
    for line in data:
        code += len(line)
        literal += len(eval(line))

        r = ""
        for c in line:
            if c == '\\':
                r += '\\\\'
            elif c == '"':
                r += '\\"'
            else:
                r += c
            
        rpr += len(r) + 2

    print(code - literal)
    print(rpr - code)

def main():
    data = parse_input()
    part(data)

if __name__ == '__main__':
    main()
