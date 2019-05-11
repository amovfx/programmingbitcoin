from __future__ import annotations
from typing import Union
from functools import wraps


import logging
#logging.basicConfig(level=logging.DEBUG)



typehintunion = Union[int, 'FieldElement']


class FiniteFieldObject(object):
    """Object for all finite element derivitives to inherit from."""
    def __init__(self, bounds):
        self._bounds = bounds

    def getBounds(self):
        return self._bounds

class FiniteFieldElement(object):

    """Base class for FIniteField Factory to create FInite Element objects."""

    _bounds = None
    @classmethod
    def getBounds(cls):
        return cls._bounds

    @classmethod
    def setBounds(cls, bounds):
        cls._bounds = bounds

class FiniteField(object):
    """
    This field object sets the bounds of the finite field and is also a factory
    for element class appropriate to that field.
    """

    class _FieldElement(FiniteFieldElement):
        """An element of the finite field. This object provides the mathematical
        operations for the field elements."""

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
            def wrapped_f(field1: FiniteFieldObject, other):
                if isinstance(other, int):
                    other = field1.__class__(other)
                return func(field1, other)

            return wrapped_f

        @_ensureFieldElementArg
        def __eq__(self, other: FiniteField._FieldElement) -> bool:
            return self.getNum() == other.getNum()

        @_ensureFieldElementArg
        def __ne__(self, other: FiniteField._FieldElement) -> bool:
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
        def __add__(self, other: typehintunion) -> FiniteField._FieldElement:
            num = (self.getNum() + other.getNum()) % self.getPrime()
            return self.__class__(num)

        @_ensureFieldElementArg
        def __sub__(self, other: typehintunion) -> FiniteField._FieldElement:
            num = (self.getNum() - other.getNum()) % self.getPrime()
            return self.__class__(num)

        @_ensureFieldElementArg
        def __mul__(self, other: typehintunion) -> FiniteField._FieldElement:
            num = (self.getNum() * other.getNum()) % self.getPrime()
            return self.__class__(num)

        @_ensureFieldElementArg
        def __pow__(self, other: typehintunion) -> FiniteField._FieldElement:
            num = pow(self.getNum(), other.getNum(), self.getPrime())
            return self.__class__(num)

        @_ensureFieldElementArg
        def __floordiv__(self, other: typehintunion) -> FiniteField._FieldElement:
            num = (self.getNum() * pow(other.getNum(), self.getPrime() - 2, self.getPrime())) % self.getPrime()
            return self.__class__(num)

        @_ensureFieldElementArg
        def __truediv__(self, other: typehintunion) -> FiniteField._FieldElement:
            # raise Warning("True division defaults to integer division.")
            return self // other

        @_ensureFieldElementArg
        def __mod__(self, other):
            return self.getNum() % other.getNum()

        def __repr__(self):
            # return f'<{self.__class__.__name__} {self.getNum()}} >'
            return f'<FieldElement {self.getNum()} f{self.getPrime()}>'

        # public methods

        def setNum(self, num):
            """Set num if it is in the proper field range."""
            if num > self.getPrime() or num < 0:
                raise ValueError(f'{num} is outside the range of 0 and {self.getPrim()}')
            else:
                self._num = num

        def getNum(self):
            return self._num

        @classmethod
        def getPrime(cls):
            return cls.getBounds()

    def __init__(self, prime):
        self._bounds = prime

    @property
    def Element(self):

        """This returns a class with bounds set. All instances of this object will work correctly together.

        Returns(FiniteFieldElement):
            A dynamicaly created class so all instances of this class can share a unique bound attribute.
            This allows to create multiple objects in different fields.

        """

        fieldElement = type(f"FieldElement{self._bounds}", (FiniteFieldElement, object), dict(self._FieldElement.__dict__))
        fieldElement.setBounds(self._bounds)
        return fieldElement

    def __call__(self, num):
        """Quick method to return an instanced FieldElement"""
        return self.Element(num)









