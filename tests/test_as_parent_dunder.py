from parent import AsParent
import unittest


class TestAsParentResolution(unittest.TestCase):
    def test_simple_inheritance(self):
        class B(AsParent):
            def method(self):
                yield 'B'
        class A(B):
            def method(self):
                yield 'A'
                yield from self.__as_parent__(B).method()

        assert list(A().method()) == ['A', 'B']

    def test_with_one_extra_layer(self):
        class C(AsParent):
            def method(self):
                yield 'C'
        class B(C):
            def method(self):
                yield 'B'
                yield from self.__as_parent__(C).method()
        class A(B):
            def method(self):
                yield 'A'
                yield from self.__as_parent__(B).method()

        assert list(A().method()) == ['A', 'B', 'C']

    def test_with_two_parents(self):
        class C(AsParent):
            def method(self):
                yield 'C'
        class B(AsParent):
            def method(self):
                yield 'B'
        class A(B,C):
            def method(self):
                yield 'A'
                yield from self.__as_parent__(B).method()
                yield from self.__as_parent__(C).method()

        assert list(A().method()) == ['A', 'B', 'C']

    def test_with_diamond_tree(self):
        class D(AsParent):
            def method(self):
                yield 'D'
        class C(D):
            def method(self):
                yield 'C'
                yield from self.__as_parent__(D).method()
        class B(D):
            def method(self):
                yield 'B'
                yield from self.__as_parent__(D).method()
        class A(B,C):
            def method(self):
                yield 'A'
                yield from self.__as_parent__(B).method()
                yield from self.__as_parent__(C).method()

        assert list(A().method()) == ['A', 'B', 'D', 'C', 'D']

    def test_targeted_is_not_an_ancestor(self):
        class B: pass
        class A(AsParent):
            def method(self):
                yield 'A'
                yield from self.__as_parent__(B).method()

        with self.assertRaises(TypeError):
            list(A().method())

    def test_can_target_indirect_parent(self):
        class C(AsParent):
            def method(self):
                yield 'C'
        class B(C):
            def method(self):
                yield 'B'
        class A(B):
            def method(self):
                yield 'A'
                yield from self.__as_parent__(C).method()

        assert list(A().method()) == ['A', 'C']

    def test_cant_target_itself(self):
        class A(AsParent):
            def method(self):
                yield 'A'
                yield from self.__as_parent__(A).method()

        with self.assertRaises(TypeError):
            list(A().method())

    def test_cant_target_itself_in_middle_of_tree(self):
        class B(AsParent):
            def method(self):
                yield 'B'
                self.__as_parent__(B).method()
        class A(B):
            def method(self):
                yield 'A'
                yield from self.__as_parent__(B).method()


        with self.assertRaises(TypeError):
            list(A().method())
