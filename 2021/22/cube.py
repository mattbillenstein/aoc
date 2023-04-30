#!/usr/bin/env pypy3

class Cube:
    def __init__(self, pt1, pt2, value=None):
        self.value = value
        self.pt1 = (
            min(pt1[0], pt2[0]),
            min(pt1[1], pt2[1]),
            min(pt1[2], pt2[2]),
        )
        self.pt2 = (
            max(pt1[0], pt2[0]),
            max(pt1[1], pt2[1]),
            max(pt1[2], pt2[2]),
        )

    @property
    def volume(self):
        # volume including boundaries - so a point-cube has a volume of 1
        return (self.pt2[0] - self.pt1[0] + 1) \
             * (self.pt2[1] - self.pt1[1] + 1) \
             * (self.pt2[2] - self.pt1[2] + 1)

    def intersection(self, other):
        xmin = max(self.pt1[0], other.pt1[0])
        xmax = min(self.pt2[0], other.pt2[0])
        ymin = max(self.pt1[1], other.pt1[1])
        ymax = min(self.pt2[1], other.pt2[1])
        zmin = max(self.pt1[2], other.pt1[2])
        zmax = min(self.pt2[2], other.pt2[2])

        if xmin > xmax or ymin > ymax or zmin > zmax:
            return None
        return Cube((xmin, ymin, zmin), (xmax, ymax, zmax))

    def __eq__(self, other):
        return self.pt1 == other.pt1 and self.pt2 == other.pt2

    def __hash__(self):
        return hash((self.pt1, self.pt2, self.value))

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

    # point cube
    c4 = Cube((10, 10, 10), (10, 10, 10))
    assert c1.intersection(c4) == c4.intersection(c1) == c4

    # plane cube
    c5 = Cube((10, 10, 10), (30, 30, 10))
    assert c1.intersection(c5) == c5.intersection(c1) == Cube((10, 10, 10), (20, 20, 10))
