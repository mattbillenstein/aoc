#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    data = {}
    for line in lines:
        name, op = line.split(': ')
        op = op.split()
        if len(op) == 1:
            op = int(op[0])
        data[name] = op
    return data

def resolve(name, data):
    v = data[name]
    if isinstance(v, int):
        return v

    n1, op, n2 = v
    v1 = resolve(n1, data)
    v2 = resolve(n2, data)
    if op == '+':
        return v1 + v2
    if op == '*':
        return v1 * v2
    if op == '-':
        return v1 - v2
    if op == '/':
        return v1 // v2
    if op == '=':
        return v1 == v2

def func(name, data):
    v = data[name]
    if v == 'humn':
        return v

    if isinstance(v, int):
        return v

    n1, op, n2 = v
    v1 = func(n1, data)
    v2 = func(n2, data)
    
    if not isinstance(v1, (tuple, str)) and not isinstance(v2, (tuple, str)):
        if op == '+':
            return v1 + v2
        if op == '*':
            return v1 * v2
        if op == '-':
            return v1 - v2
        if op == '/':
            assert v1 % v2 == 0
            return v1 // v2
        if op == '=':
            return v1 == v2

    return (v1, op, v2)

def solve(a, b):
    while a != 'humn':
#        print('solve', a, b)
        v1, op, v2 = a
        v1i = isinstance(v1, int)

        if op == '/':
            if v1i:
                b = v1 / b
            else:
                b *= v2
        elif op == '*':
            if v1i:
                assert b % v1 == 0
                b //= v1
            else:
                assert b % v2 == 0
                b //= v2
        elif op == '+':
            if v1i:
                b -= v1
            else:
                b -= v2
        elif op == '-':
            if v1i:
                b = v1 - b
            else:
                b += v2

        if v1i:
            a = v2
        else:
            a = v1
    return b

def part1(data):
    x = resolve('root', data)
    print(x)

def part2(data):
    data['root'][1] = '=='
    data['humn'] = 'humn'

    a = func(data['root'][0], data)
    b = func(data['root'][2], data)

    value = solve(a, b)
    print(value)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
