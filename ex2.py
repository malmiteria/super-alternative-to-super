
class D:
    def method(self):
        yield 'D'

class C(D):
    def method(self):
        yield 'C'
        yield from super().method()

class B(C):
    def method(self):
        yield 'B'
        yield from super().method()

class A(B,C):
    def method(self):
        yield 'A'
        yield from super().method()

print(list(A().method()))
from parent import build_parenting_order
print(build_parenting_order(A))
