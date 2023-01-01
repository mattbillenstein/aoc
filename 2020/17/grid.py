#!/usr/bin/env python3

def neighbors8(pt, dir=None):
    x, y = pt
    if dir:
        if dir in ('N', 'U', '^'):
            L = [(_, y-1) for _ in range(x-1, x+1+1)]
        elif dir in ('S', 'D', 'v'):
            L = [(_, y+1) for _ in range(x-1, x+1+1)]
        elif dir in ('W', 'L', '<'):
            L = [(x-1, _) for _ in range(y-1, y+1+1)]
        elif dir in ('E', 'R', '>'):
            L = [(x+1, _) for _ in range(y-1, y+1+1)]
        else:
            assert 0, dir
    else:
        L = [(nx, ny) for nx in range(x-1, x+1+1) for ny in range(y-1, y+1+1) if (nx, ny) != (x, y)]

    return L

def neighbors4(pt, dir=None):
    x, y = pt
    if dir:
        if dir in ('N', 'U', '^'):
            L = [(x, y-1)]
        elif dir in ('S', 'D', 'v'):
            L = [(x, y+1)]
        elif dir in ('W', 'L', '<'):
            L = [(x-1, y)]
        elif dir in ('E', 'R', '>'):
            L = [(x+1, y)]
        else:
            assert 0, dir
    else:
        L = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

    return L

def neighbors4d(pt, dir=None):
    # diagonals only
    x, y = pt
    if dir:
        if dir in ('NW', 'UL'):
            L = [(x-1, y-1)]
        elif dir in ('NE', 'UR'):
            L = [(x+1, y-1)]
        elif dir in ('SW', 'DL'):
            L = [(x-1, y+1)]
        elif dir in ('SE', 'DR'):
            L = [(x+1, y+1)]
        else:
            assert 0, dir
    else:
        L = [(x-1, y-1), (x+1, y-1), (x-1, y+1), (x+1, y+1)]

    return L

def step(pt, dir):
    nx, ny = pt
    if dir in ('N', 'U', '^'):
        ny -= 1
    elif dir in ('S', 'D', 'v'):
        ny += 1
    elif dir in ('W', 'L', '<'):
        nx -= 1
    elif dir in ('E', 'R', '>'):
        nx += 1
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

class Grid:
    def __init__(self, items, chars={'.': 0, '#': 1}):
        self.chars = chars
        self.values = {v: k for k, v in chars.items()}

        if isinstance(items, list) and isinstance(items[0], str):
            self.g = [[0] * len(items[0]) for _ in items]
            for y in range(len(items)):
                for x in range(len(items[y])):
                    v = chars[items[y][x]]
                    if v:
                        self.g[y][x] = v
        else:
            self.g = [list(_) for _ in items]

    def copy(self):
        return Grid([list(_) for _ in self.g], self.chars)

    def print(self):
        for y in self.ys:
            s = ''
            for x in self.xs:
                v = self.get((x, y)) or 0
                s += self.values.get(v, '?')
            print(s)

    # props
    @property
    def box(self):
        if not self.g:
            return (0, 0), (0, 0)
        return (0, len(self.g[0])-1), (0, len(self.g)-1)

    @property
    def size(self):
        return (len(self.g[0]), len(self.g))

    @property
    def xs(self):
        return range(0, len(self.g[0]))

    @property
    def ys(self):
        return range(0, len(self.g))

    def get(self, pt):
        return self.g[pt[1]][pt[0]]

    # mutate
    def set(self, pt, v):
        self.g[pt[1]][pt[0]] = v

    def remove(self, pt):
        self.g[pt[1]][pt[0]] = 0

    def add(self, pt):
        self.g[pt[1]][pt[0]] = 1

    def move(self, pt, newpt):
        self.g[newpt[1]][newpt[0]] = self.g[pt[1]][pt[0]]
        self.g[pt[1]][pt[0]] = 0

    # neighbors
    def neighbors8(self, pt, dir=None):
        L = neighbors8(pt, dir)
        size = self.size
        return [_ for _ in L if 0 <= _[0] < size[0] and 0 <= _[1] < size[1]]

    def neighbors4(self, pt, dir=None):
        L = neighbors4(pt, dir)
        size = self.size
        return [_ for _ in L if 0 <= _[0] < size[0] and 0 <= _[1] < size[1]]

    def neighbors4d(self, pt, dir=None):
        L = neighbors4d(pt, dir)
        size = self.size
        return [_ for _ in L if 0 <= _[0] < size[0] and 0 <= _[1] < size[1]]

    def step(self, pt, dir):
        npt = step(pt, dir)
        size = self.size
        if 0 <= npt[0] < size[0] and 0 <= npt[1] < size[1]:
            return npt
        return None

    # dict/set ish methods
    def __iter__(self):
        for y in self.ys:
            for x in self.xs:
                yield (x, y)

    def __contains__(self, pt):
        size = self.size
        return 0 <= pt[0] < size[0] and 0 <= pt[1] < size[1]

    def __len__(self):
        size = self.size
        return size[0] * size[1]

    # transformations
    def flip_x(self):
        self.g.reverse()

    def flip_y(self):
        for L in self.g:
            L.reverse()

    def rotate_cw(self):
        self.g[:] = [list(_) for _ in zip(*self.g[::-1])]

    def rotate_ccw(self):
        self.g[:] = [list(_) for _ in zip(*self.g)][::-1]

