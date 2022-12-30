# -*- coding: utf-8 -*-

__author__ = """Shlomi Fish"""
__email__ = 'shlomif@shlomifish.org'
__version__ = '0.1.0'


class ChineseRemainderConstructor:
    """Synopsis:

from modint import ChineseRemainderConstructor, chinese_remainder

cr = ChineseRemainderConstructor([2, 5])
assert cr.rem([1, 0]) == 5
assert cr.rem([0, 3]) == 8

# Convenience function
assert chinese_remainder([2, 3, 7], [1, 2, 3]) == 17
    """
    def __init__(self, bases):
        """Accepts a list of integer bases."""
        self._bases = bases
        p = 1
        for x in bases:
            p *= x
        self._prod = p
        self._inverses = [p//x for x in bases]
        self._muls = [inv * self.mul_inv(inv, base) for base, inv
                      in zip(self._bases, self._inverses)]

    def rem(self, mods):
        """Accepts a list of corresponding modulos for the bases and
        returns the accumulated modulo.
        """
        ret = 0
        for mul, mod in zip(self._muls, mods):
            ret += mul * mod
        return ret % self._prod

    def mul_inv(self, a, b):
        """Internal method that implements Euclid's modified gcd algorithm.
        """
        initial_b = b
        x0, x1 = 0, 1
        if b == 1:
            return 1
        while a > 1:
            div, mod = divmod(a, b)
            a, b = b, mod
            x0, x1 = x1 - div * x0, x0
        return (x1 if x1 >= 0 else x1 + initial_b)


def chinese_remainder(n, mods):
    """Convenience function that calculates the chinese remainder directly."""
    return ChineseRemainderConstructor(n).rem(mods)


def invmod(base, mod):
    """
    invmod(base=base, mod=mod) * mod % base == 1

    Modular multiplicative Inverse convenience function. See:

    https://stackoverflow.com/questions/4798654/

    (Added in v0.4.0)
    """
    return chinese_remainder([base, mod], [1, 0]) // mod
