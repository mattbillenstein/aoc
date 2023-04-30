#!/usr/bin/env pypy3


# https://www.redblobgames.com/grids/hexagons/
#
# using doubled-width horizontal layout - column values are doubled between cells

def step_hex(pt, dir):
    nx, ny = pt
    if dir in ('W', 'L', '<'):
        nx -= 2
    elif dir in ('E', 'R', '>'):
        nx += 2
    elif dir in ('NW', 'UL'):
        nx -= 1
        ny -= 1
    elif dir in ('NE', 'UR'):
        nx += 1
        ny -= 1
    elif dir in ('SW', 'DL'):
        nx -= 1
        ny += 1
    elif dir in ('SE', 'DR'):
        nx += 1
        ny += 1
    else:
        assert 0, dir
    return nx, ny

def neighbors6(pt):
    return [step_hex(pt, _) for _ in ('E', 'W', 'NE', 'NW', 'SE', 'SW')]

class HexSparseGrid:
    def __init__(self, items, chars={'.': 0, '#': 1}):
        self.chars = chars
        self.values = {v: k for k, v in chars.items()}

        if isinstance(items, set):
            self.g = {_: 1 for _ in items}
        elif items and isinstance(items, list) and isinstance(items[0], str):
            self.g = {}
            for y in range(len(items)):
                for x in range(len(items[y])):
                    v = self.chars[items[y][x]]
                    if v:
                        self.g[(x, y)] = v
        else:
            self.g = dict(items)

    def copy(self):
        return SparseGrid(dict(self.g), self.chars)

    # props
    @property
    def box(self):
        if not self.g:
            return (0, 0), (0, 0)
        minx = min(_[0] for _ in self.g)
        maxx = max(_[0] for _ in self.g)
        miny = min(_[1] for _ in self.g)
        maxy = max(_[1] for _ in self.g)
        return (minx, miny), (maxx, maxy)

    @property
    def size(self):
        if not self.g:
            return (0, 0)
        box = self.box
        return (
            box[1][0] - box[0][0] + 1,
            box[1][1] - box[0][1] + 1,
        )

    def xs(self, y):
        minx = min(_[0] for _ in self.g)
        maxx = max(_[0] for _ in self.g)

        if y % 2 == 0:
            while minx % 2 == 1:
                minx -= 1
        else:
            while minx % 2 == 0:
                minx -= 1
            
        return range(minx, maxx+2, 2)

    @property
    def ys(self):
        minx = min(_[1] for _ in self.g)
        maxx = max(_[1] for _ in self.g)
        return range(minx-1, maxx+2)

    def get(self, pt, default=None):
        return self.g.get(pt, default)

    # mutate
    def set(self, pt, v):
        self.g[pt] = v

    def remove(self, pt):
        del self.g[pt]

    def add(self, pt):
        self.g[pt] = 1

    def move(self, pt, newpt):
        self.g[newpt] = self.g.pop(pt)

    def clear(self):
        self.g.clear()

    # neighbors
    def neighbors6(self, pt):
        return neighbors6(pt)

    def step(self, pt, dir):
        return step_hex(pt, dir)

    # dict/set ish methods
    def __iter__(self):
        return iter(dict(self.g))

    def __contains__(self, k):
        return k in self.g

    def __len__(self):
        return len(self.g)

    def print(self):
        for y in self.ys:
            s = ''
            if y % 2 == 0:
                s = ' '
            for x in self.xs(y):
                v = self.get((x, y)) or 0
                s += self.values.get(v, '?') + ' '
            print(s)
