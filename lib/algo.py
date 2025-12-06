def find_repeating(seq, brk=1000000):
    length = len(seq)
    max_run = 0
    run_pos = None
    for i1 in range(length):
        i2 = i1 + 1

        item1 = grid[i1]
        while i2 < length:
            item2 = grid[i2]
            if item1 == item2:
                break
            i2 += 1

        tmp = (i1, i2)
        run = 0
        while i1 < length and i2 < length:
            item1 = grid[i1]
            item2 = grid[i2]
#            print(i1, i2, item1, item2)
            if item1 != item2:
                break
            run += 1
            i1 += 1
            i2 += 1

        if run > max_run:
            max_run = run
            run_pos = tmp
#            print(y_run, max_run)

            # if we run off the end, that's fine, but after brk, stop
            # looking...
            if max_run > brk:
                break

    return run_pos, max_run

def shoelace(pts):
    # shoelace formula - area of polygon given perimeter points
    assert pts[0] == pts[-1]
    return sum((a[0]*b[1]-b[0]*a[1]) for a,b in zip(pts, pts[1:])) // 2

def rect_perimeter(pts):
    assert pts[0] == pts[-1]
    return sum(abs(a[0] - b[0]) + abs(a[1] - b[1]) for a, b in zip(pts, pts[1:]))

def picks_shoelace_area(pts, include_border=True):
    '''
    Couple explanations:

    Picks Theorem: A = i + b/2 - 1
        This is the interior (zero-width border) area

        For area with a border, basic algebra lets us solve: i = A - b/2 + 1,
        which then implies: i + b = A + b/2 + 1

        Geometrically, Picks will include half the border - 1, so we add back
        half the border + 1 to get the full area

    ------

    Calculating i + b from the Pick's theorem, using the Shoelace formula to
    calculate the area

    i + b = A + b/2 + 1

    b (the number of integer points on the shape's boundary) is just our
    shape's perimeter, which we can easily calculate.

    We can use the Shoelace formula to calculate A, but that's not the area we
    are looking for, as it is only the area inside the shape, not counting the
    boundaries.

    The actual area we are looking for is i + b, which is the number of integer
    points within and on the shape's boundary. As we already know A and b, we
    only have to find i, which is, after transforming the Pick's to look for
    it, i = A - b/2 + 1. We add b to both sides of the equation, and what we
    get is i + b = A + b/2 + 1, which is our answer.
    '''

    # pts should close a loop
    assert pts[0] == pts[-1]

    # with zero width border, this is effectively the interior + half the border
    i = shoelace(pts)           # includes half the boundary
    b = rect_perimeter(pts)     # compute boundary, add half back plus 1/4 in each corner?

    if include_border:
        area = i + b//2 + 1
    else:
        area = i - b//2 + 1

    return area

def cramers_rule(A, B):
    if len(A) == 3:
        return cramers_rule_3(A, B)
    return cramers_rule_2(A, B)

def det2(matrix):
    a, b = matrix[0]
    c, d = matrix[1]
    return a*d - b*c

def cramers_rule_2(A, B):
    """
    Solves a system of linear equations using Cramer's Rule.

    AX = B

    D = det(A)
    Dx = det([B, A1])
    Dy = det([A0, B])
    x = Dx / D
    y = Dy / D
    """

    D = det2(A)
    if D == 0:
        raise ValueError("Determinant of coefficient matrix is zero, Cramer's rule cannot be applied.")

    Dx = det2([[B[0], A[0][1]], [B[1], A[1][1]]])
    Dy = det2([[A[0][0], B[0]], [A[1][0], B[1]]])

    x = Dx / D
    y = Dy / D

    return (x, y)

def det3(matrix):
    """Calculates the determinant of a 3x3 matrix."""
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)

def cramers_rule_3(A, B):
    D = det3(A)
    if D == 0:
        raise ValueError("Determinant of coefficient matrix is zero, Cramer's rule cannot be applied.")

    Dx = det3([ [B[_], A[_][1], A[_][2]] for _ in range(3) ])
    Dy = det3([ [A[_][0], B[_], A[_][2]] for _ in range(3) ])
    Dz = det3([ [A[_][0], A[_][1], B[_]] for _ in range(3) ])

    x = Dx / D
    y = Dy / D
    z = Dz / D

    return (x, y, z)

def merge_ranges(ranges):
    # merge a list of 2-tuples representing ranges
    ranges = sorted(ranges)
    last = None
    a1, a2 = ranges[0]
    assert a1 <= a2
    for b1, b2 in ranges[1:]:
        assert b1 <= b2
        if b1 <= a1 <= b2 or b1 <= a2 <= b2 or a1 <= b1 <= a2 or a1 <= b2 <= a2:
            a1, a2 = min(a1, b1), max(a2, b2)
        else:
            last = (a1, a2)
            yield last
            a1, a2 = b1, b2

    if (a1, a2) != last:
        yield (a1, a2)
