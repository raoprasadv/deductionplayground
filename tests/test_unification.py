import unittest
import deduction.basics as b


def foo():
    raise b.UnificationFailure(1, 2, {})

class MyTestCase(unittest.TestCase):

    def test_something(self):
        s = ""
        try:
            foo()
        except b.UnificationFailure as e:
            s = repr(e)
        self.assertEqual(s, "UnificationFailure(1, 2, {})")

    def test_constantconstant(self):
        t1 = 1
        t2 = 1
        assert b.unify(t1, t2, {}) == {}

    def test_uf(self):
        t1 = 2
        t2 = 1
        try:
            b.unify(t1, t2, {})
            self.assertFalse(True)
        except b.UnificationFailure as e:
            self.assertEqual(e.term1, t1)
            self.assertEqual(e.term2, t2)

    def test_vc(self):
        t1 = b.Var(1)
        t2 = 1
        u = b.unify(t1, t2, {})
        self.assertEqual(u,{1:1})

    def test_cv(self):
        t1 = 1
        t2 = b.Var(1)
        u = b.unify(t1, t2, {})
        self.assertEqual(u,{1:1})

    def test_bc(self):
        t1 = b.Var(1)
        t2 = 1
        u = b.unify(t1, t2, {1:1})
        self.assertEqual(u,{1:1})

    def test_failbc(self):
        t1 = b.Var(1)
        t2 = 1
        try:
            u = b.unify(t1, t2, {1:2})
            self.assertEqual(u,{1:1})
        except b.UnificationFailure as e:
            self.assertEqual(e.term1, 2)
            self.assertEqual(e.term2, 1)

    def test_multib(self):
        t1 = b.Var(1)
        t2 = 2
        u = b.unify(t1, 2, {1:b.Var(3), 3:2})
        foo = "no Exceptions were thrown"
        self.assertNotEqual(foo, "")


    def test_multib2(self):
        t1 = b.Var(1)
        t2 = b.Var(2)
        u = b.unify(t1, 2, {1:b.Var(3), 2:b.Var(4), 4:b.Var(1), 3:2})
        foo = "no Exceptions were thrown"
        self.assertNotEqual(foo, "")

    def test_multib3(self):
        t1 = b.Var(1)
        t2 = b.Var(2)
        u = b.unify(t1, 2, {1:b.Var(3), 2:b.Var(4), 4:1, 3:2})
        foo = "no Exceptions were thrown"
        self.assertNotEqual(foo, "")



if __name__ == '__main__':
    unittest.main()
