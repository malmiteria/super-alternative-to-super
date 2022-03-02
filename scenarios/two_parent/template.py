
class C:
    def method(self, *args, **kwargs):
        yield 'C'

class B:
    def method(self, *args, **kwargs):
        yield 'B'

class A(B,C):
    def method(self, *args, **kwargs):
        yield 'A'
