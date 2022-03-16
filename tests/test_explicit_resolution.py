from parent import ExplicitMethodResolution, ConcurentMethodResolutionError
import unittest


class TestMROStraightForward(unittest.TestCase):
    def test(self):
        class A(ExplicitMethodResolution):
            attribute = 'a'
            def method(self):
                return 'A'

        assert A().method() == 'A'
        assert A().attribute == 'a'

class TestMROCantBeFound(unittest.TestCase):
    def test_parent_dont_have_it(self):
        class B(ExplicitMethodResolution):
            pass
        class A(B):
            pass

        with self.assertRaises(AttributeError):
            A().method
        with self.assertRaises(AttributeError):
            A().attribute

    def test_child_has_it(self):
        class B(ExplicitMethodResolution):
            pass
        class A(B):
            attribute = 'a'
            def method(self):
                return 'A'

        assert A().method() == 'A'
        assert A().attribute == 'a'

    def test_cant_be_found_in_multiple_parent_either(self):
        class E(ExplicitMethodResolution):
            pass
        class D(ExplicitMethodResolution):
            pass
        class C(ExplicitMethodResolution):
            pass
        class B(ExplicitMethodResolution):
            pass
        class A(B,C,D,E):
            pass

        with self.assertRaises(AttributeError):
            A().method
        with self.assertRaises(AttributeError):
            A().attribute

class TestMROOnlyOneParentHasIt(unittest.TestCase):
    def test_with_one_parent(self):
        class B(ExplicitMethodResolution):
            attribute = 'b'
            def method(self):
                return 'B'
        class A(B):
            pass

        assert A().method() == 'B'
        assert A().attribute == 'b'

    def test_one_parent_only_has_it_with_multiple_parents(self):
        class C(ExplicitMethodResolution):
            pass
        class B(ExplicitMethodResolution):
            attribute = 'b'
            def method(self):
                return 'B'
        class A(B,C):
            pass

        assert A().method() == 'B'
        assert A().attribute == 'b'

    def test_one_parent_has_it_but_child_has_it_too(self):
        class B(ExplicitMethodResolution):
            attribute = 'b'
            def method(self): pass
        class A(B):
            attribute = 'a'
            def method(self):
                return 'A'

        assert A().method() == 'A'
        assert A().attribute == 'a'


class TestMROMultipleParentHaveIt(unittest.TestCase):
    def test_double_inheritance(self):
        class C(ExplicitMethodResolution):
            attribute = 'c'
            def method(self): pass
        class B(ExplicitMethodResolution):
            attribute = 'b'
            def method(self): pass
        class A(B,C):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            A().attribute

    def test_two_parent_have_it_and_others_dont(self):
        class E(ExplicitMethodResolution):
            pass
        class D(ExplicitMethodResolution):
            pass
        class C(ExplicitMethodResolution):
            attribute = 'c'
            def method(self): pass
        class B(ExplicitMethodResolution):
            attribute = 'b'
            def method(self): pass
        class A(B,C,D,E):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            A().attribute

    def test_two_parent_have_it_but_child_too(self):
        class C(ExplicitMethodResolution):
            attribute = 'c'
            def method(self): pass
        class B(ExplicitMethodResolution):
            attribute = 'b'
            def method(self): pass
        class A(B,C):
            attribute = 'a'
            def method(self):
                return 'A'

        assert A().method() == 'A'
        assert A().attribute == 'a'

    def test_one_parent_raise_concurent_method_resolution_error(self):
        class D(ExplicitMethodResolution):
            attribute = 'd'
            def method(self): pass
        class C(ExplicitMethodResolution):
            attribute = 'c'
            def method(self): pass
        class B(C,D):
            pass
        class A(B):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            A().attribute

    def test_one_parent_raise_concurent_method_resolution_error_but_child_has_it(self):
        class D(ExplicitMethodResolution):
            attribute = 'd'
            def method(self): pass
        class C(ExplicitMethodResolution):
            attribute = 'c'
            def method(self): pass
        class B(C,D):
            pass
        class A(B):
            attribute = 'a'
            def method(self):
                return 'A'

        assert A().method() == 'A'
        assert A().attribute == 'a'

    def test_one_parent_raise_concurent_method_resolution_error_and_one_parent_has_it(self):
        class E(ExplicitMethodResolution):
            attribute = 'e'
            def method(self): pass
        class D(ExplicitMethodResolution):
            attribute = 'd'
            def method(self): pass
        class C(D,E):
            pass
        class B(ExplicitMethodResolution):
            attribute = 'b'
            def method(self): pass
        class A(B,C):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            A().attribute


class TestMROMultipleParentResolveItFromTheSameGrandparent(unittest.TestCase):
    def test_diamond_shape(self):
        class D(ExplicitMethodResolution):
            attribute = 'd'
            def method(self):
                return 'D'
        class C(D):
            pass
        class B(D):
            pass
        class A(B,C):
            pass

        assert A().method() == 'D'
        assert A().attribute == 'd'

    def test_diamond_shape_but_child_resolves_it(self):
        class D(ExplicitMethodResolution):
            attribute = 'd'
            def method(self): pass
        class C(D):
            pass
        class B(D):
            pass
        class A(B,C):
            attribute = 'a'
            def method(self):
                return 'A'

        assert A().method() == 'A'
        assert A().attribute == 'a'

    def test_diamond_shape_but_one_direct_parent_redefines_it(self):
        class D(ExplicitMethodResolution):
            attribute = 'd'
            def method(self): pass
        class C(D):
            attribute = 'c'
            def method(self): pass
        class B(D):
            pass
        class A(B,C):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            A().attribute

    def test_diamond_shape_but_another_parent_resolves_it(self):
        class E(ExplicitMethodResolution):
            attribute = 'e'
            def method(self): pass
        class D(ExplicitMethodResolution):
            attribute = 'd'
            def method(self): pass
        class C(E):
            pass
        class B(E):
            pass
        class A(B,C,D):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            A().attribute
