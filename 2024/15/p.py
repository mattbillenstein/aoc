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

def find_boxes_in_line(pt, move, g):
    # this handles all moves for single boxes and left/right for double boxes
    # we can just scan the line to find a hole collecting boxes along the
    # way... If we hit a wall before a hole, return None - nothing can move
    boxes = []
    while 1:
        npt = g.step(pt, move)
        c = g.getc(npt)
        if c == '#':
            return boxes, None
        elif c == '.':
            return boxes, npt
        elif c in 'O[':
            boxes.append(npt)
        pt = npt

def find_boxes_not_in_line(pt, move, g):
    # this handles up/down for 2-wide boxes, recursing for neighbor boxes above
    # and below...
    #
    # A box can move if it's clear or all the other boxes in its' way can
    # move...
    #
    # passed in pt is always [, left edge of a box

    assert g.getc(pt) == '['

    boxes = [pt]

    npt = g.step(pt, move)
    cc = g.getc(npt) + g.getc(g.step(npt, '>'))

    L = []

    if cc[0] == '#' or cc[1] == '#':
        # directly blocked
        can_move = False
    elif cc == '..':
        # directly clear
        can_move = True
    elif cc == '].':
        # recurse on left box
        L, can_move = find_boxes_not_in_line(g.step(npt, '<'), move, g)
    elif cc == '[]':
        # recurse on single in-line box
        L, can_move = find_boxes_not_in_line(npt, move, g)
    elif cc == '.[':
        # recurse on right box
        L, can_move = find_boxes_not_in_line(g.step(npt, '>'), move, g)
    elif cc == '][':
        # recurse on both left/right box
        L1, can_move_left = find_boxes_not_in_line(g.step(npt, '<'), move, g)
        L2, can_move_right = find_boxes_not_in_line(g.step(npt, '>'), move, g)
        L = L1 + L2
        can_move = can_move_left and can_move_right
    else:
        assert 0, cc

    boxes.extend(L)

    return boxes, can_move

def move_boxes(boxes, move, g):
    if not boxes:
        return

    c = g.getc(boxes[0])

    # clear existing locations
    for box in boxes:
        g.setc(box, '.')
        if c == '[':
            g.setc((box[0]+1, box[1]), '.')

    # set new locations
    for box in boxes:
        npt = g.step(box, move)
        g.setc(npt, c)
        if c == '[':
            g.setc((npt[0]+1, npt[1]), ']')

def part1(g, moves):
    g = g.copy()

    # find start point and clear the @
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

        boxes, hole = find_boxes_in_line(pt, move, g)
        if hole:
            move_boxes(boxes, move, g)
            pt = g.step(pt, move)

    if DEBUG:
        g.setc(pt, move)
        g.print()

    print(sum(_[1] * 100 + _[0] for _ in g if g.getc(_) == 'O'))


def part2(g, moves):
    # expand to double-width
    ng = Grid([['.'] * g.size[0] * 2 for _ in range(g.size[1])], g.chars)
    for pt in g:
        c = g.getc(pt)
        nc = {'.': '..', '#': '##', 'O': '[]', '@': '@.'}[c]
        ng.setc((pt[0]*2, pt[1]), nc[0])
        ng.setc((pt[0]*2+1, pt[1]), nc[1])

    g = ng

    # find start point and clear the @
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

        if move in '<>':
            boxes, hole = find_boxes_in_line(pt, move, g)
            if hole:
                move_boxes(boxes, move, g)
                pt = g.step(pt, move)
        else:
            npt = g.step(pt, move)
            c = g.getc(npt)
            if c == '.':
                pt = npt
            elif c == '#':
                # can't move
                pass
            elif c in '[]':
                spt = npt
                if c == ']':
                    spt = (npt[0]-1, npt[1])

                boxes, can_move = find_boxes_not_in_line(spt, move, g)
                if can_move:
                    move_boxes(boxes, move, g)
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
