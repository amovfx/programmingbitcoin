import unittest

from BTCTutorial.finiteField import FiniteField

class FieldElementTest(unittest.TestCase):

    def test_makeElement(self):

        FE17 = FiniteField(17)
        b = FE17(5)
        c = FE17(11)
        d = FE17(16)
        self.assertEqual(b+c, d)

    def test_ne(self):
        FE31 = FiniteField(31)
        a = FE31(2)
        b = FE31(2)
        c = FE31(15)
        self.assertEqual(a, b)
        self.assertTrue(a != c)
        self.assertFalse(a != a)

    def test_eq(self):
        FE19 = FiniteField(19)
        a = FE19(5)
        b = FE19(5)
        c = FE19(6)
        self.assertEqual(a, b)
        self.assertTrue(a == b)
        self.assertFalse(a == c)

    def test_add(self):
        FE17 = FiniteField(17)
        a = FE17(6)
        b = FE17(7)
        c = FE17(13)
        self.assertEqual(a + b, c)
        self.assertEqual(a + 7, c)

    def test_sub(self):
        FE17 = FiniteField(17)
        a = FE17(15)
        b = FE17(5)
        c = FE17(10)
        self.assertEqual(a - b, c)
        self.assertEqual(a - 5, c)

    def test_mul(self):
        FE17 = FiniteField(17)
        a = FE17(2)
        b = FE17(3)
        c = FE17(6)
        self.assertEqual(a*b, c)
        self.assertEqual(a*3, c)

    def test_pow(self):
        FE17 = FiniteField(17)
        a = FE17(2)
        b = FE17(3)
        c = FE17(8)
        self.assertEqual(a**b, c)
        self.assertEqual(a**3, c)

    def test_floordiv(self):
        FE17 = FiniteField(17)
        a = FE17(15)
        b = FE17(5)
        c = FE17(3)
        self.assertEqual(a // b, c)
        self.assertEqual(a // 5, c)

    def test_truediv(self):
        FE17 = FiniteField(17)
        a = FE17(15)
        b = FE17(5)
        c = FE17(3)
        self.assertEqual(a / b, c)
        self.assertEqual(a / 5, c)


if __name__ == "__main__":

    unittest.main()