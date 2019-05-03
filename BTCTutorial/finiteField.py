from __future__ import annotations
from typing import Union
from functools import wraps

from math import sqrt
from itertools import count, islice

import unittest

#todo annotate with comments

class FiniteField:
    class __FiniteField:
        def __init__(self, prime):

            self.prime = prime

        def __repr__(self):
            return f"<FiniteField ({self.prime}) >"



    instance = None

    def __new__(cls, prime=17):
        if prime > 1 and all(prime % i for i in islice(count(2), int(sqrt(prime) - 1))):
            if not FiniteField.instance:
                FiniteField.instance = FiniteField.__FiniteField(prime)
            return FiniteField.instance
        else:
            raise ValueError(f'{prime} is not prime')


    def __getttr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        #todo: add check for setting prime
        return setattr(self.instance, name)



class FiniteFieldTest(unittest.TestCase):

    def test_prime(self):
        with self.assertRaises(ValueError):
            nonPrimeField = FiniteField(16)
        primeField = FiniteField(17)
        self.assertEqual(17, primeField.prime)

