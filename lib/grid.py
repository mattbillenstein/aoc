#!/usr/bin/env python3

def neighbors(pt, dir=None):
    x, y = pt
    if dir:
        if dir in ('N', 'U'):
            L = [(_, y-1) for _ in range(x-1, x+1+1)]
        elif dir in ('S', 'D'):
            L = [(_, y+1) for _ in range(x-1, x+1+1)]
        elif dir in ('W', 'L'):
            L = [(x-1, _) for _ in range(y-1, y+1+1)]
        elif dir in ('E', 'R'):
            L = [(x+1, _) for _ in range(y-1, y+1+1)]
        else:
            assert 0, dir
    else:
        L = [(nx, ny) for nx in range(x-1, x+1+1) for ny in range(y-1, y+1+1) if (nx, ny) != (x, y)]

    return L

def neighbors_manhattan(pt, dir=None):
    x, y = pt
    if dir:
        if dir in ('N', 'U'):
            L = [(x, y-1)]
        elif dir in ('S', 'D'):
            L = [(x, y+1)]
        elif dir in ('W', 'L'):
            L = [(x-1, y)]
        elif dir in ('E', 'R'):
            L = [(x+1, y)]
        else:
            assert 0, dir
    else:
        L = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

    return L

def step(pt, dir):
    nx, ny = pt
    if dir in ('N', 'U'):
        ny -= 1
    elif dir in ('S', 'D'):
        ny += 1
    if dir in ('W', 'L'):
        nx -= 1
    elif dir in ('E', 'R'):
        nx += 1
    return nx, ny

class Grid:
    def __init__(self, arr):
        self.g = [list(_) for _ in arr]

    @property
    def box(self):
        if not self.g:
            return (0, 0), (0, 0)
        return (0, len(self.g[0])-1), (0, len(self.g)-1)

    @property
    def size(self):
        return (len(self.g[0]), len(self.g))

    def get(self, pt):
        return self.g[pt[1]][pt[0]]

    def set(self, pt, v):
        self.g[pt[1]][pt[0]] = v

    @property
    def xs(self):
        return range(0, len(self.g[0]))

    @property
    def ys(self):
        return range(0, len(self.g))
    
    def print(self, chars='.#'):
        for y in self.ys:
            s = ''
            for x in self.xs:
                if self.get((x, y)):
                    s += chars[1]
                else:
                    s += chars[0]
            print(s)

    def neighbors(self, pt, dir=None):
        L = neighbors(pt, dir)
        size = self.size
        return [_ for _ in L if 0 <= _[0] < size[0] and 0 <= _[1] < size[1]]

    def neighbors_manhattan(self, pt, dir=None):
        L = neighbors_manhattan(pt, dir)
        size = self.size
        return [_ for _ in L if 0 <= _[0] < size[0] and 0 <= _[1] < size[1]]

    def step(self, pt, dir):
        npt = step(pt, dir)
        size = self.size
        if 0 <= npt[0] < size[0] and 0 <= npt[1] < size[1]:
            return npt
        return None

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

class SparseGrid(Grid):
    def __init__(self, items):
        if isinstance(items, (list, set)):
            self.g = {_: 1 for _ in items}
        else:
            self.g = dict(items)
        self.sizex = 0
        self.sizey = 0

    @property
    def box(self):
        if not self.g:
            return (0, 0), (0, 0)
        minx = min(_[0] for _ in self.g)
        maxx = max(_[0] for _ in self.g)
        miny = min(_[1] for _ in self.g)
        maxy = max(_[1] for _ in self.g)
        return (minx, maxx), (miny, maxy)

    @property
    def size(self):
        if not self.g:
            return (0, 0)
        box = self.box
        return (box[0][1] - box[0][0] + 1, box[1][1] - box[1][0] + 1)

    def get(self, pt):
        return self.g.get(pt)

    def set(self, pt, v):
        self.g[pt] = v
    
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

    def neighbors(self, pt, dir=None):
        # sparsegrid doesn't care about boundaries
        return neighbors(pt, dir)

    def neighbors_manhattan(self, pt, dir=None):
        # sparsegrid doesn't care about boundaries
        return neighbors_manhattan(pt, dir)

    def step(self, pt, dir):
        return step(pt, dir)

    # dict/set ish methods
    def __iter__(self):
        return iter(self.g)

    def __contains__(self, k):
        return k in self.g

    def __len__(self):
        return len(self.g)

    def remove(self, k):
        del self.g[k]

    def add(self, k):
        self.g[k] = 1

    def move(self, pt, newpt):
        self.g[newpt] = self.g.pop(pt)

if __name__ == '__main__':
    g1 = Grid([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    g2 = SparseGrid({
        (0, 0): 0, (1, 0): 1, (2, 0): 2,
        (0, 1): 3, (1, 1): 4, (2, 1): 5,
        (0, 2): 6, (1, 2): 7, (2, 2): 8,
    })

    g1.print()
    g2.print()

    assert g1.box == g2.box, (g1.box, g2.box)
    assert g1.size == g2.size
    assert g1.xs == g2.xs
    assert g1.ys == g2.ys

    # neighbors including diagonals
    assert g1.neighbors((0, 0)) == [(0, 1), (1, 0), (1, 1)], g1.neighbors((0, 0))
    assert g1.neighbors((1, 0)) == [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)], g1.neighbors((1, 0))
    assert g1.neighbors((1, 1)) == [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)], g1.neighbors((1, 1))
    assert g1.neighbors((1, 0), 'N') == [], g1.neighbors((1, 1))
    assert g1.neighbors((1, 0), 'S') == [(0, 1), (1, 1), (2, 1)], g1.neighbors((1, 0), 'S')

    assert g1.neighbors_manhattan((0, 0)) == [(1, 0), (0, 1)], g1.neighbors_manhattan((0, 0))
    assert g1.neighbors_manhattan((1, 0)) == [(0, 0), (2, 0), (1, 1)], g1.neighbors_manhattan((1, 0))
    assert g1.neighbors_manhattan((1, 1)) == [(0, 1), (2, 1), (1, 0), (1, 2)], g1.neighbors_manhattan((1, 1))

    # sparsegrid has no borders...
    assert g2.neighbors((0, 0)) == [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)], g2.neighbors((0, 0))
    assert g2.neighbors((1, 0), 'N') == [(0, -1), (1, -1), (2, -1)], g2.neighbors((1, 0), 'N')
    assert g2.neighbors((1, 0), 'S') == [(0, 1), (1, 1), (2, 1)], g2.neighbors((1, 0), 'S')

    assert g2.neighbors_manhattan((0, 0)) == [(-1, 0), (1, 0), (0, -1), (0, 1)], g2.neighbors_manhattan((0, 0))
    assert g2.neighbors_manhattan((1, 0)) == [(0, 0), (2, 0), (1, -1), (1, 1)], g2.neighbors_manhattan((1, 0))
    assert g2.neighbors_manhattan((1, 0), 'N') == [(1, -1)], g2.neighbors_manhattan((1, 0), 'N')
    assert g2.neighbors_manhattan((1, 0), 'S') == [(1, 1)], g2.neighbors_manhattan((1, 0), 'S')
    assert g2.neighbors_manhattan((1, 1)) == [(0, 1), (2, 1), (1, 0), (1, 2)], g2.neighbors_manhattan((1, 1))

    assert list(g1) == list(g2)
    assert (1, 1) in g1
    assert (1, 1) in g2
    assert (10, 10) not in g1
    assert (10, 10) not in g2

    assert len(g1) == len(g2)
