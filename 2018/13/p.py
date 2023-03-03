#!/usr/bin/env pypy3

import sys

from grid import Grid

DEBUG = sys.argv.count('-v')

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines

class Cart:
    def __init__(self, dir, pt):
        self.dir = dir
        self.pt = pt
        self.turns = 0

    def turn(self):
        i = self.turns % 3
        if i == 0:
            # left
            self.dir = {'^': '<', '<': 'v', 'v': '>', '>': '^'}[self.dir]
        elif i == 1:
            # straight
            pass
        elif i == 2:
            # right
            self.dir = {'^': '>', '>': 'v', 'v': '<', '<': '^'}[self.dir]

        self.turns += 1

    def curve(self, c):
        self.dir = {
            '^': {'/': '>', '\\': '<'},
            '<': {'/': 'v', '\\': '^'},
            'v': {'/': '<', '\\': '>'},
            '>': {'/': '^', '\\': 'v'},
        }[self.dir][c]

    def __repr__(self):
        return f'Cart({self.dir}, {self.pt})'

def run(data, part):
    chars = {
        ' ': 0, 
        '^': 1,
        '>': 2,
        'v': 3,
        '<': 4,
        '-': 5,
        '|': 6,
        '\\': 7,
        '/': 8,
        '+': 9,
    }
    values = {v: k for k, v in chars.items()}

    g = Grid(data, chars)

    carts = []
    for pt in g:
        c = g.getc(pt)
        if c in '<>':
            g.setc(pt, '-')
            carts.append(Cart(c, pt))
        elif c in 'v^':
            g.setc(pt, '|')
            carts.append(Cart(c, pt))

    while 1:
        carts.sort(key=lambda x:(x.pt[1], x.pt[0]))

        remove = []

        g2 = g.copy()

        for cart in carts:
            npt = g.step(cart.pt, cart.dir)
            c = g.getc(npt)

            assert c != 0

            for cart2 in carts:
                if cart2.pt == npt:
                    remove.append(cart)
                    remove.append(cart2)

                    if part == 1:
                        # print first collision
                        print('Collision:', npt)
                        return

            cart.pt = npt
            if c == '+':
                cart.turn()
            elif c in '/\\':
                cart.curve(c)

            g2.setc(cart.pt, cart.dir)

        for cart in remove:
            carts.remove(cart)

        # part2, only one cart left, print its location
        if len(carts) == 1:
            print(carts[0])
            break

        if DEBUG:
            print(carts)
            g2.print()
            print()

def main():
    data = parse_input()
    if '1' in sys.argv:
        run(data, 1)
    if '2' in sys.argv:
        run(data, 2)

if __name__ == '__main__':
    main()
