import sys

DEBUG = '--debug-intcode' in sys.argv

def debug(*args):
    if DEBUG:
        print(*args)

def run(mem, input=None):
    input = input or []
    output = []
    g = intcode(mem)

    # run up to first yield
    next(g)

    # feed input and collect output
    for x in input:
        v = g.send(x)
        if v is not None:
            yield v

    # finish consuming any other output
    for v in g:
        if v is not None:
            yield v

def intcode(mem):
    mem = list(mem) + [0] * 1_000_000

    rbase = 0
    pc = 0
    while mem[pc] != 99:
        instr = mem[pc]
        op = instr % 100
        mode = [instr // 100 % 10, instr // 1000 % 10, instr // 10000 % 10]

        debug(op, mode, mem[pc:pc+4])

        def load(i):
            # 1 is immediate
            v = mem[pc+i+1]
            if mode[i] == 0:
                # absolute
                v = mem[v]
            elif mode[i] == 2:
                # relative
                v = mem[rbase + v]
            return v

        def store(i, v):
            assert mode[i] != 1  # no immedate store
            if mode[i] == 0:
                mem[mem[pc+i+1]] = v
            elif mode[i] == 2:
                mem[rbase + mem[pc+i+1]] = v

        if op == 1:
            # add
            store(2, load(0) + load(1))
            pc += 4
        elif op == 2:
            # mul
            store(2, load(0) * load(1))
            pc += 4
        elif op == 3:
            # input
            x = None
            while x is None:
                x = yield 'INPUT'
                debug('IN', x)
            store(0, x)
            pc += 2
        elif op == 4:
            # output
            x = load(0)
            debug('OUT', x)
            yield x
            pc += 2
        elif op == 5:
            # jump if true
            if load(0) != 0:
                pc = load(1)
            else:
                pc += 3
        elif op == 6:
            # jump if false
            if load(0) == 0:
                pc = load(1)
            else:
                pc += 3
        elif op == 7:
            # <
            store(2, int(load(0) < load(1)))
            pc += 4
        elif op == 8:
            # ==
            store(2, int(load(0) == load(1)))
            pc += 4
        elif op == 9:
            # set rbase
            rbase += load(0)
            pc += 2
        else:
            assert 0, ('Invalid instruction', op)
