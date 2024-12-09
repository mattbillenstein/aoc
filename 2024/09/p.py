#!/usr/bin/env pypy3

import sys

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    return lines[0]

def parse_as_blocks(map):
    id = 0
    disk = []
    is_file = True
    for c in map:
        x = int(c)
        y = -1
        if is_file:
            y = id
            id += 1
        for _ in range(x):
            disk.append(y)
        is_file = not is_file
    return disk

def checksum(disk):
    cksum = 0
    for i, x in enumerate(disk):
        if x == -1:
            continue
        cksum += i * x
    return cksum

def part1(data):
    disk = parse_as_blocks(data)

    # compact by moving individual blocks
    i = 0
    j = len(disk) - 1
    while 1:
        while disk[i] != -1:
            i += 1
        while disk[j] == -1:
            j -= 1
        if j <= i:
            break

        disk[i], disk[j] = disk[j], disk[i]

    print(checksum(disk))

def parse_as_files(map):
    id = 0
    disk = []
    is_file = True
    for c in map:
        x = int(c)
        tup = (-1, x)
        if is_file:
            tup = (id, x)
            id += 1
        disk.append(tup)
        is_file = not is_file
    return disk

def part2(data):
    # compact whole files into the leftmost available free spot, merge and
    # manage free blocks
    disk = parse_as_files(data)
    maxid = max(_[0] for _ in disk)

    for id in range(maxid, -1, -1):
        bidx = 0
        while disk[bidx][0] != id:
            bidx += 1

        size = disk[bidx][1]

        fidx = 0
        while fidx < len(disk) and (disk[fidx][0] != -1 or disk[fidx][1] < size):
            fidx += 1

        # insert file block before free block, reduce size of free block
        if fidx < len(disk) and fidx < bidx:
            block = disk[bidx]
            disk[bidx] = (-1, block[1])  # make it free
            free = disk[fidx]
            disk[fidx] = (-1, free[1]-block[1]) # free leftover space
            disk.insert(fidx, block)

        # merge free blocks or delete empty free blocks
        while 1:
            changed = False

            # remove empty free blocks
            i = 0
            while i < len(disk):
                # remove empty free file at i
                if disk[i][0] == -1 and disk[i][1] == 0:
                    changed = True
                    disk = disk[:i] + disk[i+1:]
                    break

                # merge adjacent free blocks at i, i+1 into i+1, remove i
                if i < len(disk)-1 and disk[i][0] == -1 and disk[i+1][0] == -1:
                    changed = True
                    disk[i+1] = (-1, disk[i][1] + disk[i+1][1])
                    disk = disk[:i] + disk[i+1:]
                    break

                i += 1

            if not changed:
                break

    # convert file disk to block disk for checksum
    bdisk = []
    for id, size in disk:
        for i in range(size):
            bdisk.append(id)

    print(checksum(bdisk))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
