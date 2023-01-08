#!/usr/bin/env pypy3

import math
import sys
import time
from collections import defaultdict
from pprint import pprint

from grid import Grid

DEBUG = '--debug' in sys.argv

class Tile(Grid):
    def __init__(self, items, id):
        self.id = id
        super().__init__(items)

    @property
    def edge_T(self):
        return ''.join(str(self.get((_, 0))) for _ in self.xs)

    @property
    def edge_Tm(self):
        # the min of current orientation and reversed...
        e = self.edge_T
        er = ''.join(reversed(e))
        return min(e, er)

    @property
    def edge_B(self):
        return ''.join(str(self.get((_, self.box[1][1]))) for _ in self.xs)

    @property
    def edge_Bm(self):
        e = self.edge_B
        er = ''.join(reversed(e))
        return min(e, er)

    @property
    def edge_L(self):
        return ''.join(str(self.get((0, _))) for _ in self.ys)

    @property
    def edge_Lm(self):
        e = self.edge_L
        er = ''.join(reversed(e))
        return min(e, er)

    @property
    def edge_R(self):
        return ''.join(str(self.get((self.box[0][1], _))) for _ in self.ys)

    @property
    def edge_Rm(self):
        e = self.edge_R
        er = ''.join(reversed(e))
        return min(e, er)

def debug(*args):
    if DEBUG:
        print(*args)

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    tiles = {}
    for line in lines:
        if line.startswith('Tile '):
            id = int(line.split()[1][:-1])
            tiles[id] = tile = []
        elif line:
            tile.append(line)

    for id in list(tiles):
        tiles[id] = Tile(tiles[id], id)

    return tiles

def run(tiles):
    # edge to list of tile id
    edges = defaultdict(list)
    for tile_id, tile in tiles.items():
        edges[tile.edge_Tm].append(tile_id)
        edges[tile.edge_Bm].append(tile_id)
        edges[tile.edge_Lm].append(tile_id)
        edges[tile.edge_Rm].append(tile_id)

    # compute corners - having two edges with just that tile sharing that edge
    corners = defaultdict(int)
    for eid, L in edges.items():
        if len(L) == 1:
            corners[L[0]] += 1

    corners = [k for k, v in corners.items() if v == 2]

    return edges, corners

def part1(tiles):
    edges, corners = run(tiles)

    # product of corner ids
    print(math.prod(corners))

def part2(tiles):
    edges, corners = run(tiles)

    size = int(math.sqrt(len(tiles)))

    # pick a corner and orient it for top-left
    T = corners[0]
    TT = tiles[T]
    while len(edges[TT.edge_Tm]) > 1 or len(edges[TT.edge_Lm]) > 1:
        TT.rotate_cw()

    # larger grid holding tiles
    G = [[None] * size for _ in range(size)]
    G[0][0] = TT

    # stitch everything to the top-left tile, for the first tile on a row,
    # stitch it to the tile above, then stitch the rest of the row to that
    # tile...
    for row in range(0, size):
        for col in range(0, size):
            if G[row][col] is not None:
                continue

            if col == 0:
                # stitch to top
                U = G[row-1][col]

                # find the other tile that shares this edge
                tile_id = [_ for _ in edges[U.edge_Bm] if _ != U.id][0]
                T = tiles[tile_id]

                # put it on the big grid
                G[row][col] = T

                # rotate until matching
                while T.edge_Tm != U.edge_Bm:
                    T.rotate_cw()

                # flip if not equal
                if T.edge_T != U.edge_B:
                    T.flip_y()

                assert len(edges[T.edge_Lm]) == 1  # faces out
            else:
                # stitch to left
                L = G[row][col-1]

                tile_id = [_ for _ in edges[L.edge_Rm] if _ != L.id][0]
                T = tiles[tile_id]

                G[row][col] = T

                while T.edge_Lm != L.edge_Rm:
                    T.rotate_cw()

                if T.edge_L != L.edge_R:
                    T.flip_x()

                assert T.edge_L == L.edge_R

            if row > 0:
                # check top edge to bottom of tile above...
                assert T.edge_T == G[row-1][col].edge_B

    # compute size of new grid
    tile_size = G[0][0].size
    sizex = (tile_size[0]-2) * len(G[0])
    sizey = (tile_size[1]-2) * len(G)

    L = [[0] * sizex for _ in range(sizey)]

    # paste tiles on new grid
    for y, row in enumerate(G):
        offsety = (tile_size[1]-2) * y
        for x, tile in enumerate(G[y]):
            offsetx = (tile_size[0]-2) * x
            for ty in range(1, tile.size[1]-1):
                for tx in range(1, tile.size[0]-1):
                    L[offsety + ty - 1][offsetx + tx - 1] = tile.get((tx, ty))

    # char O for monster
    g = Grid(L, chars={'.': 0, '#': 1, 'O': 2})

    # ala sparse grid, just store #
    monster = set()
    with open('monster.txt') as f:
        for y, line in enumerate(f):
            line = line.rstrip()
            for x, c in enumerate(line):
                if c == '#':
                    monster.add((x, y))

    # find monsters and paint, if we don't find a monster in an iteration,
    # rotate, after 4 rotations, flip_y and then keep rotating...
    monsters = 0
    i = 0
    while 1:
        i += 1
        for y in g.ys:
            for x in g.xs:
                try:
                    if all(g.get((x + mx, y + my)) for mx, my in monster):
                        monsters += 1

                        for mx, my in monster:
                            g.set((x + mx, y + my), 2)
                except IndexError:
                    # off the grid, just break
                    break

        # we found monsters, assuming we can only find them in one orientation,
        # we're done here...
        if monsters:
            break

        g.rotate_cw()
        if i == 4:
            g.flip_y()

    if DEBUG:
        g.print()
        print(monsters)

    # count points that are set, but not monster
    cnt = 0
    for pt in g:
        if g.get(pt) == 1:
            cnt += 1

    print(cnt)

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
