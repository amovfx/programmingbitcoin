from __future__ import annotations
from functools import wraps


class FiniteField:
    def __init__(self, num: int, prime: int):
        self._num = num
        self._prime = prime


    def _ensureField(func):
        @wraps(func)
        def wrapped(field1: FiniteField, field2: FiniteField):
            if field1._prime != field2._prime:
                raise ValueError(f'Fields must match. {field1._prime} != {field2._prime}')
            return func(field1, field2)
        return wrapped

    @_ensureField
    def __add__(self, other: FiniteField) -> FiniteField:
        num = (self._num + other._num) % self._prime
        return self.__class__(num, self._prime)

    @_ensureField
    def __mul__(self, other: FiniteField) -> FiniteField:
        num = (self._num * other._num) % self._prime
        return self.__class__(num, self._prime)

    @_ensureField
    def __pow__(self, other: FiniteField) -> FiniteField:
        num = pow(self._num, other._num, self._prime)
        return self.__class__(num, self._prime)

    @_ensureField
    def __floordiv__(self, other: FiniteField) -> FiniteField:
        num = (self._num * pow(other._num, self._prime - 2, self._prime)) % self._prime
        return self.__class__(num, self._prime)



    def __repr__(self):
        return f'FieldElement_{self._prime}({self._num})'



a = FiniteField(13,19)
b = FiniteField(24,19)
c = a+b
print (a._num)
print (c)
print (c._num)
print ((13+24)%19)