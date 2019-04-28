from __future__ import annotations
from typing import Union
from functools import wraps

from math import sqrt
from itertools import count, islice

import unittest



class FieldElement:
    """
    An object to do finite field math.
    """

    typehint = Union[int, FieldElement]

    def __init__(self, num: int, prime: int):

        if prime > 1 and all(prime % i for i in islice(count(2), int(sqrt(prime) - 1))):
            self._prime = prime
        else:
            raise ValueError(f'{prime} is not a prime number.')

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
    def __add__(self, other: typehint) -> FieldElement:
        num = (self._num + other._num) % self._prime
        return self.__class__(num, self._prime)

    @_ensureField
    def __sub__(self, other: typehint) -> FieldElement:
        num = (self._num - other._num) % self._prime
        return self.__class__(num, self._prime)

    @_ensureField
    def __mul__(self, other: typehint) -> FieldElement:
        num = (self._num * other._num) % self._prime
        return self.__class__(num, self._prime)

    @_ensureField
    def __pow__(self, other: typehint) -> FieldElement:
        num = pow(self._num, other._num, self._prime)
        return self.__class__(num, self._prime)

    @_ensureField
    def __floordiv__(self, other: typehint) -> FieldElement:
        num = (self._num * pow(other._num, self._prime - 2, self._prime)) % self._prime
        return self.__class__(num, self._prime)

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




A = FieldElement(3,19)
A
B = FieldElement(18, 19)
A ** 2