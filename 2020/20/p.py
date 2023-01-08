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
    # edge to tile id and face + reversed
    edges = defaultdict(list)
    for tile_id, tile in tiles.items():
        edges[tile.edge_Tm].append(tile_id)
        edges[tile.edge_Bm].append(tile_id)
        edges[tile.edge_Lm].append(tile_id)
        edges[tile.edge_Rm].append(tile_id)

    corners = defaultdict(int)
    for eid, L in edges.items():
        if len(L) == 1:
            corners[L[0]] += 1

    corners = [k for k, v in corners.items() if v == 2]

    return edges, corners

def part1(tiles):
    edges, corners = run(tiles)
    print(math.prod(corners))

def other_tile_id(tile_id, edge, edges):
    return [_ for _ in edges[edge] if _ != tile_id][0]

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

                T = tiles[other_tile_id(U.id, U.edge_Bm, edges)]
                G[row][col] = T

                while T.edge_Tm != U.edge_Bm:
                    T.rotate_cw()

                if T.edge_T != U.edge_B:
                    T.flip_y()

                assert len(edges[T.edge_Lm]) == 1  # faces out
            else:
                # stitch to left
                L = G[row][col-1]

                T = tiles[other_tile_id(L.id, L.edge_Rm, edges)]
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

    g = Grid(L)
    g.print()

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(data)
    if '2' in sys.argv:
        part2(data)

if __name__ == '__main__':
    main()
