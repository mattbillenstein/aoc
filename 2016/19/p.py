#!/usr/bin/env pypy3

import sys

DEBUG = sys.argv.count('-v')

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return int(lines[0])

def part1(n):
    L = [[_+1] for _ in range(n)]
    pos = 0
    found = True
    while found:
        if L[pos]:
            found = False
            i = (pos + 1) % n
            while i != pos:
                if L[i]:
                    found = True
                    L[pos].extend(L[i])
                    L[i].clear()
                    break
                i = (i + 1) % n
        pos = (pos + 1) % n

    for i in range(len(L)):
        if L[i]:
            print(i+1)
            break

class SkipList:
    def __init__(self, base=10000):
        self.L = [[]]
        self.size = 0
        self.base = base

    def append(self, item):
        if len(self.L[-1]) >= self.base:
            self.L.append([])
        self.L[-1].append(item)
        self.size += 1

    def pop(self, idx):
        i, j = self._get_index(idx)
        item = self.L[i][j]
        self.L[i].pop(j)
        self.size -= 1
        return item
        
    def _get_index(self, idx):
        tot = 0
        for i in range(len(self.L)):
            if tot <= idx < tot + len(self.L[i]):
                break
            tot += len(self.L[i])
        return i, idx - tot

    def __getitem__(self, idx):
        i, j = self._get_index(idx)
        return self.L[i][j]

    def __len__(self):
        return self.size

def part2(n):
    L = SkipList()
    for i in range(n):
        L.append(i+1)

    pos = 0
    while len(L) > 1:
        i = (len(L) // 2 + pos) % len(L)
        L.pop(i)
        if i > pos:
            pos += 1
        pos = pos % len(L)

        if DEBUG:
            if len(L) % 1000 == 0 or len(L) < 20:
                print(pos, len(L))

    print(L[0])

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
