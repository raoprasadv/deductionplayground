import unittest
import deduction.parse_term as p

class MyTestCase(unittest.TestCase):
    def test_base(self):
        t,_ = p.consume_term("p")
        self.assertEqual(t, ['p'])

    def test_base1(self):
        try:
            t,_ = p.consume_term("paa paa")
        except p.ParseError as e:
            self.assertEqual(e.message, 'space separated atoms' )

    def test_p1(self):
        t,idx = p.consume_term("p(1)")
        self.assertEqual(t, ['p', ['1']])
        self.assertEqual(idx, 3)  # idx points to the last consumed character

    def test_p2(self):
        s = "p(1,2,3)"
        t, idx = p.consume_term(s)
        self.assertEqual(t, ['p', ['1', '2', '3']])
        self.assertEqual(idx, len(s) - 1)  # idx points to the last consumed character

    def test_p3(self):
        s = "p(1,2,3),"
        t, idx = p.consume_term(s)
        self.assertEqual(t, ['p', ['1', '2', '3']])
        self.assertEqual(idx, 7)  # idx points to the last consumed character


if __name__ == '__main__':
    unittest.main()
