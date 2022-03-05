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
        yield from A.__as_parent__(B, self).method(*args, **kwargs)
        yield from A.__as_parent__(C, self).method(*args, **kwargs)
