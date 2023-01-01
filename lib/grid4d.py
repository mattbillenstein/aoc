#!/usr/bin/env python3

class SparseGrid4D:
    def __init__(self, items, chars={'.': 0, '#': 1}):
        self.chars = chars
        self.values = {v: k for k, v in chars.items()}

        if isinstance(items, set):
            self.g = {_: 1 for _ in items}
        else:
            self.g = dict(items)

    def copy(self):
        return SparseGrid4D(dict(self.g), self.chars)

    def print(self):
        for w in self.ws:
            for z in self.zs:
                print(f'z={z}, w={w}')
                for y in self.ys:
                    s = ''
                    for x in self.xs:
                        v = self.get((x, y, z, w)) or 0
                        s += self.values.get(v, '?')
                    print(s)
                print()

    # props
    @property
    def box(self):
        if not self.g:
            return (0, 0, 0, 0), (0, 0, 0, 0)
        minx = min(_[0] for _ in self.g)
        maxx = max(_[0] for _ in self.g)
        miny = min(_[1] for _ in self.g)
        maxy = max(_[1] for _ in self.g)
        minz = min(_[2] for _ in self.g)
        maxz = max(_[2] for _ in self.g)
        minw = min(_[3] for _ in self.g)
        maxw = max(_[3] for _ in self.g)
        return (minx, miny, minz, minw), (maxx, maxy, maxz, maxw)

    @property
    def size(self):
        if not self.g:
            return (0, 0, 0, 0)
        box = self.box
        return (
            box[1][0] - box[0][0] + 1,
            box[1][1] - box[0][1] + 1,
            box[1][2] - box[0][2] + 1,
            box[1][3] - box[0][3] + 1,
        )

    @property
    def xs(self):
        minx = min(_[0] for _ in self.g)
        maxx = max(_[0] for _ in self.g)
        return range(minx, maxx+1)

    @property
    def ys(self):
        minx = min(_[1] for _ in self.g)
        maxx = max(_[1] for _ in self.g)
        return range(minx, maxx+1)

    @property
    def zs(self):
        minz = min(_[2] for _ in self.g)
        maxz = max(_[2] for _ in self.g)
        return range(minz, maxz+1)

    @property
    def ws(self):
        minw = min(_[3] for _ in self.g)
        maxw = max(_[3] for _ in self.g)
        return range(minw, maxw+1)

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

    # neighbors
    def neighbors80(self, pt):
        # sparsegrid doesn't care about boundaries
        L = []
        for x in range(pt[0]-1, pt[0]+2):
            for y in range(pt[1]-1, pt[1]+2):
                for z in range(pt[2]-1, pt[2]+2):
                    for w in range(pt[3]-1, pt[3]+2):
                        npt = (x, y, z, w)
                        if npt != pt:
                            L.append(npt)
        return L

    # dict/set ish methods
    def __iter__(self):
        return iter(dict(self.g))

    def __contains__(self, k):
        return k in self.g

    def __len__(self):
        return len(self.g)
