from parent import Parenting, ConcurentMethodResolutionError
import unittest


class TestMROStraightForward(unittest.TestCase):
    def test(self):
        class A(Parenting):
            def method(self):
                return 'A'

        order = A().method()

        assert order == 'A'

class TestMROCantBeFound(unittest.TestCase):
    def test(self):
        class A(Parenting):
            pass

        with self.assertRaises(AttributeError):
            order = A().method

    def test_double_inheritence(self):
        class C(Parenting):
            def method(self):
                return 'C'
        class B(Parenting):
            def __init__(self):
                self.name = 'B'
            def method(self):
                return 'B'
        class A(B,C):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            A().method
# only direct parents
# parenting order shouldn't change based on child inheritence tree
# should raise error when parent is not in bases

