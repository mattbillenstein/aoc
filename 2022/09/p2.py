#!/usr/bin/env python3

import string
import sys

class Thing:
    def __init__(self, name):
        self.name = name
        self.x = 0
        self.y = 0
        self.tail = None

    def pos(self):
        return (self.x, self.y)

    def __str__(self):
        return str(self.pos())

    def move(self, dir):
        head = self
        tail = self.tail

        pos = head.pos()

        if dir == 'U':
            head.y += 1
            if tail and tail.y < head.y-1:
                if tail.x < head.x:
                    tail.move('UR')
                elif tail.x > head.x:
                    tail.move('UL')
                else:
                    tail.move('U')
        elif dir == 'D':
            head.y -= 1
            if tail and tail.y > head.y+1:
                if tail.x < head.x:
                    tail.move('DR')
                elif tail.x > head.x:
                    tail.move('DL')
                else:
                    tail.move('D')
        elif dir == 'R':
            head.x += 1
            if tail and tail.x < head.x-1:
                if tail.y < head.y:
                    tail.move('RU')
                elif tail.y > head.y:
                    tail.move('RD')
                else:
                    tail.move('R')
        elif dir == 'L':
            head.x -= 1
            if tail and tail.x > head.x+1:
                if tail.y < head.y:
                    tail.move('LU')
                elif tail.y > head.y:
                    tail.move('LD')
                else:
                    tail.move('L')

        # diagonals? this is dumb, easier to model these as two single moves? WTF
        elif dir == 'UR':
            head.x += 1
            head.y += 1
            if tail:
                if tail.pos() != pos and tail.x != head.x and tail.y != head.y:
                    tail.move(dir)
                elif head.x - tail.x > 1:
                    tail.move('R')
                elif head.y - tail.y > 1:
                    tail.move('U')
        elif dir == 'UL':
            head.x -= 1
            head.y += 1
            if tail:
                if tail.pos() != pos and tail.x != head.x and tail.y != head.y:
                    tail.move(dir)
                elif tail.x - head.x > 1:
                    tail.move('L')
                elif head.y - tail.y > 1:
                    tail.move('U')
        elif dir == 'DR':
            head.x += 1
            head.y -= 1
            if tail:
                if tail.pos() != pos and tail.x != head.x and tail.y != head.y:
                    tail.move(dir)
                elif head.x - tail.x > 1:
                    tail.move('R')
                elif tail.y - head.y > 1:
                    tail.move('D')
        elif dir == 'DL':
            head.x -= 1
            head.y -= 1
            if tail:
                if tail.pos() != pos and tail.x != head.x and tail.y != head.y:
                    tail.move(dir)
                elif tail.x - head.x > 1:
                    tail.move('L')
                elif tail.y - head.y > 1:
                    tail.move('D')
        elif dir == 'RU':
            head.x += 1
            head.y += 1
            if tail:
                if tail.pos() != pos and tail.x != head.x and tail.y != head.y:
                    tail.move(dir)
                elif head.y - tail.y > 1:
                    tail.move('U')
                elif head.x - tail.x > 1:
                    tail.move('R')
        elif dir == 'RD':
            head.x += 1
            head.y -= 1
            if tail:
                if tail.pos() != pos and tail.x != head.x and tail.y != head.y:
                    tail.move(dir)
                elif tail.y - head.y > 1:
                    tail.move('D')
                elif head.x - tail.x > 1:
                    tail.move('R')
        elif dir == 'LU':
            head.x -= 1
            head.y += 1
            if tail:
                if tail.pos() != pos and tail.x != head.x and tail.y != head.y:
                    tail.move(dir)
                elif head.y - tail.y > 1:
                    tail.move('U')
                elif tail.x - head.x > 1:
                    tail.move('L')
        elif dir == 'LD':
            head.x -= 1
            head.y -= 1
            if tail:
                if tail.pos() != pos and tail.x != head.x and tail.y != head.y:
                    tail.move(dir)
                elif tail.y - head.y > 1:
                    tail.move('D')
                elif tail.x - head.x > 1:
                    tail.move('L')

    def step(self, dir):
        if dir == 'U':
            self.y += 1
        elif dir == 'D':
            self.y -= 1
        elif dir == 'L':
            self.x -= 1
        elif dir == 'R':
            self.x += 1

        if self.tail:
            self.tail.follow(self)

    def follow(self, other):
        dx = other.x - self.x
        dy = other.y - self.y

        if abs(dx) <= 1 and abs(dy) <= 1:
            return

        if dx == 0:
            self.y += 1 if dy > 0 else -1
        elif dy == 0:
            self.x += 1 if dx > 0 else -1

        else:
            self.x += 1 if dx > 0 else -1
            self.y += 1 if dy > 0 else -1

        if self.tail:
            self.tail.follow(self)

def main(argv):
    num_knots = int(argv[2])
    letters = string.printable
    knots = [Thing(letters[_]) for _ in range(num_knots)]
    for i in range(1, len(knots)):
        knots[i-1].tail = knots[i]

    head = knots[0]
    tail = knots[-1]

    with open(argv[1]) as f:
        lines = [_.strip('\r\n') for _ in f]

    visited = set()

    for line in lines:
        dir, cnt = line.split()
        cnt = int(cnt)
        print(f'head {head}')
        print(f'tail {tail}')
        print()
        print(f'line "{line}"')
        for i in range(cnt):
            # my original bad code, propagating moves head -> tail
#            head.move(dir)

            # better solution having knot[i+1] follow knot [i]
            head.step(dir)

            visited.add(tail.pos())

        print_grid(knots)
        print()

    print(len(visited))


def print_grid(knots):
    buffer = 10
    minx = min(_.x for _ in knots) - buffer
    maxx = max(_.x for _ in knots) + buffer

    miny = min(_.y for _ in knots) - buffer
    maxy = max(_.y for _ in knots) + buffer

    positions = {_.pos(): _.name for _ in reversed(knots)}

    for j in range(maxy - miny, 0, -1):
        s = ''
        for i in range(0, maxx - minx):
            ix = i + minx
            iy = j + miny

            if (ix, iy) in positions:
                s += positions[(ix, iy)]
            elif (ix, iy) == (0, 0):
                s += 's'
            else:
                s += '.'

        print(s)


if __name__ == '__main__':
    main(sys.argv)
