#!/usr/bin/env python3

class Cube:
    def __init__(self, pt1, pt2, value=None):
        self.value = value

        self.corners = []
        for x in (pt1[0], pt2[0]):
            for y in (pt1[1], pt2[1]):
                for z in (pt1[2], pt2[2]):
                    self.corners.append((x, y, z))

        self.corners.sort()

        self.pt1 = self.corners[0]
        self.pt2 = self.corners[-1]

        self.xs = (min(self.pt1[0], self.pt2[0]), max(self.pt1[0], self.pt2[0]))
        self.ys = (min(self.pt1[1], self.pt2[1]), max(self.pt1[1], self.pt2[1]))
        self.zs = (min(self.pt1[2], self.pt2[2]), max(self.pt1[2], self.pt2[2]))

    def contains(self, pt):
        return (
            self.xs[0] <= pt[0] <= self.xs[1] and
            self.ys[0] <= pt[1] <= self.ys[1] and
            self.zs[0] <= pt[2] <= self.zs[1]
        )

    def contains_xy(self, pt):
        return (
            self.xs[0] <= pt[0] <= self.xs[1] and
            self.ys[0] <= pt[1] <= self.ys[1]
        )

    def contains_xz(self, pt):
        return (
            self.xs[0] <= pt[0] <= self.xs[1] and
            self.zs[0] <= pt[2] <= self.zs[1]
        )

    def contains_yz(self, pt):
        return (
            self.ys[0] <= pt[1] <= self.ys[1] and
            self.zs[0] <= pt[2] <= self.zs[1]
        )

    def intersection(self, other):
        other_contains = [_ for _ in self.corners if other.contains(_)]
        self_contains  = [_ for _ in other.corners if self.contains(_)]

        # no overlap
        if not self_contains and not other_contains:
            return None

        # swap and deal with just one intersection
        if other_contains and not self_contains:
            self, other = other, self
            self_contains, other_contains = other_contains, self_contains

        # one completely contains other, return a copy
        if len(self_contains) == 8:
            return Cube(other.pt1, other.pt2)
            
        if len(self_contains) == 1:
            assert len(other_contains) == 1
            pts = [self_contains[0], other_contains[0]]
            return Cube(self_contains[0], other_contains[0])

        if len(self_contains) == 2:
            # two points, two axis will be the same, project
            assert len(other_contains) == 0
            a, b = self_contains
            if a[0] == b[0]:
                if a[1] == b[1]:
                    # x/y same, enclose z
                    pt = None
                    for x in self.corners:
                        if other.contains_xy(x):
                            pt = x
                            break
                    assert pt

                    return Cube((a[0], a[1], a[2]), (pt[0], pt[1], b[2]))
                else:
                    # x/z same, enclose y
                    pt = None
                    for x in self.corners:
                        if other.contains_xz(x):
                            pt = x
                            break
                    assert pt

                    return Cube((a[0], a[1], a[2]), (pt[0], b[1], pt[2]))
            else:
                # y/z same, enclose x
                pt = None
                for x in self.corners:
                    if other.contains_yz(x):
                        pt = x
                        break
                assert pt

                return Cube((a[0], a[1], a[2]), (b[0], pt[1], pt[2]))

        if len(self_contains) == 4:
            assert len(other_contains) == 0
            # just need to truncate on one axis given a point outside the box
            # a is inside, b is outside
            a, b = other.pt1, other.pt2
            if self.contains(b):
                a, b = b, a
            
            if self.contains_xy(b):
                if b[2] > self.zs[1]:
                    b = (b[0], b[1], self.zs[1])
                else:
                    b = (b[0], b[1], self.zs[0])
            elif self.contains_xz(b):
                if b[1] > self.ys[1]:
                    b = (b[0], self.ys[1], b[2])
                else:
                    b = (b[0], self.ys[0], b[2])
            else:
                if b[0] > self.xs[1]:
                    b = (self.xs[1], b[1], b[2])
                else:
                    b = (self.xs[0], b[1], b[2])

            return Cube(a, b)

        assert 0

    def __eq__(self, other):
        return self.pt1 == other.pt1 and self.pt2 == other.pt2

    def __repr__(self):
        return f'Cube({self.pt1}, {self.pt2})'

if __name__ == '__main__':
    # equals
    c1 = Cube((0,0,0), (20,20,20))
    assert c1 == Cube((20,20,20), (0,0,0))

    # no intersection
    assert c1.intersection(Cube((100,100,100), (200,200,200))) is None

    # one corner
    c2 = Cube((10,10,10), (30,30,30))
    assert c1.intersection(c2) == c2.intersection(c1) == Cube((10,10,10), (20,20,20))

    # two corners x/y
    c3 = Cube((17, 18, 8), (27, 28, 16))
    assert c1.intersection(c3) == c3.intersection(c1) == Cube((17, 18, 8), (20, 20, 16))
    # two corners x/y
    c3 = Cube((17, 18, 8), (-27, -28, 16))
    assert c1.intersection(c3) == c3.intersection(c1) == Cube((17, 18, 8), (0, 0, 16))

    # two corners x/z
    c3 = Cube((17, 8, 18), (27, 16, 28))
    assert c1.intersection(c3) == c3.intersection(c1) == Cube((17, 8, 18), (20, 16, 20))
    # two corners x/z
    c3 = Cube((17, 8, 18), (-27, 16, -28))
    assert c1.intersection(c3) == c3.intersection(c1) == Cube((17, 8, 18), (0, 16, 0))

    # two corners y/z
    c3 = Cube((8, 18, 17), (16, 28, 27))
    assert c1.intersection(c3) == c3.intersection(c1) == Cube((8, 18, 17), (16, 20, 20))
    # two corners y/z
    c3 = Cube((8, 18, 17), (16, -28, -27))
    assert c1.intersection(c3) == c3.intersection(c1) == Cube((8, 18, 17), (16, 0, 0))

    # four corners - truncate x
    c3 = Cube((17, 6, 8), (27, 15, 16))
    assert c1.intersection(c3) == c3.intersection(c1) == Cube((17, 6, 8), (20, 15, 16))
    # four corners - truncate x
    c3 = Cube((17, 6, 8), (-27, 15, 16))
    assert c1.intersection(c3) == c3.intersection(c1) == Cube((17, 6, 8), (0, 15, 16))

    # four corners - truncate y
    c3 = Cube((6, 17, 8), (16, 27, 16))
    assert c1.intersection(c3) == c3.intersection(c1) == Cube((6, 17, 8), (16, 20, 16))
    # four corners - truncate y
    c3 = Cube((6, 17, 8), (16, -27, 16))
    assert c1.intersection(c3) == c3.intersection(c1) == Cube((6, 17, 8), (16, 0, 16))

    # four corners - truncate z
    c3 = Cube((6, 8, 17), (16, 16, 27))
    assert c1.intersection(c3) == c3.intersection(c1) == Cube((6, 8, 17), (16, 16, 20))
    # four corners - truncate z
    c3 = Cube((6, 8, 17), (16, 16, -27))
    assert c1.intersection(c3) == c3.intersection(c1) == Cube((6, 8, 17), (16, 16, 0))
