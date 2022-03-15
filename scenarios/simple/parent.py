from parent import Parenting

class B(Parenting):
    def method(self, *args, **kwargs):
        yield 'B'

class A(B):
    def method(self, *args, **kwargs):
        yield 'A'
        yield from self.__as_parent__(B).method(*args, **kwargs)
