#!/usr/bin/env python3

import sys
from collections import defaultdict

def main(argv):
    stacks = defaultdict(list)
    stacklines = []

    with open(argv[1]) as f:
        for line in f:
            if not line.strip():
                continue

            if line.startswith(' 1 '):
                stacklines.reverse()
                for i, c in enumerate(line.rstrip()):
                    if c != ' ':
                        stacks[c] = [_[i] for _ in stacklines if _[i] != ' ']

            elif line.startswith('move '):
                _, cnt, _, s1, _, s2 = line.strip().split()
                cnt = int(cnt)

                items = stacks[s1][-cnt:]
                del stacks[s1][-cnt:]

                # for p2, comment this out
#                items.reverse()

                stacks[s2].extend(items)

            else:
                stacklines.append(line)

        for k, L in stacks.items():
            print(k, L)

        print(''.join(_[-1] for _ in stacks.values()))

if __name__ == '__main__':
    main(sys.argv)
