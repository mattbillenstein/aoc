#!/usr/bin/env python3

import sys

class Thing:
    def __init__(self):
        self.x = 0
        self.y = 0

    def pos(self):
        return (self.x, self.y)

    def __str__(self):
        return str(self.pos())

def main(argv):
    head = Thing()
    tail = Thing()

    with open(argv[1]) as f:
        lines = [_.strip('\r\n') for _ in f]

    visited = set()

    for line in lines:
        dir, cnt = line.split()
        cnt = int(cnt)
        print(f'line "{line}"')
        print(f'head {head}')
        print(f'tail {tail}')
        print()
        for i in range(cnt):
            if dir == 'U':
                head.y += 1
                if tail.y < head.y-1:
                    tail.y = head.y-1
                    tail.x = head.x
            elif dir == 'D':
                head.y -= 1
                if tail.y > head.y+1:
                    tail.y = head.y+1
                    tail.x = head.x
            elif dir == 'R':
                head.x += 1
                if tail.x < head.x-1:
                    tail.x = head.x-1
                    tail.y = head.y
            elif dir == 'L':
                head.x -= 1
                if tail.x > head.x+1:
                    tail.x = head.x+1
                    tail.y = head.y
            else:
                assert 0

            visited.add(tail.pos())

    print(len(visited))

if __name__ == '__main__':
    main(sys.argv)
