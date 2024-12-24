#!/usr/bin/env pypy3

import sys
from collections import namedtuple
from itertools import permutations

DEBUG = sys.argv.count('-v')

Gate = namedtuple('Gate', ['type', 'a', 'b', 'q'])

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    inputs = {}
    gates = {}
    for line in lines:
        if ':' in line:
            inp, val = line.replace(':', '').split()
            inputs[inp] = int(val)
        elif '->' in line:
            w1, type, w2, _, out = line.split()
            if w1[0] == 'y' and w2[0] == 'x':
                w1, w2 = w2, w1
            gates[out] = Gate(type, a=w1, b=w2, q=out)
    
    return (inputs, gates)

def solve(inputs, gates):
    # collect all wires and assign known value
    wires = {_: None for _ in gates}
    for inp, v in inputs.items():
        wires[inp] = v

    # while there are any unknowns, propagate ins to outs
    while any(_ is None for _ in wires.values()):
        for g in gates.values():
            if wires[g.q] is None:
                if wires[g.a] is not None and wires[g.b] is not None:
                    if g.type == 'AND':
                        wires[g.q] = (wires[g.a] & wires[g.b]) & 1
                    elif g.type == 'OR':
                        wires[g.q] = (wires[g.a] | wires[g.b]) & 1
                    elif g.type == 'XOR':
                        wires[g.q] = (wires[g.a] ^ wires[g.b]) & 1

    # compute output value, shift each bit into an int...
    x = 0
    for i in range(100):
        name = f'z{i:02d}'
        if name not in wires:
            break
        x |= (wires[name] << i)
        
    return x

def part1(inputs, gates):
    print(solve(inputs, gates))

def part2(inputs, gates):
    # Circuit just implements a full adder:
    #
    #   Zi = (Xi XOR Yi) XOR Ci-1
    #   Ci = (Xi AND Yi) OR ((Xi XOR Yi) AND Ci-1)
    #
    # Don't need to compute or simulate anything, just trace back structurally
    # from each Zi checking for bad outputs/inputs...

    bad = []

    zs = sorted([_.q for _ in gates.values() if _.q[0] == 'z'])
    Z0, ZN = zs[0], zs[-1]

    z0 = gates[Z0]
    zn = gates[ZN]

    # Special case, Z0 = X0 XOR Y0
    if z0.type != 'XOR':
        bad.append((Z0, f'{Z0} not XOR'))
    else:
        assert z0.a == Z0.replace('z', 'x'), in1
        assert z0.b == Z0.replace('z', 'y'), in2

    # Special case, ZN is just carry-out N-1
    if zn.type != 'OR':
        bad.append((ZN, f'{ZN} not OR'))
    else:
        # just check they're and
        assert gates[zn.a].type == 'AND'
        assert gates[zn.b].type == 'AND'

    # otherwise, check each Zi
    for i in range(1, len(zs)-1):
        c = f'c{i:02d}'
        x = f'x{i:02d}'
        y = f'y{i:02d}'
        z = f'z{i:02d}'

        # check output direct
        zi = gates[z]
        if zi.type != 'XOR':
            bad.append((z, f'{z} not XOR {zi.type}'))
            continue

        # Grab Zi inputs
        g1 = gates[zi.a]
        g2 = gates[zi.b]

        # Swap gates making g1 Zi and g2 Ci - either could actually be wrong
        # which is why this check is written this way...
        if g1.type == 'OR' or g2.type == 'XOR':
            g1, g2 = g2, g1

        # Zi = Xi XOR Yi
        if g1.type != 'XOR':
            bad.append((g1.q, f'{z} in1 not XOR'))
        else:
            # Xi
            if g1.a != x:
                bad.append((g1.q, f'{z} in1 XOR in1 not {x}'))
            # Yi
            if g1.b != y:
                bad.append((g1.q, f'{z} in2 XOR in2 not {y}'))

        # Ci = (Xi AND Yi) OR ((Xi XOR Yi) AND Ci-1)
        if g2.type == 'AND' and i == 1:
            # C0 is just X AND Y - no carry-in
            pass
        elif g2.type != 'OR':
            # Ci = _ OR _
            bad.append((g2.q, f'{c} not OR'))
        else:
            # Just checking both ANDs here, seems to be enough without checking
            # inputs as well...
            g2a = gates[g2.a]
            if g2a.type != 'AND':
                bad.append((g2.a, f'{c} in1 not AND {g2a.type}'))

            g2b = gates[g2.b]
            if g2b.type != 'AND':
                bad.append((g2.b, f'{c} in2 not AND {g2b.type}'))

    if DEBUG:
        for item in bad:
            print(item)
        print(len(bad))

    bad = [_[0] for _ in bad]
    print(','.join(sorted(bad)))

    # for fun, try all swaps until our input solves
    x = y = 0
    for n, v in inputs.items():
        if v:
            i = int(n[1:])
            if n[0] == 'x':
                x |= v << i
            else:
                y |= v << i

    z = x + y

    if DEBUG:
        print(f"{x} + {y} = {z}")

    for tup in permutations(bad):
        swaps = list(zip(tup[::2], tup[1::2]))

        gs = dict(gates)
        for a, b in swaps:
            gs[a], gs[b] = gs[b]._replace(q=a), gs[a]._replace(q=b)

        zz = solve(inputs, gs)

        if zz == z:
            if DEBUG:
                print("Swaps =", swaps)
            break

    assert zz == z


def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