class SparseGrid(Grid):
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
    def neighbors8(self, pt, dir=None):
        # sparsegrid doesn't care about boundaries
        return neighbors8(pt, dir)

    def neighbors4(self, pt, dir=None):
        # sparsegrid doesn't care about boundaries
        return neighbors4(pt, dir)

    def neighbors4d(self, pt, dir=None):
        return neighbors4d(pt, dir)

    def step(self, pt, dir):
        return step(pt, dir)

    # dict/set ish methods
    def __iter__(self):
        return iter(dict(self.g))

    def __contains__(self, k):
        return k in self.g

    def __len__(self):
        return len(self.g)

    # transformations
    def flip_x(self):
        _, sizey = self.size
        self.g = {(pt[0], sizey-1-pt[1]): v for pt, v in self.g.items()}

    def flip_y(self):
        sizex, _ = self.size
        self.g = {(sizex-1-pt[0], pt[1]): v for pt, v in self.g.items()}

    def rotate_cw(self):
        _, sizey = self.size
        self.g = {(sizey-1-pt[1], pt[0]): v for pt, v in self.g.items()}

    def rotate_ccw(self):
        sizex, _ = self.size
        self.g = {(pt[1], sizex-1-pt[0]): v for pt, v in self.g.items()}

class SparseGrid3D:
    def __init__(self, items, chars={'.': 0, '#': 1}):
        self.chars = chars
        self.values = {v: k for k, v in chars.items()}

        if isinstance(items, set):
            self.g = {_: 1 for _ in items}
        else:
            self.g = dict(items)

    def copy(self):
        return SparseGrid3D(dict(self.g), self.chars)

    def print(self):
        for z in self.zs:
            print(f'z = {z}')
            for y in self.ys:
                s = ''
                for x in self.xs:
                    v = self.get((x, y, z)) or 0
                    s += self.values.get(v, '?')
                print(s)
            print()

    # props
    @property
    def box(self):
        if not self.g:
            return (0, 0, 0), (0, 0, 0)
        minx = min(_[0] for _ in self.g)
        maxx = max(_[0] for _ in self.g)
        miny = min(_[1] for _ in self.g)
        maxy = max(_[1] for _ in self.g)
        minz = min(_[2] for _ in self.g)
        maxz = max(_[2] for _ in self.g)
        return (minx, miny, minz), (maxx, maxy, maxz)

    @property
    def size(self):
        if not self.g:
            return (0, 0, 0)
        box = self.box
        return (box[0][1] - box[0][0] + 1, box[1][1] - box[1][0] + 1, box[2][1] - box[2][0])

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
    def neighbors26(self, pt):
        # sparsegrid doesn't care about boundaries
        L = []
        for x in range(pt[0]-1, pt[0]+2):
            for y in range(pt[1]-1, pt[1]+2):
                for z in range(pt[2]-1, pt[2]+2):
                    npt = (x, y, z)
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

if __name__ == '__main__':
    g1 = Grid([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    g2 = SparseGrid({
        (0, 0): 0, (1, 0): 1, (2, 0): 2,
        (0, 1): 3, (1, 1): 4, (2, 1): 5,
        (0, 2): 6, (1, 2): 7, (2, 2): 8,
    })

#    g1.print()
#    g2.print()

    assert g1.box == g2.box, (g1.box, g2.box)
    assert g1.size == g2.size
    assert g1.xs == g2.xs
    assert g1.ys == g2.ys

    # neighbors including diagonals
    assert g1.neighbors8((0, 0)) == [(0, 1), (1, 0), (1, 1)], g1.neighbors8((0, 0))
    assert g1.neighbors8((1, 0)) == [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)], g1.neighbors8((1, 0))
    assert g1.neighbors8((1, 1)) == [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)], g1.neighbors8((1, 1))
    assert g1.neighbors8((1, 0), 'N') == [], g1.neighbors8((1, 1))
    assert g1.neighbors8((1, 0), 'S') == [(0, 1), (1, 1), (2, 1)], g1.neighbors8((1, 0), 'S')

    assert g1.neighbors4((0, 0)) == [(1, 0), (0, 1)], g1.neighbors4((0, 0))
    assert g1.neighbors4((1, 0)) == [(0, 0), (2, 0), (1, 1)], g1.neighbors4((1, 0))
    assert g1.neighbors4((1, 1)) == [(0, 1), (2, 1), (1, 0), (1, 2)], g1.neighbors4((1, 1))

    # sparsegrid has no borders...
    assert g2.neighbors8((0, 0)) == [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)], g2.neighbors8((0, 0))
    assert g2.neighbors8((1, 0), 'N') == [(0, -1), (1, -1), (2, -1)], g2.neighbors8((1, 0), 'N')
    assert g2.neighbors8((1, 0), 'S') == [(0, 1), (1, 1), (2, 1)], g2.neighbors8((1, 0), 'S')

    assert g2.neighbors4((0, 0)) == [(-1, 0), (1, 0), (0, -1), (0, 1)], g2.neighbors4((0, 0))
    assert g2.neighbors4((1, 0)) == [(0, 0), (2, 0), (1, -1), (1, 1)], g2.neighbors4((1, 0))
    assert g2.neighbors4((1, 0), 'N') == [(1, -1)], g2.neighbors4((1, 0), 'N')
    assert g2.neighbors4((1, 0), 'S') == [(1, 1)], g2.neighbors4((1, 0), 'S')
    assert g2.neighbors4((1, 1)) == [(0, 1), (2, 1), (1, 0), (1, 2)], g2.neighbors4((1, 1))

    assert list(g1) == list(g2)
    assert (1, 1) in g1
    assert (1, 1) in g2
    assert (10, 10) not in g1
    assert (10, 10) not in g2

    assert len(g1) == len(g2)
