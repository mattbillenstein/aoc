#!/usr/bin/env pypy3

import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    lines = [_.split() for _ in lines]
    for line in lines:
        if line[-1] not in 'wxyz':
            line[-1] = int(line[-1])
    return lines

def translate(prog):
    s = '''
def func(input):
    w = x = y = z = 0

'''
    icnt = 0

    for instr in prog:
        op, reg, *rest = instr
        if rest:
            v = rest[0]

        if op == 'inp':
            s += f'    {reg} = input[{icnt}]\n'
            icnt += 1
        elif op == 'mul':
            s += f'    {reg} *= {v}\n'
        elif op == 'add':
            s += f'    {reg} += {v}\n'
        elif op == 'mod':
            s += f'    {reg} %= {v}\n'
        elif op == 'div':
            s += f'    {reg} //= {v}\n'
        elif op == 'eql':
            s += f'    {reg} = int({reg} == {v})\n'
        else:
            assert 0, op

    s += '    return {"w": w, "x": x, "y": y, "z": z}\n'

    return s

def part(prog):
    # faster implementation - translate to python and then spin through some of
    # the digits and look for low z to spin through the other ones...  Bit of
    # trial and error getting this working.

    s = translate(prog)
    debug(s)
    exec(s, globals())

    rng = range(1, 10)

    mn = int(''.join('9' * 14))
    mx = int(''.join('1' * 14))

    L = [9 for _ in range(14)]

    # some pairs of numbers always have a consistent offset, just hardcode a
    # couple and search the rest...
    for L[0] in rng:
      L[13] = L[0] - 4
      if L[13] < 1:
        continue
      for L[1] in rng:
        for L[2] in rng:
          L[3] = L[2] + 3
          if L[3] > 9:
            continue
          for L[4] in rng:
            for L[5] in rng:
              for L[6] in rng:
                d = func(L)
                if DEBUG:
                  print(L, d['z'])
                if d['z'] < 500_000:
                  for L[7] in rng:
                    for L[8] in rng:
                      for L[9] in rng:
                        for L[10] in rng:
                          for L[11] in rng:
                            for L[12] in rng:
                              d = func(L)
                              if d['z'] == 0:
                                n = int(''.join(str(_) for _ in L))
                                if n < mn:
                                  mn = n
                                if n > mx:
                                  mx = n

    print(mx)
    print(mn)

def do_bin(prog):
    exec(translate(prog), globals())
    for i in range(10):
        regs = func([i])
        print(i, regs)

def test_monad(prog):
    exec(translate(prog), globals())
    regs = func([int(_) for _ in sys.argv[2]])
    print(regs)

def main():
    if 'bin' in sys.argv:
        data = parse_input()
        do_bin(data)
    elif 'monad' in sys.argv:
        data = parse_input()
        test_monad(data)
    else:
        data = parse_input()
        part(data)

if __name__ == '__main__':
    main()
