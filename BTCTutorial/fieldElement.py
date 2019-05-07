from __future__ import annotations
from typing import Union
from functools import wraps

from math import sqrt
from itertools import count, islice

import unittest
import logging
#logging.basicConfig(level=logging.DEBUG)

from BTCTutorial.finiteField import FiniteField


class FieldElement:
    """
    An object to do finite field element math.
    """

    typehintunion = Union[int, 'FieldElement']

    def __init__(self, num: int, prime=None):

        self._ensureFiniteField()
        self.setNum(num)
        if prime is not None:
            print(f"setting prime: {prime}")
            self.setPrime(prime)
        else:
            self._prime = None


    def _ensureFiniteField(self):
        logging.debug("Creating FieldElement.",exc_info=True)
        if FiniteField.instance == None:
            logging.debug("Creating FiniteField", exc_info=True)
            FiniteField()
        else:
            logging.debug(f"Element in {FiniteField()}")

    def _ensureFieldElementArg(func):
        """
        Wrapper for class functions to check if _prime variable matches. This also converts ints to FIniteFIelds
        :return:
        """
        @wraps(func)
        def wrapped(field1: FieldElement, other):

            if isinstance(other, int):
                other = FieldElement(other)
            return func(field1, other)
        return wrapped


    @_ensureFieldElementArg
    def __eq__(self, other: FieldElement) -> bool:
        return (self._num == other.getNum())

    @_ensureFieldElementArg
    def __ne__(self, other: FieldElement) -> bool:
        if other is None:
            return False
        return not self == other

    @_ensureFieldElementArg
    def __lt__(self, other):
        return (self._num < other._num)

    @_ensureFieldElementArg
    def __gt__(self, other):
        return (self._num > other._num)

    @_ensureFieldElementArg
    def __add__(self, other: typehintunion) -> FieldElement:
        num = (self._num + other._num) % self.getPrime()
        return self.__class__(num, self.getPrime())

    @_ensureFieldElementArg
    def __sub__(self, other: typehintunion) -> FieldElement:
        num = (self._num - other._num) % self.getPrime()
        return self.__class__(num, self.getPrime())

    @_ensureFieldElementArg
    def __mul__(self, other: typehintunion) -> FieldElement:
        num = (self._num * other._num) % self.getPrime()
        return self.__class__(num, self.getPrime())

    @_ensureFieldElementArg
    def __pow__(self, other: typehintunion) -> FieldElement:
        num = pow(self._num, other._num, self.getPrime())
        return self.__class__(num, self.getPrime())

    @_ensureFieldElementArg
    def __floordiv__(self, other: typehintunion) -> FieldElement:
        num = (self._num * pow(other._num, self.getPrime() - 2, self.getPrime())) % self.getPrime()
        return self.__class__(num, self.getPrime())

    @_ensureFieldElementArg
    def __truediv__(self, other: typehintunion) -> FieldElement:
        #raise Warning("True division defaults to integer division.")
        return self // other

    @_ensureFieldElementArg
    def __mod__(self, other):
        return self._num % other._num

    def __repr__(self):
        return f'<{self.__class__.__name__} {self._num} f{FiniteField().getPrime()} >'

    #public methods

    def setNum(self, num):
        # maybe auto convert?
        if num > self.getPrime() or num < 0:
            raise ValueError(f'{num} is outside the range of 0 and self.prime')
        else:
            self._num = num

    def getNum(self):
        return self._num

    def setPrime(self, prime):
        self._prime = prime

    def getPrime(self):
        if self._prime is None:
            return FiniteField().getPrime()
        else:
            return self._prime


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
        FieldElement(17)
        a = FieldElement(6)
        b = FieldElement(7)
        c = FieldElement(13)
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

    def test_FiniteField(self):
        #todo: impliment this
        pass

if __name__ == "__main__":

    unittest.main()
