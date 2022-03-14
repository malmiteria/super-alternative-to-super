from parent import Parenting, ConcurentMethodResolutionError
import unittest


class TestMROStraightForward(unittest.TestCase):
    def test(self):
        class A(Parenting):
            attribute = 'a'
            def method(self):
                return 'A'

        assert A().method() == 'A'
        assert A().attribute == 'a'

class TestMROCantBeFound(unittest.TestCase):
    def test_parent_dont_have_it(self):
        class B(Parenting):
            pass
        class A(B):
            pass

        with self.assertRaises(AttributeError):
            A().method
        with self.assertRaises(AttributeError):
            A().attribute

    def test_child_has_it(self):
        class B(Parenting):
            pass
        class A(B):
            attribute = 'a'
            def method(self):
                return 'A'

        assert A().method() == 'A'
        assert A().attribute == 'a'

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
            A().method
        with self.assertRaises(AttributeError):
            A().attribute

class TestMROOnlyOneParentHasIt(unittest.TestCase):
    def test_with_one_parent(self):
        class B(Parenting):
            attribute = 'b'
            def method(self):
                return 'B'
        class A(B):
            pass

        assert A().method() == 'B'
        assert A().attribute == 'b'

    def test_one_parent_only_has_it_with_multiple_parents(self):
        class C(Parenting):
            pass
        class B(Parenting):
            attribute = 'b'
            def method(self):
                return 'B'
        class A(B,C):
            pass

        assert A().method() == 'B'
        assert A().attribute == 'b'

    def test_one_parent_has_it_but_child_has_it_too(self):
        class B(Parenting):
            attribute = 'b'
            def method(self):
                return 'B'
        class A(B):
            attribute = 'a'
            def method(self):
                return 'A'

        assert A().method() == 'A'
        assert A().attribute == 'a'


class TestMROMultipleParentHaveIt(unittest.TestCase):
    def test_double_inheritance(self):
        class C(Parenting):
            attribute = 'c'
            def method(self):
                return 'C'
        class B(Parenting):
            attribute = 'b'
            def method(self):
                return 'B'
        class A(B,C):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            A().attribute

    def test_two_parent_have_it_and_others_dont(self):
        class E(Parenting):
            pass
        class D(Parenting):
            pass
        class C(Parenting):
            attribute = 'c'
            def method(self):
                return 'C'
        class B(Parenting):
            attribute = 'b'
            def method(self):
                return 'B'
        class A(B,C,D,E):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            A().attribute

    def test_two_parent_have_it_but_child_too(self):
        class C(Parenting):
            attribute = 'c'
            def method(self):
                return 'C'
        class B(Parenting):
            attribute = 'b'
            def method(self):
                return 'B'
        class A(B,C):
            attribute = 'a'
            def method(self):
                return 'A'

        assert A().method() == 'A'
        assert A().attribute == 'a'

    def test_one_parent_raise_concurent_method_resolution_error(self):
        class D(Parenting):
            attribute = 'd'
            def method(self):
                return 'D'
        class C(Parenting):
            attribute = 'c'
            def method(self):
                return 'C'
        class B(C,D):
            pass
        class A(B):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            A().attribute

    def test_one_parent_raise_concurent_method_resolution_error_but_child_has_it(self):
        class D(Parenting):
            attribute = 'd'
            def method(self):
                return 'D'
        class C(Parenting):
            attribute = 'c'
            def method(self):
                return 'C'
        class B(C,D):
            pass
        class A(B):
            attribute = 'a'
            def method(self):
                return 'A'

        assert A().method() == 'A'
        assert A().attribute == 'a'

    def test_one_parent_raise_concurent_method_resolution_error_and_one_parent_has_it(self):
        class E(Parenting):
            attribute = 'e'
            def method(self):
                return 'E'
        class D(Parenting):
            attribute = 'd'
            def method(self):
                return 'D'
        class C(D,E):
            pass
        class B(Parenting):
            attribute = 'b'
            def method(self):
                return 'B'
        class A(B,C):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            A().attribute

