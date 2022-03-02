
class C:
    def method(self, *args, **kwargs):
        yield 'C'

class B:
    def method(self, *args, **kwargs):
        yield 'B'

class A(B,C):
    def method(self, *args, **kwargs):
        yield 'A'
        yield from super().method(*args, **kwargs)
        yield from super(B, self).method(*args, **kwargs)
