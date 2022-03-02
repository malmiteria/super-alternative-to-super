
class D:
    def method(self, *args, **kwargs):
        yield 'D'

class C(D):
    def method(self, *args, **kwargs):
        yield 'C'

class B(D):
    def method(self, *args, **kwargs):
        yield 'B'

class A(B,C):
    def method(self, *args, **kwargs):
        yield 'A'
