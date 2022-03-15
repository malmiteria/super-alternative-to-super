from parent import Parenting

class C(Parenting):
    def method(self, *args, **kwargs):
        yield 'C'

class B(Parenting):
    def method(self, *args, **kwargs):
        yield 'B'

class A(B,C):
    def method(self, *args, **kwargs):
        yield 'A'
        yield from self.__as_parent__(B).method(*args, **kwargs)
        yield from self.__as_parent__(C).method(*args, **kwargs)
