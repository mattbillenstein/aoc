#!/usr/bin/env pypy3

import sys

from grid import Grid

DEBUG = sys.argv.count('-v')

def parse_input():
    lines = [_.strip('\r\n') for _ in sys.stdin]
    idx = lines.index('')
    g = Grid(lines[:idx], {c: i for i, c in enumerate('.#O@<^>v[]')})
    moves = ''.join(lines[idx+1:])
    return g, moves

def find_boxes(pt, move, g):
    # Return boxes and if we can move when moving from pt, recurse on relevant
    # points in the same direction until we hit a hole or wall...
    npt = g.step(pt, move)
    c = g.getc(npt)

    assert c in '.#O[]', c

    if c == '.':
        return [], True
    if c == '#':
        return [], False
    if c == 'O':
        L, can_move = find_boxes(npt, move, g)
        return [npt] + L, can_move

    # double width boxes, different stuff depending on move direction...
    if move in 'v^':
        if c == '[':
            npt2 = g.step(npt, '>')
        elif c == ']':
            npt2 = g.step(npt, '<')
        L1, can_move1 = find_boxes(npt, move, g)
        L2, can_move2 = find_boxes(npt2, move, g)
        return [npt if c == '[' else npt2] + L1 + L2, can_move1 and can_move2

    # <> skip over second half of box
    npt2 = g.step(npt, move)
    L, can_move = find_boxes(g.step(npt, move), move, g)
    return [npt if c == '[' else npt2] + L, can_move

    assert 0, c

def move_boxes(boxes, move, g):
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

def part(g, moves):
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

        boxes, can_move = find_boxes(pt, move, g)
        if can_move:
            if boxes:
                move_boxes(boxes, move, g)
            pt = g.step(pt, move)

    if DEBUG:
        print()
        g.setc(pt, move)
        g.print()

    return sum(_[1] * 100 + _[0] for _ in g if g.getc(_) in 'O[')

def part1(g, moves):
    print(part(g, moves))

def part2(g, moves):
    # expand to double-width
    ng = Grid([['.'] * g.size[0] * 2 for _ in range(g.size[1])], g.chars)
    for pt in g:
        c = g.getc(pt)
        nc = {'.': '..', '#': '##', 'O': '[]', '@': '@.'}[c]
        ng.setc((pt[0]*2, pt[1]), nc[0])
        ng.setc((pt[0]*2+1, pt[1]), nc[1])

    print(part(ng, moves))

def main():
    data = parse_input()
    if '1' in sys.argv:
        part1(*data)
    if '2' in sys.argv:
        part2(*data)

if __name__ == '__main__':
    main()
