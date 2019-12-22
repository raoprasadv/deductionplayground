import unittest
import deduction.basics as b

class PointTest(unittest.TestCase):
    def test_var0(self):
        v = b.Var(1)
        assert str(v) == "Var(1)"