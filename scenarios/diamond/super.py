
class D:
    def method(self, *args, **kwargs):
        yield 'D'

class C(D):
    def method(self, *args, **kwargs):
        yield 'C'
        yield from super().method(*args, **kwargs)

class B(D):
    def method(self, *args, **kwargs):
        yield 'B'
        yield from super().method(*args, **kwargs)

class A(B,C):
    def method(self, *args, **kwargs):
        yield 'A'
        yield from super().method(*args, **kwargs)
        #yield from super(C, self).method(*args, **kwargs)
        #yield from super(B, self).method(*args, **kwargs)
        #yield from super(C, self).method(*args, **kwargs)
