#!/usr/bin/env python3

import sys

def compute_dir_size(d, path):
    size = 0
    for item in d[path].values():
        if item['type'] == 'd':
            # recursively compute size of child dir
            size += compute_dir_size(d, path + (item['name'],))
        else:
            size += item['size']
    return size

def main(argv):
    with open(argv[1]) as f:
        lines = f.readlines()

    # the disk, directory path as tuple -> dict of name -> fileobj
    d = {}
    path = ()  # root dir
    for line in lines:
        if line.startswith('$'):
            in_ls = False
            _, cmd, *rest = line.split()
            if cmd == 'cd':
                arg = rest[0]
                if arg == '/':
                    path = ()
                elif arg == '..':
                    path = path[:-1]
                else:
                    path = path + (arg,)

                if path not in d:
                    d[path] = {}

            elif cmd == 'ls':
                in_ls = True

        elif in_ls:
            size, name = line.split()
            if size == 'dir':
                o = {'type': 'd', 'size': 0, 'name': name}
            else:
                o = {'type': 'f', 'size': int(size), 'name': name}

            # using dict here to potentially clobber multiple listings in same
            # dir, although this didn't happen in my input...
            d[path][name] = o

    total_size = compute_dir_size(d, ()) 
    free_size = 70_000_000 - total_size
    delete_size = 30_000_000 - free_size

    print(f'Tot:{total_size} Free:{free_size} Delete:{delete_size}')

    smallest = (1e9, None)
    tot = 0
    for path in d:
        size = compute_dir_size(d, path)

        # part 1, sum of all dir sizes with <= 100000
        if size <= 100_000:
            tot += size

        # part two, find smallest directory with size >= delete_size
        elif size >= delete_size:
            if size < smallest[0]:
                smallest = (size, path)

    print(tot)
    print(smallest[0], '/' + '/'.join(smallest[1]))

if __name__ == '__main__':
    main(sys.argv)
