from parent import Parenting, ConcurentMethodResolutionError
import unittest


class TestMROStraightForward(unittest.TestCase):
    def test(self):
        class A(Parenting):
            def method(self):
                return 'A'

        assert A().method() == 'A'

class TestMROCantBeFound(unittest.TestCase):
    def test_parent_dont_have_it(self):
        class B(Parenting):
            pass
        class A(B):
            pass

        with self.assertRaises(AttributeError):
            order = A().method

    def test_child_has_it(self):
        class B(Parenting):
            pass
        class A(B):
            def method(self):
                return 'A'

        assert A().method() == 'A'

    def test_cant_be_found_in_multiple_parent_either(self):
        class E(Parenting):
            pass
        class D(Parenting):
            pass
        class C(Parenting):
            pass
        class B(Parenting):
            pass
        class A(B,C,D,E):
            pass

        with self.assertRaises(AttributeError):
            order = A().method

class TestMROOnlyOneParentHasIt(unittest.TestCase):
    def test_with_one_parent(self):
        class B(Parenting):
            def method(self):
                return 'B'
        class A(B):
            pass

        assert A().method() == 'B'

    def test_one_parent_only_has_it_with_multiple_parents(self):
        class C(Parenting):
            pass
        class B(Parenting):
            def method(self):
                return 'B'
        class A(B,C):
            pass

        assert A().method() == 'B'

    def test_one_parent_has_it_but_child_has_it_too(self):
        class B(Parenting):
            def method(self):
                return 'B'
        class A(B):
            def method(self):
                return 'A'

        assert A().method() == 'A'


class TestMROMultipleParentHaveIt(unittest.TestCase):
    def test_double_inheritence(self):
        class C(Parenting):
            def method(self):
                return 'C'
        class B(Parenting):
            def method(self):
                return 'B'
        class A(B,C):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            A().method

    def test_two_parent_have_it_and_others_dont(self):
        class E(Parenting):
            pass
        class D(Parenting):
            pass
        class C(Parenting):
            def method(self):
                return 'C'
        class B(Parenting):
            def method(self):
                return 'B'
        class A(B,C,D,E):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            A().method

    def test_two_parent_have_it_but_child_too(self):
        class C(Parenting):
            def method(self):
                return 'C'
        class B(Parenting):
            def method(self):
                return 'B'
        class A(B,C):
            def method(self):
                return 'A'

        assert A().method() == 'A'

    def test_one_parent_raise_concurent_method_resolution_error(self):
        class D(Parenting):
            def method(self):
                return 'D'
        class C(Parenting):
            def method(self):
                return 'C'
        class B(C,D):
            pass
        class A(B):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            A().method

    def test_one_parent_raise_concurent_method_resolution_error_but_child_has_it(self):
        class D(Parenting):
            def method(self):
                return 'D'
        class C(Parenting):
            def method(self):
                return 'C'
        class B(C,D):
            pass
        class A(B):
            def method(self):
                return 'A'

        assert A().method() == 'A'

    def test_one_parent_raise_concurent_method_resolution_error_and_one_parent_has_it(self):
        class E(Parenting):
            def method(self):
                return 'E'
        class D(Parenting):
            def method(self):
                return 'D'
        class C(D,E):
            pass
        class B(Parenting):
            def method(self):
                return 'B'
        class A(B,C):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            A().method

