from __future__ import annotations
from typing import Union
from functools import wraps

from math import sqrt
from itertools import count, islice

import unittest

from .finiteField import FiniteField


class FieldElement:
    """
    An object to do finite field element math.
    """

    typehintunion = Union[int, 'FieldElement']

    def __init__(self, num: int, prime=None):

        if prime is not None:
            """Set the prime value of the FiniteField singleton."""
            finiteField = FiniteField(prime)
        else:
            #warning you are creating a default field.
            finiteField = FiniteField()

        self._prime = finiteField.getPrime()


        #maybe auto convert?
        if num > self._prime or num < 0:
            raise ValueError(f'{num} is outside the range of 0 and self.prime')
        else:
            self._num = num


    def _ensureField(func):
        """
        Wrapper for class functions to check if _prime variable matches. This also converts ints to FIniteFIelds
        :return:
        """
        @wraps(func)
        def wrapped(field1: FieldElement, other):

            if isinstance(other, int):
                other = FieldElement(other, field1._prime)
            elif isinstance(other, FieldElement):
                if field1._prime != other._prime:
                    raise ValueError(f'Fields must match. {field1._prime} != {other._prime}')
            else:
                raise ValueError("Second argument must be an int or a FieldElement.")

            return func(field1, other)
        return wrapped



    @_ensureField
    def __eq__(self, other: FieldElement) -> bool:
        return self._num == other._num and self._prime == other._prime

    @_ensureField
    def __ne__(self, other: FieldElement) -> bool:
        if other is None:
            return False
        return not self == other

    @_ensureField
    def __add__(self, other: typehintunion) -> FieldElement:
        num = (self._num + other._num) % self._prime
        return self.__class__(num, self._prime)

    @_ensureField
    def __sub__(self, other: typehintunion) -> FieldElement:
        num = (self._num - other._num) % self._prime
        return self.__class__(num, self._prime)

    @_ensureField
    def __mul__(self, other: typehintunion) -> FieldElement:
        num = (self._num * other._num) % self._prime
        return self.__class__(num, self._prime)

    @_ensureField
    def __pow__(self, other: typehintunion) -> FieldElement:
        num = pow(self._num, other._num, self._prime)
        return self.__class__(num, self._prime)

    @_ensureField
    def __floordiv__(self, other: typehintunion) -> FieldElement:
        num = (self._num * pow(other._num, self._prime - 2, self._prime)) % self._prime
        return self.__class__(num, self._prime)

    @_ensureField
    def __truediv__(self, other: typehintunion) -> FieldElement:
        #raise Warning("True division defaults to integer division.")
        return self // other

    def __repr__(self):
        return f'<{self.__class__.__name__} {self._num} f{self._prime} >'


class FieldElementTest(unittest.TestCase):

    def test_ne(self):
        a = FieldElement(2, 31)
        b = FieldElement(2, 31)
        c = FieldElement(15, 31)
        self.assertEqual(a, b)
        self.assertTrue(a != c)
        self.assertFalse(a != a)

    def test_eq(self):
        a = FieldElement(5, 19)
        b = FieldElement(5,19)
        c = FieldElement(6, 19)
        self.assertEqual(a, b)
        self.assertTrue(a == b)
        self.assertFalse(a == c)

    def test_add(self):
        a = FieldElement(6, 17)
        b = FieldElement(7, 17)
        c = FieldElement(13, 17)
        self.assertEqual(a + b, c)
        self.assertEqual(a + 7, c)

    def test_sub(self):
        a = FieldElement(15, 17)
        b = FieldElement(5, 17)
        c = FieldElement(10, 17)
        self.assertEqual(a - b, c)
        self.assertEqual(a - 5, c)

    def test_mul(self):
        a = FieldElement(2, 17)
        b = FieldElement(3, 17)
        c = FieldElement(6, 17)
        self.assertEqual(a*b, c)
        self.assertEqual(a*3, c)

    def test_pow(self):
        a = FieldElement(2, 17)
        b = FieldElement(3, 17)
        c = FieldElement(8, 17)
        self.assertEqual(a**b, c)
        self.assertEqual(a**3, c)

    def test_floordiv(self):
        a = FieldElement(15, 17)
        b = FieldElement(5, 17)
        c = FieldElement(3, 17)
        self.assertEqual(a // b, c)
        self.assertEqual(a // 5, c)

    def test_truediv(self):
        a = FieldElement(15, 17)
        b = FieldElement(5, 17)
        c = FieldElement(3, 17)
        self.assertEqual(a / b, c)
        self.assertEqual(a / 5, c)

if __name__ == "__main__":
    unittest.main()
