#Copyright dwetfyw

from __future__ import annotations

from math import sqrt
from itertools import count, islice

import unittest

#todo annotate with comments

class FiniteField:
    """Finite Field is a Singleton to contain a prime value to limit the field for future classes."""
    class __FiniteField:
        def __init__(self, prime):
            self.setPrime(prime)

        def __repr__(self):
            return f"<FiniteField ({self.getPrime()}) >"

        def getPrime(self):
            return self._prime

        def setPrime(self, prime):
            """Filter for prime numbers """
            if prime > 1 and all(prime % i for i in islice(count(2), int(sqrt(prime) - 1))):
                self._prime = prime
            else:
                raise ValueError(f'{prime} is not prime')


    instance = None

    def __new__(cls, prime=None):


        """Create singleton"""
        if FiniteField.instance is None:
            if prime is None:
                Warning("prime value defaulting to 17.")
                prime = 17
            FiniteField.instance = FiniteField.__FiniteField(prime)
        else:
            FiniteField.instance.setPrime(prime)
        return FiniteField.instance



    def __getttr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)



class FiniteFieldTest(unittest.TestCase):
    """Various unit testing for the FiniteField class."""

    def test_prime(self):
        #print ("Testing non prime")
        with self.assertRaises(ValueError):
            nonPrimeField = FiniteField(16)

    def test_functions(self):
        primeField = FiniteField(17)
        self.assertEqual(17, primeField._prime)
        self.assertEqual(17, primeField.getPrime())

    def test_Simpleton(self):
        primeField = FiniteField(23)
        self.assertNotEqual(17, primeField.getPrime())

    def test_NoDefault(self):
        primeField = FiniteField()
        print (primeField.getPrime())

if __name__ == "__main__":
    unittest.main()