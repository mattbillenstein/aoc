#!/usr/bin/env pypy3

import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    regs = {}
    for line in lines:
        line=line.replace(':', '')
        if line.startswith('Register'):
            _, reg, val = line.split()
            regs[reg] = int(val)
        elif line.startswith('Program'):
            prog = line.split()[1].split(',')
            prog = [int(_) for _ in prog]
    return (prog, regs)

def run(prog, regs):
    debug(prog, regs)
    ip = 0

    output = []

    def combo(op):
        if op in (0, 1, 2, 3):
            return op
        if op == 4:
            return regs['A']
        if op == 5:
            return regs['B']
        if op == 6:
            return regs['C']
        assert 0, op

    while ip < len(prog):
        instr = prog[ip]
        ip += 1
        op = prog[ip]
        ip += 1
        debug(instr, op, regs)
        if instr == 0:    # adv
            regs['A'] = regs['A'] // 2**combo(op)
        elif instr == 1:  # bxl
            regs['B'] = regs['B'] ^ op
        elif instr == 2:  # bst
            regs['B'] = combo(op) & 0b111
        elif instr == 3:  # jnz
            if regs['A'] != 0:
                ip = op
        elif instr == 4:  # bxc
            regs['B'] = regs['B'] ^ regs['C']
        elif instr == 5:  # out
            output.append(combo(op) & 0b111)
        elif instr == 6:  # bdv
            regs['B'] = regs['A'] // 2**combo(op)
        elif instr == 7:  # cdv
            regs['C'] = regs['A'] // 2**combo(op)
        debug('   ', regs)

    return ','.join(str(_) for _ in output)

def part1(prog, regs):
    prog = tuple(prog)
    regs = dict(regs)
    out = run(prog, regs)
    print(out)

def run_input(A):
    # debugging and understanding the program...
    out = []
    B = 0
    C = 0
    while A:
        debug()
        debug('A', A)
        B = A & 0b111               # 2, 4      B = A & 0b111
        debug('B store =', B)
        B = B ^ 5                   # 1, 5      B = B ^ 5           shift value
        shift = B
        debug('B shift =', B)
        C = A >> B                  # 7, 5      C = A >> B          A >> B,  B is 0-7
        debug('C store', C & 0b111, 'shifted', B)
        B = B ^ 6                   # 1, 6      B = B ^ 6
        debug('B xor 6', B)
        B = B ^ C                   # 4, 1      B = B ^ C
        debug('B out', B, B & 0b111)
        out.append(B & 0b111)       # 5, 5      out B & 0b111
        A = A >> 3                  # 0, 3      A = A >> 3
                                    # 3, 0      if A == 0 break

    return ','.join(str(_) for _ in out)

def part2(prog, regs):
    # Importantly, the given program consumes 3-bits of reg A for every output,
    # so in backwards order, try each 3-bit number shifted onto our new value
    # and check that a simplified version of the algorithm produces the same
    # output value.  Do this recursively collecting matches and use the
    # smallest match.

    matches = []
    def find(v, out):
        debug(v, out)
        if not out:
            matches.append(v)
            return

        x = out[-1]

        for i in range(8):
            val = (v << 3) | i

            A = val & 0b111
            C = val >> (A ^ 5) & 0b111
            newx = C ^ 5 ^ 6 ^ A

            if newx == x:
                find(val, out[:-1])

    find(0, tuple(prog))

    value = min(matches)

    assert run_input(value) == ','.join(str(_) for _ in prog)

    print(value)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
