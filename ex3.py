from parent import Parenting


class G(Parenting):
    def method(self):
        yield 'G'

class F(Parenting):
    def method(self):
        yield 'F'
        #yield from super().method()

class E(Parenting):
    def method(self):
        yield 'E'
        #yield from super().method()

class D(Parenting):
    def method(self):
        yield 'D'
        yield from super().method()

class C(F,G):
    def method(self):
        yield 'C'
        yield from self.parent(F).method()
        yield from self.parent(G).method()
        #yield from super(.method()

class B(D,E):
    def method(self):
        yield 'B'
        yield from B.parent(self, D).method()
        #yield from parent(self, B, E).method()
        #yield from super().method()

class A(B,C):
    def method(self):
        yield 'A'
        yield from self.parent(B).method()
        yield from self.parent(C).method()
        #yield from super().method()

print(list(A().method()))
