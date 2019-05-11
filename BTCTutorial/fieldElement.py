from __future__ import annotations
from typing import Union
from functools import wraps

import unittest
import logging
#logging.basicConfig(level=logging.DEBUG)

from BTCTutorial.finiteField import FiniteField
from collections import OrderedDict


typehintunion = Union[int, 'FieldElement']



class _FieldElement(object):
    """Performs finite field math."""

    prime = 1

    def __init__(self, num: int):
        self.setNum(num)

    def _ensureFieldElementArg(func):
        """
        Converts int arguments to the class type of field1.
        Arguments:
            func:
                function to wrap.
        Returns(fn):
            wrapped function with int argument converted.
            
        """
        @wraps(func)
        def wrapped_f(field1: _FieldElement, other):
            if isinstance(other, int):
                other = field1.__class__(other)
            return func(field1, other)

        return wrapped_f


    @_ensureFieldElementArg
    def __eq__(self, other: _FieldElement) -> bool:
        return self.getNum() == other.getNum()

    @_ensureFieldElementArg
    def __ne__(self, other: _FieldElement) -> bool:
        if other is None:
            return False
        return not self == other

    @_ensureFieldElementArg
    def __lt__(self, other):
        return self.getNum() < other.getNum()

    @_ensureFieldElementArg
    def __gt__(self, other):
        return self.getNum() > other.getNum()

    @_ensureFieldElementArg
    def __add__(self, other: typehintunion) -> _FieldElement:
        num = (self.getNum() + other.getNum()) % self.getPrime()
        return self.__class__(num)

    @_ensureFieldElementArg
    def __sub__(self, other: typehintunion) -> _FieldElement:
        num = (self.getNum() - other.getNum()) % self.getPrime()
        return self.__class__(num)

    @_ensureFieldElementArg
    def __mul__(self, other: typehintunion) -> _FieldElement:
        num = (self.getNum() * other.getNum()) % self.getPrime()
        return self.__class__(num)

    @_ensureFieldElementArg
    def __pow__(self, other: typehintunion) -> _FieldElement:
        num = pow(self.getNum(), other.getNum(), self.getPrime())
        return self.__class__(num)

    @_ensureFieldElementArg
    def __floordiv__(self, other: typehintunion) -> _FieldElement:
        num = (self.getNum() * pow(other.getNum(), self.getPrime() - 2, self.getPrime())) % self.getPrime()
        return self.__class__(num)

    @_ensureFieldElementArg
    def __truediv__(self, other: typehintunion) -> _FieldElement:
        #raise Warning("True division defaults to integer division.")
        return self // other

    @_ensureFieldElementArg
    def __mod__(self, other):
        return self.getNum() % other.getNum()

    def __repr__(self):
        #return f'<{self.__class__.__name__} {self.getNum()}} >'
        return f'<{self.getNum()} f{self.getPrime()}>'

    #public methods

    def setNum(self, num):
        """Set num if it is in the proper field range."""
        if num > self.getPrime() or num < 0:
            raise ValueError(f'{num} is outside the range of 0 and self.prime')
        else:
            self.__num = num

    def getNum(self):
        return self.getNum()

    @classmethod
    def getPrime(cls):
        return cls.prime


class FiniteField(object):
    "Sets the field and returns FieldElements bounded to this field."
    instance = None
    FieldElements = OrderedDict()

    def __new__(cls, x, prime=None):
        "Returns a FieldElement"
        if prime is None:
            if len(cls.FieldElements):
                return list(cls.FieldElements.items())[-1]
            else:
                raise ValueError("FiniteField must have a prime number")
        else:
            try:
                return cls.FieldElements[prime]
            except KeyError:
                #create the enw class
                return cls.makeFieldElement(prime)

    @classmethod
    def makeFieldElement(cls, prime:int):
        """
        Makes a specific _FieldElement class with a unique prime member that has all available math operations to function in the FiniteField.
        Args:
            prime(int):
                Sets the prime number of the newly create type class.

        Returns:
            fieldElement(_fieldElement<XXX>):
                The dynamically created class locked to a prime number. All operations will happen within
                the finite field.
        """
        fieldElement = type(f"FieldElement{prime}", (), dict(_FieldElement.__dict__))
        fieldElement.prime = prime
        return fieldElement


    def __repr__(self):
        return f'<PrimeField{self.prime}>'

class FiniteElement(FiniteField):
    def __new__(cls, x, prime=None):
        "Returns a FieldElement"
        return super().__new__(cls, x, prime=prime)(x)






class FieldElementTest(unittest.TestCase):

    def test_makeElement(self):

        FE17 = FiniteField.makeFieldElement(17)
        b = FE17(5)
        c = FE17(11)
        d = FE17(16)
        self.assertEqual(b+c, d)

    def test_ne(self):
        FE31 = FiniteField.makeFieldElement(31)
        a = FE31(2)
        b = FE31(2)
        c = FE31(15)
        self.assertEqual(a, b)
        self.assertTrue(a != c)
        self.assertFalse(a != a)

    def test_eq(self):
        FE19 = FiniteField.makeFieldElement(19)
        a = FE19(5)
        b = FE19(5)
        c = FE19(6)
        self.assertEqual(a, b)
        self.assertTrue(a == b)
        self.assertFalse(a == c)

    def test_add(self):
        FE17 = FiniteField.makeFieldElement(17)
        a = FE17(6)
        b = FE17(7)
        c = FE17(13)
        self.assertEqual(a + b, c)
        self.assertEqual(a + 7, c)

    def test_sub(self):
        FE17 = FiniteField.makeFieldElement(17)
        a = FE17(15)
        b = FE17(5)
        c = FE17(10)
        self.assertEqual(a - b, c)
        self.assertEqual(a - 5, c)

    def test_mul(self):
        FE17 = FiniteField.makeFieldElement(17)
        a = FE17(2)
        b = FE17(3)
        c = FE17(6)
        self.assertEqual(a*b, c)
        self.assertEqual(a*3, c)

    def test_pow(self):
        a = FE17(2)
        b = FE17(3)
        c = FE17(8)
        self.assertEqual(a**b, c)
        self.assertEqual(a**3, c)

    def test_floordiv(self):
        a = FE17(15)
        b = FE17(5)
        c = FE17(3)
        self.assertEqual(a // b, c)
        self.assertEqual(a // 5, c)

    def test_truediv(self):
        a = FE17(15)
        b = FE17(5)
        c = FE17(3)
        self.assertEqual(a / b, c)
        self.assertEqual(a / 5, c)

    def test_FiniteField(self):
        #todo: impliment this
        pass

if __name__ == "__main__":

    unittest.main()
