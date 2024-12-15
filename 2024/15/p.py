#!/usr/bin/env pypy3

import sys

from grid import Grid

DEBUG = sys.argv.count('-v')

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    idx = lines.index('')
    g = Grid(lines[:idx], {'.': 0, '#': 1, "O": 2, "<": 3, "^": 4, ">": 5, "v": 6, '[': 7, ']': 8})
    moves = ''.join(lines[idx+1:])
    return g, moves

def find_hole(pt, dir, g):
    boxes = []
    while 1:
        npt = g.step(pt, dir)
        c = g.getc(npt)
        if c == '#':
            return []
        elif c == '.':
            boxes.append(npt)
            return boxes
        elif c == 'O':
            boxes.append(npt)
        pt = npt

def part1(g, moves):
    g = g.copy()

    for pt in g:
        if g.getc(pt) == '@':
            break

    g.setc(pt, '.')

    if DEBUG:
        g.print()

    for move in moves:
        to_move = find_hole(pt, move, g)
        if to_move:
            for npt in to_move:
                g.setc(npt, 'O')
            g.setc(pt, '.')
            pt = g.step(pt, move)
            g.setc(pt, '.')

    if DEBUG:
        g.setc(pt, move)
        g.print()

    print(sum(_[1] * 100 + _[0] for _ in g if g.getc(_) == 'O'))

def find_hole2(pt, dir, g):
    boxes = []
    while 1:
        npt = g.step(pt, dir)
        c = g.getc(npt)
        if c == '#':
            return boxes, None
        elif c == '.':
            return boxes, npt
        elif c == '[':
            boxes.append(npt)
        elif c == ']':
            boxes.append((npt[0]-1, npt[1]))
        pt = npt

def find_boxes(pt, dir, g):
    # recursively find boxes until we either can't move or every box can move
    boxes = []
    assert g.getc(pt) == '['
    npt = g.step(pt, dir)
    c = g.getc(npt)
    if c == '[':
        # box directly above box
        boxes.extend(find_boxes(npt, dir, g))
        boxes.append((pt, all(_[1] for _ in boxes)))
    elif c == ']':
        boxes.extend(find_boxes((npt[0]-1, npt[1]), dir, g))

        npt2 = (npt[0]+1, npt[1])
        c2 = g.getc(npt2)
        if c2 == '.':
            boxes.append((pt, True))
        elif c2 == '#':
            boxes.append((pt, False))
        elif c2 == '[':
            boxes.extend(find_boxes(npt2, dir, g))
            boxes.append((pt, all(_[1] for _ in boxes)))
    elif c == '.':
        npt2 = (npt[0]+1, npt[1])
        c2 = g.getc(npt2)
        if c2 == '.':
            boxes.append((pt, True))
        elif c2 == '#':
            boxes.append((pt, False))
        elif c2 == '[':
            boxes.extend(find_boxes(npt2, dir, g))
            boxes.append((pt, all(_[1] for _ in boxes)))
    elif c == '#':
        boxes.append((pt, False))
            
    return boxes


def part2(g, moves):
    ng = Grid([['.'] * g.size[0] * 2 for _ in range(g.size[1])], g.chars)
    for pt in g:
        c = g.getc(pt)
        nc = {'.': '..', '#': '##', 'O': '[]', '@': '@.'}[c]
        ng.setc((pt[0]*2, pt[1]), nc[0])
        ng.setc((pt[0]*2+1, pt[1]), nc[1])

    g = ng

    for pt in g:
        if g.getc(pt) == '@':
            break
    g.setc(pt, '.')

    if DEBUG:
        g.print()

    for move in moves:
        if DEBUG > 1:
            print()
            print(pt, move)
            g.setc(pt, move)
            g.print()
            g.setc(pt, '.')

        npt = g.step(pt, move)
        c = g.getc(npt)
        if c == '.':
            pt = npt
        elif c == '#':
            # can't move
            pass
        elif move in '^v' and c in '[]':
            spt = npt
            if c == ']':
                spt = (npt[0]-1, npt[1])
            boxes = find_boxes(spt, move, g)

            # [(pt, bool can move), ...]
            if all(_[1] for _ in boxes):
                # move the boxes
                dy = -1 if move == '^' else 1

                # discard can-move flag
                boxes = [_[0] for _ in boxes]

                # clear current positions
                for box in boxes:
                    g.setc(box, '.')
                    g.setc((box[0]+1, box[1]), '.')

                # set new positions
                for box in boxes:
                    g.setc((box[0], box[1]+dy), '[')
                    g.setc((box[0]+1, box[1]+dy), ']')

                pt = npt
        elif move in '<>' and c in '[]':
            boxes, hole = find_hole2(pt, move, g)

            if hole:
                # clear
                for box in boxes:
                    g.setc(box, '.')
                    g.setc((box[0]+1, box[1]), '.')

                # set
                for box in boxes:
                    if move == '<':
                        g.setc((box[0]-1, box[1]), '[')
                        g.setc(box, ']')
                    elif move == '>':
                        g.setc((box[0]+1, box[1]), '[')
                        g.setc((box[0]+2, box[1]), ']')

                g.setc(npt, '.')
                pt = npt
        else:
            assert 0, c

    if DEBUG:
        g.setc(pt, move)
        g.print()

    print(sum(_[1] * 100 + _[0] for _ in g if g.getc(_) == '['))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
