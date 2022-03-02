from parent import Parenting

class D(Parenting):
    def method(self, *args, **kwargs):
        yield 'D'

class C(D):
    def method(self, *args, **kwargs):
        yield 'C'
        yield from self.parent(D).method(*args, **kwargs)

class B(D):
    def method(self, *args, **kwargs):
        yield 'B'
        yield from self.parent(D).method(*args, **kwargs)

class A(B,C):
    def method(self, *args, **kwargs):
        yield 'A'
        yield from self.parent(B).method(*args, **kwargs)
        yield from self.parent(C).method(*args, **kwargs)
