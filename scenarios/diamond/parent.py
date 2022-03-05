from parent import Parenting

class D(Parenting):
    def method(self, *args, **kwargs):
        yield 'D'

class C(D):
    def method(self, *args, **kwargs):
        yield 'C'
        yield from C.__as_parent__(D, self).method(*args, **kwargs)

class B(D):
    def method(self, *args, **kwargs):
        yield 'B'
        yield from B.__as_parent__(D, self).method(*args, **kwargs)

class A(B,C):
    def method(self, *args, **kwargs):
        yield 'A'
        yield from A.__as_parent__(B, self).method(*args, **kwargs)
        yield from A.__as_parent__(C, self).method(*args, **kwargs)
