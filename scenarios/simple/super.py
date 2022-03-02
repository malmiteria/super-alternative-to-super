

class B:
    def method(self, *args, **kwargs):
        yield 'B'

class A(B):
    def method(self, *args, **kwargs):
        yield 'A'
        yield from super().method(*args, **kwargs)
